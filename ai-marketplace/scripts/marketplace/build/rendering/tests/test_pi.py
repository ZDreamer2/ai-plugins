"""Pin strict Pi rendering and preflight through independent PHP expectations."""

import base64
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

from marketplace.build import PiConstructReport
from marketplace.build.rendering import (
    FileRendering, PiConstruct, pi_package_metadata, pi_plugin_metadata, preflight_pi,
    render_file, render_file_result,
)
from marketplace.source import discover_source, pi_skill_name

from .test_claude import snapshot


def skill(name: str = "sample", description: str = "Description", body: str = "Body") -> str:
    return f"---\nname: {name}\ndescription: {description}\n---\n{body}"


class PiTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = "folder/skills/sample/SKILL.md"
        self.write("folder/ai-plugin.yml", "name: manifest\nversion: 1.2.3\ndescription: Plugin\nhooks: [ignored]\n")
        self.write(self.path, skill())
        self.source = discover_source(self.root)

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode("utf-8", "surrogateescape"))

    def render(self, content: str) -> FileRendering:
        return render_file_result(content, self.path, "pi", self.source)

    def test_metadata_independent_packages_extensions_and_nested_values(self) -> None:
        for path in ("folder/extensions/z/index.ts", "folder/extensions/z/index.js",
                     "folder/extensions/a/index.mjs", "folder/extensions/a/other.js",
                     "other/extensions/sibling/index.ts"):
            self.write(path, "extension")
        self.write("other/ai-plugin.yml", "name: other\nversion: 2\ndescription: Other\n")
        self.source = discover_source(self.root)
        before = deepcopy(self.source)
        with patch("subprocess.run", side_effect=AssertionError("Git")), \
                patch("subprocess.Popen", side_effect=AssertionError("Git")):
            result = pi_package_metadata(self.source.plugins[0])
            identity = pi_plugin_metadata(self.source.plugins[0])
        self.assertEqual(result, {
            "name": "@zdreamer2/pi-plugin-manifest", "version": "1.2.3",
            "description": "Plugin", "keywords": ["pi-package"],
            "pi": {"skills": ["./skills/sample"], "extensions": [
                "./extensions/a/index.mjs", "./extensions/z/index.js", "./extensions/z/index.ts"]},
        })
        self.assertEqual(identity, {"name": "manifest", "version": "1.2.3"})
        result["pi"]["skills"].clear()
        result["pi"]["extensions"].clear()
        result["keywords"].clear()
        self.assertEqual(self.source, before)
        self.assertTrue(pi_package_metadata(self.source.plugins[0])["pi"]["skills"])
        no_skills = replace(self.source.plugins[1], extensions=())
        self.assertEqual(pi_package_metadata(no_skills)["pi"], {"skills": []})
        unusual = replace(no_skills, manifest={"name": "other", "version": [1], "description": {"x": [2]}})
        metadata = pi_package_metadata(unusual)
        metadata["version"].clear()
        metadata["description"]["x"].clear()
        identity = pi_plugin_metadata(unusual)
        identity["version"].clear()
        self.assertEqual(unusual.manifest["version"], [1])
        self.assertEqual(unusual.manifest["description"], {"x": [2]})

    def test_manifest_names_hubs_repeated_skills_grouped_and_source_root(self) -> None:
        self.write("folder/skills/manifest/SKILL.md", skill("manifest"))
        self.write("group/other/ai-plugin.yml", "name: other\nversion: 2\ndescription: Other\n")
        self.write("group/other/skills/sample/SKILL.md", skill())
        self.write("ai-plugin.yml", "name: root-plugin\nversion: 3\ndescription: Root\n")
        self.write("skills/root-plugin/SKILL.md", skill("root-plugin"))
        source = discover_source(self.root)
        preflight_pi(source)
        for path, name in ((self.path, "manifest-sample"),
                           ("folder/skills/manifest/SKILL.md", "manifest"),
                           ("group/other/skills/sample/SKILL.md", "other-sample"),
                           ("skills/root-plugin/SKILL.md", "root-plugin")):
            content = (self.root / path).read_text()
            self.assertIn("name: " + name + "\n", render_file(content, path, "pi", source))
        self.assertEqual(pi_package_metadata(source.plugins[0])["pi"]["skills"], ["./skills/root-plugin"])
        self.assertEqual(render_file("${AGENT_SKILL(manifest)} ${AGENT_SKILL(manifest:sample)}", "README.md", "pi", source),
                         "/skill:manifest /skill:manifest-sample")
        for invocation in ("folder", "folder:sample", "missing", "manifest:missing"):
            with self.assertRaisesRegex(ValueError, "does not name a published Pi skill"):
                render_file("${AGENT_SKILL(" + invocation + ")}", "README.md", "pi", source)

    def test_supported_key_order_nulls_odd_types_and_body_bytes(self) -> None:
        content = ("---\nname: sample\ndescription: 'Unicode é🙂: quote'\n"
                   "allowed-tools: [Bash, Read]\nmetadata: {a: {b: [{c: [one, two]}]}}\n"
                   "compatibility: null\nlicense: 12\ndisable-model-invocation: odd\n"
                   "argument-hint: ignored\nuser-invocable: false\nmodel: sonnet\n---\n"
                   "\r\nUnchanged \udcff body\r\nfinal")
        expected = ("---\nname: manifest-sample\ndescription: 'Unicode é🙂: quote'\n"
                    "disable-model-invocation: odd\nlicense: 12\ncompatibility: null\n"
                    "metadata:\n  a:\n    b:\n      - { c: [one, two] }\n"
                    "allowed-tools:\n  - Bash\n  - Read\n---\n\r\nUnchanged \udcff body\r\nfinal")
        result = self.render(content)
        self.assertEqual(result.content, expected)
        self.assertEqual(result.extra_files, {})
        self.assertEqual(result.findings, [])
        self.assertEqual(render_file(content, self.path, "pi", self.source), expected)
        for value in ("null", "false", "0", "[x]", "{a: b}"):
            result = self.render(skill().replace("---\nBody", f"disable-model-invocation: {value}\n---\nBody"))
            self.assertIn("disable-model-invocation:", result.content)
            self.assertEqual(result.extra_files, {})

    def test_strict_validation_order_and_complete_delimiters(self) -> None:
        cases = [
            ("", "has no complete YAML frontmatter"),
            ("\ufeff" + skill(), "has no complete YAML frontmatter"),
            (skill().replace("\n", "\r\n"), "has no complete YAML frontmatter"),
            ("---\nname: sample\n---", "has no complete YAML frontmatter"),
            (skill(body=""), "has no instructions after its frontmatter"),
            ("---\nname: [broken\n---\n \t\r\n\0\v", "has no instructions after its frontmatter"),
            ("---\nname: [broken\n---\nBody", "has malformed YAML frontmatter:"),
            ("---\n\n---\nBody", "must have a non-empty frontmatter mapping"),
            ("---\nscalar\n---\nBody", "must have a non-empty frontmatter mapping"),
            ("---\n[]\n---\nBody", "must have a non-empty frontmatter mapping"),
            ("---\n[x]\n---\nBody", "must define name 'sample'"),
            ("---\ndescription: Text\n---\nBody", "must define name 'sample'"),
            (skill("other", "null"), "defines name 'other', but its inventoried directory names it 'sample'"),
        ]
        for name in ("null", "false", "0", "[]", "{}", "''"):
            cases.append((skill().replace("name: sample", "name: " + name), "must define name 'sample'"))
        for description in ("null", "false", "0", "[]", "{}", "''", '" \\t\\r\\n\\0\\v"'):
            cases.append((skill(description=description), "must define a non-empty string description"))
        cases.append(("---\nname: sample\n---\nBody", "must define a non-empty string description"))
        cases.append((skill(description="'" + "🙂" * 1025 + "'"), "has a description longer than 1024 characters"))
        for content, reason in cases:
            with self.subTest(content=content[:100]), self.assertRaises(ValueError) as error:
                self.render(content)
            self.assertTrue(str(error.exception).startswith(f"Pi skill '{self.path}' {reason}"), str(error.exception))
        self.assertIn("🙂" * 1024, self.render(skill(description="'" + "🙂" * 1024 + "'")).content)
        for whitespace in ("\u2003", "\u00a0", "\u1680", "\f"):
            description = '"\\f"' if whitespace == "\f" else "'" + whitespace + "'"
            self.assertTrue(self.render(skill(description=description, body=whitespace)).content)
        self.assertIn("name: manifest-sample\n", self.render(skill().replace("name: sample", "name: !!binary c2FtcGxl")).content)

    def test_saved_php_binary_and_nested_yaml_oracles(self) -> None:
        oracle = json.loads(Path(__file__).with_name("pi_oracle.json").read_text())
        for case in oracle["binary"] + oracle["text"]:
            with self.subTest(case=case.get("hex", case.get("label"))):
                self.assert_oracle(case, case["source"])
        for case in oracle["boundaries"]:
            description = bytes.fromhex(case["hex"]) * case["repeat"] + b"A" * case["ascii_suffix"]
            content = skill(description="!!binary " + base64.b64encode(description).decode())
            with self.subTest(hex=case["hex"], repeat=case["repeat"], suffix=case["ascii_suffix"]):
                self.assert_oracle(case, content)

    def assert_oracle(self, case: dict, content: str) -> None:
        self.write(self.path, content)
        before = snapshot(self.root)
        if "error" in case:
            with self.assertRaises(ValueError) as error:
                self.render(content)
            self.assertEqual(str(error.exception), case["error"])
            with self.assertRaisesRegex(ValueError, "Pi skill"):
                preflight_pi(self.source)
        else:
            self.assertEqual(self.render(content).content, case["rendered"])
            preflight_pi(self.source)
        self.assertEqual(snapshot(self.root), before)

    def test_name_limits_pattern_and_inventory_order_before_reads(self) -> None:
        for name, valid, reason in (("a" * 64, True, ""), ("a" * 65, False, "64-character"),
                                    ("abc-123", True, ""), ("abc\n", True, ""),
                                    ("Bad", False, "invalid name"), ("-a", False, "invalid name"),
                                    ("a-", False, "invalid name"), ("a--b", False, "invalid name"),
                                    ("é" * 33, False, "64-character"), ("a_b", False, "invalid name")):
            # Hub names isolate the actual published name, including PHP's final LF anchor.
            plugin = replace(self.source.plugins[0], manifest={"name": name}, skills=("skills/" + name,))
            source = replace(self.source, plugins=(plugin,))
            with self.subTest(name=name), patch.object(Path, "read_bytes", side_effect=OSError("read reached")):
                if valid:
                    with self.assertRaisesRegex(OSError, "read reached"):
                        preflight_pi(source)
                else:
                    with self.assertRaisesRegex(ValueError, reason):
                        preflight_pi(source)
        first = self.source.plugins[0]
        invalid = replace(first, root="later", manifest={"name": "INVALID"})
        with patch.object(Path, "read_bytes", side_effect=AssertionError("Names first")):
            with self.assertRaisesRegex(ValueError, "later/skills/sample/SKILL.md.*invalid name"):
                preflight_pi(replace(self.source, plugins=(first, invalid)))
        hub = replace(first, root="hub", manifest={"name": "manifest-sample"}, skills=("skills/manifest-sample",))
        with patch.object(Path, "read_bytes", side_effect=AssertionError("Names first")):
            with self.assertRaises(ValueError) as error:
                preflight_pi(replace(self.source, plugins=(first, hub)))
        self.assertEqual(str(error.exception), "Pi skills 'folder/skills/sample/SKILL.md' and 'hub/skills/manifest-sample/SKILL.md' render to the same name 'manifest-sample'.")
        preflight_pi(replace(self.source, plugins=()))
        preflight_pi(replace(self.source, plugins=(replace(first, skills=(), manifest={}),)))

    def test_includes_placeholders_selection_scanning_and_read_only_preflight(self) -> None:
        self.write("folder/docs/pi.md", "Body ${AGENT_SKILL(manifest:sample)} $ARGUMENTS\r\n")
        self.write("folder/docs/other.md", "Other-host text ${AGENT_SKILL(absent)}\n")
        content = ("---\nname: sample\ndescription: ${AGENT_SUBAGENT_TOOL}\n"
                   "model: AskUserQuestion\nallowed-tools: spawn_agent\n---\n"
                   "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/other.md)}\n"
                   "${AGENT_INCLUDE_DOC_FOR(pi, ../../docs/pi.md)}\n")
        self.write(self.path, content)
        self.write("output/pi/sentinel", "Keep")
        (self.root / self.path).chmod(0o751)
        (self.root / "folder/docs/link.md").symlink_to("pi.md")
        before = snapshot(self.root)
        with patch("subprocess.run", side_effect=AssertionError("Git")):
            preflight_pi(self.source)
        result = self.render(content)
        self.assertEqual(result.content, "---\nname: manifest-sample\ndescription: subagent\nallowed-tools: spawn_agent\n---\nBody /skill:manifest-sample $ARGUMENTS\r\n")
        self.assertEqual([(f.category, f.line, f.text) for f in result.findings], [
            (PiConstruct.HOST_TOOL, 4, "spawn_agent"), (PiConstruct.HOST_VARIABLE, 6, "$ARGUMENTS")])
        self.assertEqual(result.extra_files, {})
        result.findings.clear()
        result.extra_files["invented"] = "x"
        self.assertTrue(self.render(content).findings)
        self.assertEqual(self.render(content).extra_files, {})
        self.assertEqual(snapshot(self.root), before)
        for path in ("README.md", "folder/skills/absent/SKILL.md", "folder/skills/sample/docs/SKILL.md", "folder/@common/docs/meta.md"):
            result = render_file_result("malformed AskUserQuestion", path, "pi", self.source)
            self.assertEqual(result.content, "malformed AskUserQuestion")
            self.assertEqual([f.text for f in result.findings], ["AskUserQuestion"])
        for path in ("README.MD", "script", "data.json"):
            result = render_file_result("${AGENT_BAD}", path, "pi", self.source)
            self.assertEqual(result.content, "${AGENT_BAD}")
            self.assertEqual(result.findings, [])
        self.write(self.path, skill(body="${AGENT_BAD}"))
        before = snapshot(self.root)
        with self.assertRaisesRegex(ValueError, "names no placeholder"):
            preflight_pi(self.source)
        self.assertEqual(snapshot(self.root), before)

    def test_every_skill_read_in_inventory_order(self) -> None:
        self.write("folder/skills/second/SKILL.md", skill("second", body="${AGENT_BAD}"))
        self.write("folder/skills/third/SKILL.md", "malformed")
        source = discover_source(self.root)
        before = snapshot(self.root)
        with self.assertRaisesRegex(ValueError, "second/SKILL.md.*names no placeholder"):
            preflight_pi(source)
        self.write("folder/skills/second/SKILL.md", skill("second"))
        with self.assertRaisesRegex(ValueError, "third/SKILL.md.*has no complete"):
            preflight_pi(source)
        self.write("folder/skills/second/SKILL.md", skill("second", body="${AGENT_BAD}"))
        self.assertEqual(snapshot(self.root), before)

    def test_nested_manifest_preserves_inventoried_preflight_owner(self) -> None:
        self.write("folder/skills/sample/ai-plugin.yml",
                   "name: nested\nversion: 2\ndescription: Nested\n")
        self.write(self.path, "Malformed skill")
        self.write("output/pi/sentinel", "Keep")
        source = discover_source(self.root)
        self.assertEqual(len(source.plugins), 2)
        self.assertEqual(source.plugins[0].skills, ("skills/sample",))
        self.assertEqual(pi_skill_name(source.plugins[0], "skills/sample/SKILL.md"),
                         "manifest-sample")
        before = snapshot(self.root)
        # Ordinary tree rendering still uses the nearest manifest; preflight
        # must validate every entry under the owner that inventories it.
        self.assertEqual(render_file("Malformed skill", self.path, "pi", source),
                         "Malformed skill")
        with self.assertRaisesRegex(ValueError, "folder/skills/sample/SKILL.md.*has no complete"):
            preflight_pi(source)
        self.assertEqual(snapshot(self.root), before)
        self.write(self.path, skill("wrong"))
        with self.assertRaisesRegex(ValueError, "inventoried directory names it 'sample'"):
            preflight_pi(source)
        self.write("folder/docs/parent.md", "${AGENT_SKILL(manifest:sample)} $CODEX_HOME\n")
        content = skill(body="${AGENT_INCLUDE_DOC_FOR(pi, ../../docs/parent.md)}\n")
        self.write(self.path, content)
        before = snapshot(self.root)
        preflight_pi(source)
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(render_file(content, self.path, "pi", source),
                         skill(body="/skill:manifest-sample $CODEX_HOME\n"))


