"""Claude metadata and standalone rendering preserve read-only source facts."""

import copy
from dataclasses import replace
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import textwrap
from typing import Any
import unittest
from unittest.mock import patch

from marketplace.build.rendering import (
    claude_marketplace_metadata,
    claude_plugin_metadata,
)
from marketplace.source import discover_source, resolve_identity


class ClaudeMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_plugin_retains_resolved_identity_and_independent_nested_data(self) -> None:
        self.write("group/folder/ai-plugin.yml", textwrap.dedent("""\
            name: published-name
            version: AUTO_VERSION
            description: "Описание / ${AGENT_SKILL(example)}"
            author:
              name: Authored
              extra: [kept]
            hooks:
              SessionStart:
                - hooks:
                    - type: command
                      command: '${CLAUDE_PLUGIN_ROOT}/scripts/start'
            mcpServers:
              server:
                args: [one, two]
            lsp:
              language:
                configuration: {enabled: true}
            arbitrary:
              nested: [{values: [first, second]}]
            empty: null
            enabled: false
        """))
        raw = discover_source(self.root)
        raw_before = copy.deepcopy(raw)
        # Resolve once with a fixed clock and no history. Metadata must consume
        # this identity instead of querying Git again or using AUTO_VERSION.
        with patch("subprocess.run", return_value=subprocess.CompletedProcess(
            args=[], returncode=1, stdout="",
        )):
            resolved = resolve_identity(
                raw, now=datetime(2026, 9, 30, 21, 2, 3, tzinfo=timezone.utc),
                timezone=timezone.utc,
            )
        resolved_before = copy.deepcopy(resolved)
        with patch("subprocess.run", side_effect=AssertionError("Git rerun")), \
                patch("subprocess.Popen", side_effect=AssertionError("Git spawn")):
            result = claude_plugin_metadata(resolved.plugins[0])
            catalog = claude_marketplace_metadata(resolved)

        self.assertEqual(result, {
            "name": "published-name", "version": "26.9.30210203",
            "description": "Описание / ${AGENT_SKILL(example)}",
            "author": {"name": "Authored", "extra": ["kept"]},
            "hooks": {"SessionStart": [{"hooks": [{
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/start",
            }]}]},
            "mcpServers": {"server": {"args": ["one", "two"]}},
            "lsp": {"language": {"configuration": {"enabled": True}}},
            "arbitrary": {"nested": [{"values": ["first", "second"]}]},
            "empty": None, "enabled": False,
        })
        self.assertEqual(catalog["plugins"], [{
            "name": "published-name", "source": "./group/folder",
            "description": "Описание / ${AGENT_SKILL(example)}",
        }])
        result["author"]["extra"].append("changed")
        result["hooks"]["SessionStart"][0]["hooks"][0]["command"] = "changed"
        result["mcpServers"]["server"]["args"].append("changed")
        result["lsp"]["language"]["configuration"]["enabled"] = False
        result["arbitrary"]["nested"][0]["values"].clear()
        catalog["plugins"][0]["description"] = "changed"
        self.assertEqual(raw, raw_before)
        self.assertEqual(resolved, resolved_before)

    def test_marketplace_uses_inventory_order_root_and_grouped_paths(self) -> None:
        self.write("ai-plugin.yml", "name: root\nversion: 1\ndescription: Root\n")
        self.write("group/plugin/ai-plugin.yml", (
            "name: grouped\nversion: 2\ndescription: '  Verbatim описание  '\n"
        ))
        inventory = discover_source(self.root)
        inventory = replace(inventory, plugins=tuple(reversed(inventory.plugins)))
        before = copy.deepcopy(inventory)
        with patch("subprocess.run", side_effect=AssertionError("Git rerun")), \
                patch("subprocess.Popen", side_effect=AssertionError("Git spawn")):
            result = claude_marketplace_metadata(inventory)
        self.assertEqual(result, {
            "name": "zd-plugins",
            "owner": {"name": "ZDreamer2"},
            "metadata": {"description": "AI documentation and marketplace authoring plugins"},
            "plugins": [
                {"name": "grouped", "source": "./group/plugin",
                 "description": "  Verbatim описание  "},
                {"name": "root", "source": "./", "description": "Root"},
            ],
        })
        self.assertEqual(inventory, before)
        self.assertEqual(inventory.plugins[-1].root, ".")

    def test_description_preflight_is_not_part_of_claude_metadata(self) -> None:
        self.write("missing/ai-plugin.yml", "name: missing\nversion: 1\n")
        self.write("null/ai-plugin.yml", "name: null-description\ndescription: null\n")
        inventory = discover_source(self.root)
        self.assertEqual(claude_plugin_metadata(inventory.plugins[0]), {
            "name": "missing", "version": 1,
        })
        self.assertEqual(claude_marketplace_metadata(inventory)["plugins"], [
            {"name": "missing", "source": "./missing", "description": None},
            {"name": "null-description", "source": "./null", "description": None},
        ])

    def test_empty_marketplace(self) -> None:
        self.assertEqual(claude_marketplace_metadata(discover_source(self.root)), {
            "name": "zd-plugins", "owner": {"name": "ZDreamer2"},
            "metadata": {"description": "AI documentation and marketplace authoring plugins"},
            "plugins": [],
        })


