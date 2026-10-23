"""Pin Codex rendering's PHP contract through the standalone public API."""

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from marketplace.build.rendering import (
    CodexConstruct, FileRendering, codex_marketplace_metadata, codex_plugin_metadata,
    render_file, render_file_result,
)
from marketplace.source import codex_skill_names, discover_source

from .test_claude import snapshot


class CodexTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("group/folder/ai-plugin.yml", (
            "name: manifest-name\nversion: 2.3.4\ndescription: Plugin\n"
            "author: {name: Authored, extra: [kept]}\nhooks: [ignored]\n"
        ))
        self.path = "group/folder/skills/run/SKILL.md"
        self.write(self.path, "body")
        self.source = discover_source(self.root)

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8", "surrogateescape"))

    def render(self, text: str) -> FileRendering:
        return render_file_result(text, self.path, "codex", self.source)

    def test_complete_reduction_sidecar_and_two_location_spaces(self) -> None:
        content = (
            "---\nname: frontmatter-name\ndescription: 'Deep work: tricky half'\n"
            "argument-hint: [thing]\ndisable-model-invocation: true\n"
            "user-invocable: false\nmodel: sonnet\nignored: null\n---\n"
            "\r\nUse $ARGUMENTS and /folder:run.\r\n\udcff final"
        )
        expected = (
            "---\nname: frontmatter-name\n"
            "description: 'Deep work: tricky half. Usage: $folder:run [thing].'\n"
            "---\n\r\nUse $ARGUMENTS and /folder:run.\r\n\udcff final"
        )
        before = snapshot(self.root)
        with patch("subprocess.run", side_effect=AssertionError("Git")), \
                patch("subprocess.Popen", side_effect=AssertionError("Git")):
            result = self.render(content)
        self.assertEqual(result.content, expected)
        self.assertEqual(render_file(content, self.path, "codex", self.source), expected)
        self.assertEqual(result.extra_files, {
            "agents/openai.yaml": "policy:\n  allow_implicit_invocation: false\n",
        })
        self.assertEqual([(f.category, f.line, f.text) for f in result.findings], [
            (CodexConstruct.SKILL_FRONTMATTER, 6, "user-invocable: false"),
            (CodexConstruct.SKILL_FRONTMATTER, 7, "model: sonnet"),
            (CodexConstruct.CLAUDE_VARIABLE, 6, "$ARGUMENTS"),
            (CodexConstruct.SKILL_INVOCATION, 6, "/folder:run"),
        ])
        self.assertEqual(snapshot(self.root), before)
        result.extra_files.clear()
        result.findings.clear()
        self.assertTrue(self.render(content).findings)
        self.assertTrue(self.render(content).extra_files)

    def test_argument_hint_source_recovery_and_punctuation(self) -> None:
        cases = [
            ("[issue-id]", "Internal", "Internal. Usage: $folder:run [issue-id]."),
            ("12", "Already!", "Already! Usage: $folder:run 12."),
            ("false", "Ready?", "Ready? Usage: $folder:run false."),
            ("''", "Done.", "Done. Usage: $folder:run ''."),
            ('""', "Done", 'Done. Usage: $folder:run "".'),
            ("null", "Internal", "Internal"),
            ("'  hint  '", "Internal", "Internal. Usage: $folder:run   hint  ."),
            ("[x] # written", "Internal", "Internal. Usage: $folder:run [x] # written."),
        ]
        from marketplace import parse_yaml
        for hint, description, expected in cases:
            with self.subTest(hint=hint):
                result = self.render(
                    f"---\ndescription: '{description}'\nargument-hint: {hint}\n---\n"
                )
                data = parse_yaml(result.content[4:].split("\n---\n")[0])
                self.assertEqual(data, {"description": expected})
                self.assertEqual(result.findings, [])
        result = self.render(
            "---\ndescription: |\n  Stopped!\nargument-hint: x\n---\n"
        )
        self.assertEqual(result.content,
                         '---\ndescription: "Stopped!\\n Usage: $folder:run x."\n---\n')

    def test_strict_defaults_nulls_and_source_key_locations(self) -> None:
        for value, sidecar in (("false", False), ("0", True), ("true", True),
                               ("1", True), ("null", True), ("''", True)):
            with self.subTest(disable=value):
                result = self.render(
                    "---\ndescription: Test\ndisable-model-invocation: "
                    + value + "\n---\nbody"
                )
                self.assertEqual(bool(result.extra_files), sidecar)
                self.assertEqual(result.findings, [])
        for value, reported in (("true", False), ("1", True), ("false", True),
                                ("0", True), ("null", True)):
            with self.subTest(invocable=value):
                result = self.render(
                    "---\ndescription: Test\nuser-invocable: " + value + "\n---\n"
                )
                self.assertEqual(bool(result.findings), reported)
        result = self.render(
            "---\ndescription: Test\n'quoted': odd\n"
            "model  : sonnet \nnull-key: null\n"
            "<<: {merged: x}\n---\nbody"
        )
        self.assertEqual([(f.line, f.text) for f in result.findings], [
            (1, "quoted"), (4, "model  : sonnet"), (1, "merged"),
        ])

    def test_name_types_remain_authored_and_description_is_not_stricter(self) -> None:
        cases = [
            ("", ""), ("name: null\n", ""), ("name: false\n", "name: false\n"),
            ("name: 0\n", "name: 0\n"), ("name: [x, y]\n", "name:\n    - x\n    - 'y'\n"),
            ("name: {nested: [true]}\n", "name:\n    nested: [true]\n"),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                result = self.render("---\n" + source + "description: ' '\n---\n")
                self.assertEqual(result.content, "---\n" + expected + "description: ' '\n---\n")
                self.assertEqual(result.findings, [])

    def test_report_only_invalid_frontmatter_delimiters_and_descriptions(self) -> None:
        absent = "no frontmatter: Codex will not load this skill"
        invalid = "frontmatter is not valid YAML: Codex will not load this skill"
        missing = "no description: Codex has nothing to route this skill on"
        cases = [
            ("Body", absent), ("\ufeff---\ndescription: X\n---\nbody", absent),
            ("---\r\ndescription: X\r\n---\r\nbody", absent),
            ("---\ndescription: X\n---", absent),
            ("---\ndescription: X\n", absent),
            ("---\nname: [unclosed\n---\nbody", invalid),
            ("---\nscalar\n---\nbody", missing),
            ("---\n[description, text]\n---\nbody", missing),
            ("---\nname: run\n---\nbody", missing),
        ]
        for description in ("null", "''", "0", "false", "[x]", "{x: y}"):
            cases.append((f"---\ndescription: {description}\n---\nbody", missing))
        for content, reason in cases:
            with self.subTest(content=content):
                result = self.render(content)
                self.assertEqual(result.content, content)
                self.assertEqual(result.extra_files, {})
                self.assertEqual([(f.line, f.text) for f in result.findings], [(1, reason)])

    def test_shared_stages_precede_reduction_and_scan_even_for_invalid_skill(self) -> None:
        self.write("group/folder/docs/note.md", "AskUserQuestion ${AGENT_SUBAGENT_TOOL}\n")
        result = self.render(
            "---\ndescription: ${AGENT_SUBAGENT_TOOL}\nmodel: sonnet\n---\n"
            "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/note.md)}\n"
        )
        self.assertEqual(result.content,
                         "---\ndescription: spawn_agent\n---\nAskUserQuestion spawn_agent\n")
        self.assertEqual([(f.line, f.text) for f in result.findings],
                         [(3, "model: sonnet"), (4, "AskUserQuestion")])
        result = self.render("${AGENT_SUBAGENT_TOOL} $ARGUMENTS")
        self.assertEqual(result.content, "spawn_agent $ARGUMENTS")
        self.assertEqual([f.text for f in result.findings], [
            "no frontmatter: Codex will not load this skill", "$ARGUMENTS",
        ])

    def test_path_selection_and_empty_collections(self) -> None:
        content = "---\ndescription: Test\nmodel: sonnet\n---\nAskUserQuestion"
        for path in ("README.md", "group/folder/workflows/do.md",
                     "group/folder/skills/run/docs/SKILL.md"):
            result = render_file_result(content, path, "codex", self.source)
            self.assertEqual(result.content, content)
            self.assertEqual([f.text for f in result.findings], ["AskUserQuestion"])
        for path in ("README.MD", "hooks.json", "script"):
            result = render_file_result("${AGENT_BAD} " + content, path, "unknown", self.source)
            self.assertEqual(result.content, "${AGENT_BAD} " + content)
            self.assertEqual(result.findings, [])
            self.assertEqual(result.extra_files, {})
        for host in ("claude",):
            result = render_file_result(content, self.path, host, self.source)
            self.assertEqual(result.content, content)
            self.assertEqual(result.findings, [])
            self.assertEqual(result.extra_files, {})
        with self.assertRaisesRegex(ValueError, "must define name 'run'"):
            render_file_result(content, self.path, "pi", self.source)

    def test_metadata_filtering_physical_skills_and_independent_nested_results(self) -> None:
        before = deepcopy(self.source)
        with patch("subprocess.run", side_effect=AssertionError("Git")):
            metadata = codex_plugin_metadata(self.source.plugins[0])
            catalog = codex_marketplace_metadata(self.source)
        self.assertEqual(metadata, {
            "name": "manifest-name", "version": "2.3.4", "description": "Plugin",
            "author": {"name": "Authored", "extra": ["kept"]}, "skills": "./skills/",
        })
        self.assertEqual(catalog, {
            "name": "zd-plugins", "interface": {"displayName": "ZDreamer2 plugins"},
            "plugins": [{"name": "manifest-name", "source": {
                "source": "local", "path": "./group/folder",
            }, "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Productivity"}],
        })
        metadata["author"]["extra"].clear()
        catalog["plugins"][0]["policy"].clear()
        self.assertEqual(self.source, before)
        self.assertTrue(codex_marketplace_metadata(self.source)["plugins"][0]["policy"])
        plugin = self.source.plugins[0]
        for description in (None, "", 0, False, [], {}):
            with self.subTest(description=description), self.assertRaisesRegex(
                ValueError, "Plugin 'group/folder' must define a description in ai-plugin.yml: Codex requires it.",
            ):
                codex_plugin_metadata(replace(plugin, manifest={
                    **plugin.manifest, "description": description,
                }))
        empty = self.root / "empty"
        empty.mkdir()
        (empty / "skills").mkdir()
        for author in (None, False, {}):
            manifest = {"name": "empty", "version": "1", "description": " ", "author": author}
            result = codex_plugin_metadata(replace(plugin, directory=empty, manifest=manifest))
            self.assertEqual(result.get("author"), author)
            self.assertEqual("author" in result, author is not None)
            self.assertEqual(result["skills"], "./skills/")
        (empty / "skills").rmdir()
        self.assertNotIn("skills", codex_plugin_metadata(replace(plugin, directory=empty)))
        (empty / "skills").symlink_to(plugin.directory / "skills", target_is_directory=True)
        self.assertEqual(codex_plugin_metadata(replace(plugin, directory=empty))["skills"], "./skills/")

    def test_source_root_namespace_and_catalog_inventory_order(self) -> None:
        self.write("ai-plugin.yml", "name: root-manifest\nversion: 1\ndescription: Root\n")
        self.write("skills/hub/SKILL.md", "body")
        source = discover_source(self.root)
        source = replace(source, plugins=tuple(reversed(source.plugins)))
        catalog = codex_marketplace_metadata(source)
        self.assertEqual([p["source"]["path"] for p in catalog["plugins"]],
                         ["./group/folder", "./"])
        result = render_file_result(
            "---\ndescription: Test\nargument-hint: x\n---\n",
            "skills/hub/SKILL.md", "codex", source,
        )
        self.assertEqual(result.content, "---\ndescription: 'Test. Usage: $"
                         + self.root.name + ":hub x.'\n---\n")
        self.assertIn(self.root.name + ":hub", codex_skill_names(source))
        self.assertNotIn("root-manifest:hub", codex_skill_names(source))


class IsolatedCodexTests(unittest.TestCase):
    def test_copied_plugin_runs_without_site_packages_or_source_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / "installed" / "ai-marketplace"
            shutil.copytree(Path(__file__).resolve().parents[5], plugin, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            cwd = root / "unrelated"
            cwd.mkdir()
            before = snapshot(root)
            program = textwrap.dedent(r'''
                import json, os, subprocess, sys, sysconfig
                from dataclasses import replace
                from pathlib import Path
                plugin = Path(sys.argv[1])
                stdlib = sysconfig.get_path('stdlib')
                sys.path[:] = [str(plugin / 'scripts'), stdlib,
                               os.path.join(stdlib, 'lib-dynload')]
                def forbidden(*args, **kwargs):
                    raise AssertionError('No Git or external processes')
                subprocess.run = forbidden
                subprocess.Popen = forbidden
                from marketplace.source import discover_source
                from marketplace.build.rendering import (
                    render_file_result, codex_plugin_metadata, codex_marketplace_metadata,
                )
                from marketplace.build import CodexConstructReport
                source = discover_source(plugin)
                source = replace(source, plugins=tuple(replace(p, manifest={
                    **p.manifest, 'version': '3.2.1'}) for p in source.plugins))
                result = render_file_result(
                    '---\ndescription: Internal\nargument-hint: [path]\n'
                    'disable-model-invocation: true\n---\n$ARGUMENTS',
                    'skills/ai-marketplace/SKILL.md', 'codex', source,
                )
                report = CodexConstructReport()
                report.add('skills/ai-marketplace/SKILL.md', '.', result.findings)
                assert report.total() == '1 unresolved construct(s) in 1 file(s)'
                assert result.extra_files == {'agents/openai.yaml':
                                             'policy:\n  allow_implicit_invocation: false\n'}
                assert 'yaml' not in sys.modules and 'bc' not in sys.modules
                print(json.dumps({'content': result.content,
                                  'plugin': codex_plugin_metadata(source.plugins[0]),
                                  'path': codex_marketplace_metadata(source)['plugins'][0]['source']['path']}))
            ''')
            env = {**os.environ, "PYTHONPATH": str(root / "missing")}
            result = subprocess.run(["python3", "-B", "-S", "-c", program, str(plugin)],
                                    cwd=cwd, env=env, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            self.assertEqual(data["content"], "---\ndescription: 'Internal. Usage: "
                             "$ai-marketplace:ai-marketplace [path].'\n---\n$ARGUMENTS")
            self.assertEqual(data["path"], "./")
            self.assertEqual(data["plugin"]["version"], "3.2.1")
            self.assertEqual(result.stderr, "")
            self.assertEqual(snapshot(root), before)