class IsolatedPiTests(unittest.TestCase):
    def test_copied_plugin_with_only_bundled_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / "installed/ai-marketplace"
            shutil.copytree(Path(__file__).resolve().parents[5], plugin, symlinks=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            cwd = root / "unrelated"
            cwd.mkdir()
            before = snapshot(root)
            program = textwrap.dedent(r'''
                import os, subprocess, sys, sysconfig
                from pathlib import Path
                from dataclasses import replace
                plugin = Path(sys.argv[1])
                stdlib = sysconfig.get_path('stdlib')
                sys.path[:] = [str(plugin / 'scripts'), stdlib, os.path.join(stdlib, 'lib-dynload')]
                def forbidden(*args, **kwargs):
                    raise AssertionError('No external processes')
                subprocess.run = subprocess.Popen = forbidden
                from marketplace.source import discover_source
                from marketplace.build.rendering import (
                    preflight_pi, pi_package_metadata, pi_plugin_metadata, render_file_result, scan_pi,
                )
                from marketplace.build import PiConstructReport
                source = discover_source(plugin)
                source = replace(source, plugins=tuple(replace(p, manifest={**p.manifest, 'version': '3.2.1'}) for p in source.plugins))
                preflight_pi(source)
                result = render_file_result('---\nname: ai-marketplace\ndescription: Work\n---\n$CODEX_HOME',
                                            'skills/ai-marketplace/SKILL.md', 'pi', source)
                assert result.content == '---\nname: ai-marketplace\ndescription: Work\n---\n$CODEX_HOME'
                assert result.extra_files == {}
                assert result.findings == scan_pi(result.content, source)
                report = PiConstructReport()
                report.add('skills/ai-marketplace/SKILL.md', '.', result.findings)
                assert report.total() == '1 unresolved construct(s) in 1 file(s)'
                assert report.render().startswith('# Unresolved host constructs in the Pi tree\n')
                assert pi_package_metadata(source.plugins[0])['name'] == '@zdreamer2/pi-plugin-ai-marketplace'
                assert pi_plugin_metadata(source.plugins[0]) == {'name': 'ai-marketplace', 'version': '3.2.1'}
                assert 'yaml' not in sys.modules and 'bc' not in sys.modules
            ''')
            result = subprocess.run(["python3", "-B", "-S", "-c", program, str(plugin)],
                                    cwd=cwd, env={**os.environ, "PYTHONPATH": str(root / "missing")},
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")
            self.assertEqual(snapshot(root), before)
