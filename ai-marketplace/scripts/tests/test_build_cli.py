"""Exercise a copied plugin from an unrelated directory without site packages."""

import base64
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class BuildCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plugin = self.root / "installed"
        original = Path(__file__).resolve().parents[2]
        shutil.copytree(original, self.plugin, symlinks=True,
                        ignore=shutil.ignore_patterns("__pycache__"))
        self.command = self.plugin / "scripts/build.py"
        self.cwd = self.root / "unrelated"
        self.cwd.mkdir()
        self.source = self.root / "source"
        self.source.mkdir()
        self.write("group/demo/ai-plugin.yml", b"description: Demo\nversion: '1.0'\n")
        self.write("group/demo/skills/run/SKILL.md", b"---\nname: run\ndescription: Run\ndisable-model-invocation: true\n---\nUse ${AGENT_SUBAGENT_TOOL}.\n")
        self.write("group/demo/bin/tool", b"#!/bin/sh\n", 0o755)

    def write(self, path: str, content: bytes, mode: int = 0o644) -> None:
        target = self.source / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        target.chmod(mode)

    def run_cli(self, *args: str, direct: bool = False) -> subprocess.CompletedProcess:
        return self.run_tool(self.command, *args, direct=direct)

    def run_tool(self, command: Path, *args: str, direct: bool = False) -> subprocess.CompletedProcess:
        prefix = [str(command)] if direct else [sys.executable, "-B", "-S", str(command)]
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        return subprocess.run(prefix + list(args), cwd=self.cwd, env=environment,
                              capture_output=True, text=True, timeout=30)

    def snapshot(self, root: Path, excluded: Path | None = None) -> dict:
        return {
            path.relative_to(root): (
                path.lstat().st_mode,
                os.readlink(path) if path.is_symlink()
                else path.read_bytes() if path.is_file() else None,
            )
            for path in root.rglob("*")
            if excluded is None or not path.is_relative_to(excluded)
        }

    def test_help_and_missing_arguments(self) -> None:
        help_result = self.run_cli("--help")
        self.assertEqual(0, help_result.returncode, help_result.stderr)
        for option in ("--dir", "--output-dir", "--dry-run"):
            self.assertIn(option, help_result.stdout)
        missing = self.run_cli()
        self.assertNotEqual(0, missing.returncode)
        self.assertIn("--dir", missing.stderr)

    def test_default_build_is_standalone_and_preserves_source(self) -> None:
        before = {p.relative_to(self.source): p.read_bytes() for p in self.source.rglob("*") if p.is_file()}
        result = self.run_cli("--dir", str(self.source))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Building 1 plugin(s)", result.stdout)
        output = self.source / "@build"
        for host in ("claude", "codex", "pi"):
            self.assertIn(f"{host}: 2 source file(s)", result.stdout)
            script = output / host / "group/demo/bin/tool"
            self.assertEqual(0o755, script.stat().st_mode & 0o777)
        self.assertIn("policy.allow_implicit_invocation: false", result.stdout)
        self.assertIn("codex-report.md", result.stdout)
        self.assertIn("pi-report.md", result.stdout)
        self.assertTrue((output / "codex/group/demo/skills/run/agents/openai.yaml").is_file())
        self.assertIn(b"name: demo-run", (output / "pi/group/demo/skills/run/SKILL.md").read_bytes())
        for path, content in before.items():
            self.assertEqual(content, (self.source / path).read_bytes())
        self.assertFalse(list(self.plugin.rglob("__pycache__")))

    def test_custom_relative_output_and_direct_execution_without_bytecode(self) -> None:
        result = self.run_cli("--dir", "../source", "--output-dir", "generated/output", direct=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.cwd / "generated/output/pi/group/demo/package.json").is_file())
        self.assertFalse((self.source / "@build").exists())
        self.assertFalse(list(self.plugin.rglob("__pycache__")))
        self.assertEqual(0o755, self.command.stat().st_mode & 0o777)

    def test_dry_run_narrates_without_writes(self) -> None:
        output = self.root / "preview"
        result = self.run_cli("--dir", str(self.source), "--output-dir", str(output), "--dry-run")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertFalse(output.exists())
        self.assertIn("[dry-run] pi/group/demo/package.json: 1.0", result.stdout)
        self.assertTrue(all(line.startswith("[dry-run]") for line in result.stdout.splitlines()))

    def test_build_failures_have_context_and_nonzero_exit(self) -> None:
        missing = self.run_cli("--dir", str(self.root / "absent"))
        self.assertNotEqual(0, missing.returncode)
        self.assertIn("Build failed:", missing.stderr)
        self.write("group/demo/ai-plugin.yml", b"version: '1.0'\n")
        invalid = self.run_cli("--dir", str(self.source))
        self.assertNotEqual(0, invalid.returncode)
        self.assertIn("group/demo", invalid.stderr)
        self.assertIn("description", invalid.stderr)
        self.assertFalse((self.source / "@build").exists())

    def test_installers_are_claude_only_and_narrated(self) -> None:
        self.write_installer_sources()
        preview = self.run_cli("--dir", str(self.source), "--dry-run")
        self.assertEqual(0, preview.returncode, preview.stderr)
        self.assertIn("claude/@setup/install.sh:", preview.stdout)
        self.assertFalse((self.source / "@build").exists())
        result = self.run_cli("--dir", str(self.source))
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("byte(s)", result.stdout)
        self.assert_installer_output(self.source / "@build")

    def write_installer_sources(self) -> None:
        base = "@common/@setup-sources/"
        markers = b"# === BUNDLE_REPLACE_BEGIN ===\nold\n# === BUNDLE_REPLACE_END ===\n"
        self.write(base + "install.sh", b"#!/bin/sh\n__INSTALLER_VERSION__\n" + markers)
        self.write(base + "install.ps1", b"__INSTALLER_VERSION__\n" + markers)
        self.write(base + "setup.py", b'STATUS_LINE_B64 = "__STATUS_LINE_PLACEHOLDER__"\nSETTINGS_B64 = "__SETTINGS_PLACEHOLDER__"\n')
        self.write(base + "status-line.py", b"status\n")
        self.write(base + "settings.json", b"{}\n")

    def assert_installer_output(self, output: Path) -> None:
        self.assertEqual(0o755, (output / "claude/@setup/install.sh").stat().st_mode & 0o777)
        powershell = output / "claude/@setup/install.ps1"
        self.assertEqual(0o644, powershell.stat().st_mode & 0o777)
        self.assertTrue(powershell.read_bytes().startswith(b"\xef\xbb\xbf"))
        for name in ("install.sh", "install.ps1"):
            content = (output / "claude/@setup" / name).read_bytes()
            self.assertIn(base64.b64encode(b"status\n"), content)
            self.assertIn(base64.b64encode(b"{}\n"), content)
            self.assertNotIn(b"__INSTALLER_VERSION__", content)
            self.assertNotIn(b"BUNDLE_REPLACE_BEGIN", content)
        self.assertFalse((output / "codex/@setup").exists())
        self.assertFalse((output / "pi/@setup").exists())

    def test_build_composes_with_independent_validator(self) -> None:
        result = self.run_cli("--dir", str(self.source))
        self.assertEqual(0, result.returncode, result.stderr)
        validator = self.plugin / "scripts/validate_pi.py"
        output = self.source / "@build/pi"
        before = self.snapshot(self.source)
        valid = self.run_tool(validator, "--dir", str(self.source), "--tree", str(output))
        self.assertEqual(0, valid.returncode, valid.stderr)
        self.assertEqual("Validated 1 independent Pi packages.\n", valid.stdout)
        self.assertEqual(before, self.snapshot(self.source))
        (output / "group/demo/bin/tool").write_bytes(b"stale\n")
        damaged = self.snapshot(self.source)
        invalid = self.run_tool(validator, "--dir", str(self.source), "--tree", str(output))
        self.assertEqual(1, invalid.returncode)
        self.assertIn("Pi publication preflight failed:", invalid.stderr)
        self.assertIn("group/demo/bin/tool", invalid.stderr)
        self.assertEqual(damaged, self.snapshot(self.source))

    def test_source_checkout_and_generated_plugin_tools_are_standalone(self) -> None:
        checkout_plugin = self.source / "ai/ai-marketplace"
        checkout_plugin.mkdir(parents=True)
        shutil.copytree(self.plugin / "scripts", checkout_plugin / "scripts")
        (checkout_plugin / "ai-plugin.yml").write_text(
            "name: ai-marketplace\ndescription: Marketplace tools\nversion: '1.0'\n"
        )
        self.write_installer_sources()
        before = self.snapshot(self.source)
        first_output = self.source / "@build"
        first = self.run_tool(checkout_plugin / "scripts/build.py", "--dir", str(self.source))
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertIn("Building 2 plugin(s)", first.stdout)
        for host in ("claude", "codex", "pi"):
            self.assertEqual(b"#!/bin/sh\n", (first_output / host / "group/demo/bin/tool").read_bytes())
            self.assertTrue((first_output / host / "ai/ai-marketplace/scripts/build.py").is_file())
            self.assertFalse((first_output / host / "ai/ai-marketplace/ai-plugin.yml").exists())
        self.assert_installer_output(first_output)
        self.assertEqual(before, self.snapshot(self.source, first_output))

        installed_scripts = first_output / "pi/ai/ai-marketplace/scripts"
        generated_before = self.snapshot(first_output)
        first_valid = self.run_tool(installed_scripts / "validate_pi.py", "--dir", str(self.source),
                                    "--tree", str(first_output / "pi"))
        self.assertEqual(0, first_valid.returncode, first_valid.stderr)
        self.assertEqual("Validated 2 independent Pi packages.\n", first_valid.stdout)

        separate_source = self.root / "separate-source"
        separate_source.mkdir()
        shutil.copytree(self.source / "group", separate_source / "group")
        shutil.copytree(self.source / "@common", separate_source / "@common")
        separate_before = self.snapshot(separate_source)
        second_output = self.cwd / "generated"
        second = self.run_tool(installed_scripts / "build.py", "--dir", str(separate_source),
                               "--output-dir", "generated")
        self.assertEqual(0, second.returncode, second.stderr)
        self.assert_installer_output(second_output)
        second_valid = self.run_tool(installed_scripts / "validate_pi.py", "--dir", str(separate_source),
                                     "--tree", "generated/pi", "--output-dir", "generated")
        self.assertEqual(0, second_valid.returncode, second_valid.stderr)
        self.assertEqual("Validated 1 independent Pi packages.\n", second_valid.stdout)
        self.assertEqual(separate_before, self.snapshot(separate_source))
        self.assertEqual(before, self.snapshot(self.source, first_output))
        self.assertEqual(generated_before, self.snapshot(first_output))
        self.assertFalse(list(self.root.rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