def snapshot(directory: Path) -> dict[str, tuple[Any, ...]]:
    """Capture directories, links and file bytes/modes without following links."""
    result = {}
    for path in (directory, *directory.rglob("*")):
        mode = path.lstat().st_mode
        key = path.relative_to(directory).as_posix()
        if stat.S_ISLNK(mode):
            result[key] = (mode, os.readlink(path))
        elif stat.S_ISDIR(mode):
            result[key] = (mode,)
        else:
            result[key] = (mode, path.read_bytes())
    return result


class StandaloneRenderingTests(unittest.TestCase):
    def test_copied_plugin_has_no_external_dependencies_or_source_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / "installed" / "ai-marketplace"
            # Keep the source plugin's links as links: a dangling @common must
            # not become an accidental installed dependency of this library.
            shutil.copytree(
                Path(__file__).resolve().parents[5], plugin, symlinks=True,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
            )
            docs = plugin / "docs"
            docs.mkdir(exist_ok=True)
            (docs / "included.md").write_bytes(
                b"\xff ${AGENT_QUESTION_TOOL}\r\n"
            )
            (docs / "included.md").chmod(0o640)
            cwd = root / "unrelated"
            cwd.mkdir()
            before = snapshot(root)
            program = textwrap.dedent("""\
                import json
                import os
                import subprocess
                import sys
                import sysconfig
                from dataclasses import replace
                from pathlib import Path

                plugin = Path(sys.argv[1])
                stdlib = sysconfig.get_path('stdlib')
                platstdlib = sysconfig.get_path('platstdlib')
                sys.path[:] = [str(plugin / 'scripts'), stdlib, platstdlib,
                               os.path.join(platstdlib, 'lib-dynload')]
                from marketplace.source import discover_source
                from marketplace.build.rendering import (
                    render_file, render_markdown, claude_plugin_metadata,
                    claude_marketplace_metadata,
                )

                def forbidden(*args, **kwargs):
                    raise AssertionError('Rendering must not run Git or commands')

                subprocess.run = forbidden
                subprocess.Popen = forbidden
                raw = discover_source(plugin)
                inventory = replace(raw, plugins=tuple(
                    replace(p, manifest={**p.manifest, 'version': '3.2.1'})
                    for p in raw.plugins
                ))
                outputs = {}
                for host in ('claude', 'codex', 'pi'):
                    content = ('${AGENT_INCLUDE_DOC_FOR(claude, included.md)}\\n'
                               '${AGENT_SKILL(ai-marketplace)}')
                    outputs[host] = render_file(
                        content, 'docs/document.md', host, inventory,
                    ).encode('utf-8', 'surrogateescape').hex()
                outputs['markdown'] = render_markdown(
                    '${AGENT_SUBAGENT_TOOL}', 'docs/plain.txt', 'claude', inventory,
                )
                outputs['resource'] = render_file(
                    '${AGENT_BAD(%)}', 'docs/resource.MD', 'claude', inventory,
                )
                outputs['plugin'] = claude_plugin_metadata(inventory.plugins[0])
                outputs['marketplace'] = claude_marketplace_metadata(inventory)
                print(json.dumps(outputs))
            """)
            env = os.environ.copy()
            env["PYTHONPATH"] = str(root / "unavailable-inherited-import-root")
            env["PYTHONTZPATH"] = ""
            result = subprocess.run(
                ["python3", "-B", "-S", "-c", program, str(plugin)],
                cwd=cwd, env=env, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, check=True,
            )
            self.assertEqual(json.loads(result.stdout), {
                "claude": b"\xff AskUserQuestion\r\n/ai-marketplace".hex(),
                "codex": b"$ai-marketplace:ai-marketplace".hex(),
                "pi": b"/skill:ai-marketplace".hex(),
                "markdown": "Agent", "resource": "${AGENT_BAD(%)}",
                "plugin": {
                    "name": "ai-marketplace", "version": "3.2.1",
                    "description": "Ai plugins marketplace development",
                    "author": {"name": "ZDreamer"},
                },
                "marketplace": {
                    "name": "zd-plugins", "owner": {"name": "ZDreamer2"},
                    "metadata": {"description": "AI documentation and marketplace authoring plugins"},
                    "plugins": [{
                        "name": "ai-marketplace", "source": "./",
                        "description": "Ai plugins marketplace development",
                    }],
                },
            })
            self.assertEqual(result.stderr, "")
            self.assertEqual(snapshot(root), before)


if __name__ == "__main__":
    unittest.main()
