"""Check the inspection CLI using artifacts authored independently of building."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class ValidatePiCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.plugin = self.root / "installed"
        original = Path(__file__).resolve().parents[2]
        shutil.copytree(original, self.plugin, symlinks=True,
                        ignore=shutil.ignore_patterns("@common", "__pycache__"))
        self.command = self.plugin / "scripts/validate_pi.py"
        self.cwd = self.root / "unrelated"
        self.cwd.mkdir()
        self.source = self.root / "source"
        self.tree = self.root / "downloaded"
        self.source.mkdir()
        self.tree.mkdir()
        for root in ("group/demo", "other"):
            source = self.source / root
            package = self.tree / root
            (source / "skills/run").mkdir(parents=True)
            (package / "skills/run").mkdir(parents=True)
            (package / ".pi-plugin").mkdir()
            (source / "ai-plugin.yml").write_text("description: Demo\n")
            (source / "skills/run/SKILL.md").write_text("Source skill\n")
            (package / "skills/run/SKILL.md").write_text("Changed rendered skill\n")
            (package / "package.json").write_text(json.dumps({
                "name": "@zdreamer2/pi-plugin-" + source.name,
                "version": "1.0", "description": "Demo",
                "pi": {"skills": ["./skills/run"]},
            }))
            (package / ".pi-plugin/plugin.json").write_text(json.dumps({
                "name": source.name, "version": "1.0",
            }))

    def run_cli(self, *args: str, direct: bool = False) -> subprocess.CompletedProcess:
        prefix = [str(self.command)] if direct else [sys.executable, "-B", "-S", str(self.command)]
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        return subprocess.run(prefix + list(args), cwd=self.cwd, env=environment,
                              capture_output=True, text=True, timeout=20)

    def snapshot(self) -> dict:
        return {
            path.relative_to(self.root): (
                path.lstat().st_mode,
                os.readlink(path) if path.is_symlink()
                else path.read_bytes() if path.is_file() else None,
            )
            for path in self.root.rglob("*")
        }

    def test_help_and_required_arguments(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(0, result.returncode, result.stderr)
        for flag in ("--dir", "--tree", "--output-dir"):
            self.assertIn(flag, result.stdout)
        for args in ((), ("--dir", str(self.source)), ("--tree", str(self.tree))):
            with self.subTest(args=args):
                missing = self.run_cli(*args)
                self.assertEqual(2, missing.returncode)
                self.assertIn("required", missing.stderr)
                self.assertEqual("", missing.stdout)

    def test_success_is_standalone_and_read_only(self) -> None:
        before = self.snapshot()
        result = self.run_cli("--dir", "../source", "--tree", "../downloaded", direct=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("Validated 2 independent Pi packages.\n", result.stdout)
        self.assertEqual("", result.stderr)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(0o755, self.command.stat().st_mode & 0o777)

    def test_failures_use_stderr_and_preserve_inputs(self) -> None:
        metadata = self.tree / "group/demo/package.json"
        for content in (b"{", b'{"name":"wrong"}', b'"not metadata"', b'\xff'):
            with self.subTest(content=content):
                metadata.write_bytes(content)
                before = self.snapshot()
                result = self.run_cli("--dir", str(self.source), "--tree", str(self.tree))
                self.assertEqual(1, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertTrue(result.stderr.startswith("Pi publication preflight failed: "))
                self.assertIn("group/demo", result.stderr)
                self.assertEqual(before, self.snapshot())
        missing = self.run_cli("--dir", str(self.root / "absent"), "--tree", str(self.tree))
        self.assertEqual(1, missing.returncode)
        self.assertIn("absent", missing.stderr)

    def test_unreadable_metadata_is_contextual(self) -> None:
        # Inject only the read failure: root privileges can bypass chmod here.
        probe = '''
import runpy, sys
from pathlib import Path
from unittest.mock import patch
command = sys.argv.pop(1)
sys.path.insert(0, str(Path(command).parent))
original = Path.read_bytes
def read(path):
    if path.name == 'package.json':
        raise PermissionError('unreadable injected metadata: ' + str(path))
    return original(path)
with patch.object(Path, 'read_bytes', read):
    runpy.run_path(command, run_name='__main__')
'''
        before = self.snapshot()
        environment = os.environ.copy()
        environment.pop("PYTHONPATH", None)
        result = subprocess.run([
            sys.executable, "-B", "-S", "-c", probe, str(self.command),
            "--dir", str(self.source), "--tree", str(self.tree),
        ], cwd=self.cwd, env=environment, capture_output=True, text=True, timeout=20)
        self.assertEqual(1, result.returncode)
        self.assertTrue(result.stderr.startswith("Pi publication preflight failed: "))
        self.assertIn("package.json", result.stderr)
        self.assertEqual(before, self.snapshot())

    def test_custom_nested_output_and_relocated_tree(self) -> None:
        output = self.source / "group/demo/generated"
        (output / "ghost/skills/run").mkdir(parents=True)
        (output / "ghost/ai-plugin.yml").write_text("description: Generated\n")
        (output / "ghost/skills/run/SKILL.md").write_text("Generated\n")
        (self.source / "group/demo/output-alias").symlink_to(output, target_is_directory=True)
        (self.source / "manifest-alias").mkdir()
        (self.source / "manifest-alias/ai-plugin.yml").symlink_to(output / "ghost/ai-plugin.yml")
        before = self.snapshot()
        result = self.run_cli("--dir", "../source", "--tree", "../downloaded",
                              "--output-dir", "../source/group/demo/generated")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("Validated 2 independent Pi packages.\n", result.stdout)
        self.assertEqual(before, self.snapshot())
        default = self.run_cli("--dir", "../source", "--tree", "../downloaded")
        self.assertEqual(1, default.returncode)
        self.assertEqual(before, self.snapshot())


if __name__ == "__main__":
    unittest.main()
