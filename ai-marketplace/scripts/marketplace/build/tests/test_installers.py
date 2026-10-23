"""Installer byte contracts exercised through complete marketplace builds."""

import stat
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from marketplace.build import build


_BOM = b"\xef\xbb\xbf"
_BEGIN = b"# === BUNDLE_REPLACE_BEGIN ==="
_END = b"# === BUNDLE_REPLACE_END ==="
_VERSION = b"__INSTALLER_VERSION__"
_NOW = datetime(2026, 9, 30, 22, 34, 59, tzinfo=timezone.utc)
_STAMP = b"26.10.010134"
_STATUS_ASSIGNMENT = b'STATUS_LINE_B64 = "__STATUS_LINE_PLACEHOLDER__"'
_SETTINGS_ASSIGNMENT = b'SETTINGS_B64 = "__SETTINGS_PLACEHOLDER__"'
_SETUP = (
    b"# \xc3\xa9\r\n"
    + _STATUS_ASSIGNMENT + b"\r\n"
    + _SETTINGS_ASSIGNMENT + b"\r\n"
    + b"# __STATUS_LINE_PLACEHOLDER__ __SETTINGS_PLACEHOLDER__\r\n"
)
_SECOND_BLOCK = _BEGIN + b"\r\nsecond span stays\r\n" + _END
_SHELL_SOURCE = (
    b"#!/bin/sh\r\nversion=" + _VERSION + b"\r\n"
    + _BEGIN + b"\r\nfirst span\r\n" + _END + b"\r\n"
    + _SECOND_BLOCK + b"\r\nlast=" + _VERSION + b"\r\n"
)
_PS_SOURCE = (
    b"# \xc3\xa9\r\nversion=" + _VERSION + b"\r\n"
    + _BEGIN + b"\r\nfirst span\r\n" + _END + b"\r\n"
    + _SECOND_BLOCK + b"\r\nlast=" + _VERSION + b"\r\n"
)
_BUNDLED_PYTHON = (
    b"# \xc3\xa9\r\n"
    b'STATUS_LINE_B64 = "IyDDqQ0KcHJpbnQoJ/8nKQ0K"\r\n'
    b'SETTINGS_B64 = "ew0KCSJsYWJlbCI6ICLDqSINCn0NCg=="\r\n'
    b"# __STATUS_LINE_PLACEHOLDER__ __SETTINGS_PLACEHOLDER__\r\n"
)
_EXPECTED_SH = (
    b"#!/bin/sh\r\nversion=26.10.010134\r\n"
    b"_py_tmpfile=$(mktemp /tmp/bc_setup_XXXXXX.py)\n"
    b"cat > \"$_py_tmpfile\" << '__BUNDLED_PY_END__'\n"
    + _BUNDLED_PYTHON
    + b"\n__BUNDLED_PY_END__\n"
    b"PY_ARGS=()\n"
    b'[ "$AUTO_YES" = "true" ] && PY_ARGS+=("-y")\n'
    b'python3 "$_py_tmpfile" "${PY_ARGS[@]}"\n'
    b'rm -f "$_py_tmpfile"\r\n'
    + _SECOND_BLOCK + b"\r\nlast=26.10.010134\r\n"
)
_EXPECTED_PS = (
    _BOM + b"# \xc3\xa9\r\nversion=26.10.010134\r\n"
    b"$pyCode = @'\n"
    + _BUNDLED_PYTHON
    + b"\n'@\n\n"
    b"$tempFile = New-TemporaryFile\n"
    b"$pyCode | Set-Content -Path $tempFile -Encoding utf8\n\n"
    b"try {\n"
    b"\t$pyArgs = @()\n"
    b'\tif ($Yes) { $pyArgs += "-y" }\n'
    b"\t& $python $tempFile @pyArgs\n"
    b"} finally {\n"
    b"\tRemove-Item $tempFile -ErrorAction SilentlyContinue\n"
    b"}\r\n"
    + _SECOND_BLOCK + b"\r\nlast=26.10.010134\r\n"
)


class InstallersTest(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "source"
        self.source.mkdir()
        self.output = self.root / "output"
        self.sources = self.source / "@common" / "@setup-sources"

    def write_sources(self, overrides: dict[str, bytes] | None = None) -> None:
        sources = {
            "install.sh": _SHELL_SOURCE,
            "install.ps1": _PS_SOURCE,
            "setup.py": _SETUP,
            "status-line.py": b"# \xc3\xa9\r\nprint('\xff')\r\n",
            "settings.json": b'{\r\n\t"label": "\xc3\xa9"\r\n}\r\n',
        }
        sources.update(overrides or {})
        self.sources.mkdir(parents=True, exist_ok=True)
        for name, content in sources.items():
            (self.sources / name).write_bytes(content)

    def run_build(self, dry_run: bool = False):
        return build(self.source, self.output, dry_run, now=_NOW)

    def test_exact_bytes_sizes_modes_and_claude_only_destinations(self) -> None:
        for bom in (b"", _BOM):
            with self.subTest(source_bom=bool(bom)):
                self.write_sources({"install.ps1": bom + _PS_SOURCE})
                before = {
                    path.name: path.read_bytes() for path in self.sources.iterdir()
                }
                result = self.run_build()
                self.assertEqual(result.output_dir, self.output)
                self.assertEqual(result.installers, {
                    "install.sh": len(_EXPECTED_SH),
                    "install.ps1": len(_EXPECTED_PS),
                })
                setup = self.output / "claude" / "@setup"
                self.assertEqual((setup / "install.sh").read_bytes(), _EXPECTED_SH)
                self.assertEqual((setup / "install.ps1").read_bytes(), _EXPECTED_PS)
                self.assertEqual(stat.S_IMODE((setup / "install.sh").stat().st_mode), 0o755)
                self.assertEqual(stat.S_IMODE((setup / "install.ps1").stat().st_mode), 0o644)
                self.assertEqual(stat.S_IMODE(setup.stat().st_mode), 0o755)
                self.assertEqual(
                    sorted(path.relative_to(self.output).as_posix()
                           for path in self.output.rglob("*") if path.is_file()),
                    ["claude/@setup/install.ps1", "claude/@setup/install.sh"],
                )
                self.assertEqual(before, {
                    path.name: path.read_bytes() for path in self.sources.iterdir()
                })

    def test_absent_sources_skip_bundling_and_preserve_existing_output(self) -> None:
        self.assertEqual(self.run_build().installers, {})
        self.assertFalse(self.output.exists())
        self.output.mkdir()
        sentinel = self.output / "existing"
        sentinel.write_bytes(b"keep")
        self.assertEqual(self.run_build(dry_run=True).installers, {})
        self.assertEqual(self.run_build().installers, {})
        self.assertEqual(sentinel.read_bytes(), b"keep")

    def test_dry_run_bundles_without_creating_or_changing_outputs(self) -> None:
        self.write_sources()
        dry_result = self.run_build(dry_run=True)
        self.assertFalse(self.output.exists())
        real_result = self.run_build()
        self.assertEqual(dry_result.installers, real_result.installers)
        installer = self.output / "claude" / "@setup" / "install.sh"
        installer.write_bytes(b"sentinel")
        installer.chmod(0o600)
        self.run_build(dry_run=True)
        self.assertEqual(installer.read_bytes(), b"sentinel")
        self.assertEqual(stat.S_IMODE(installer.stat().st_mode), 0o600)

    def assert_bundle_failure(self, message: str) -> None:
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run):
                with self.assertRaisesRegex((ValueError, OSError), message):
                    self.run_build(dry_run=dry_run)
                self.assertFalse(self.output.exists())

    def test_each_required_file_must_exist(self) -> None:
        for name in (
            "install.sh", "install.ps1", "setup.py", "status-line.py", "settings.json",
        ):
            with self.subTest(name=name):
                self.write_sources()
                (self.sources / name).unlink()
                self.assert_bundle_failure(name.replace(".", r"\."))

    def test_strict_utf8_json_rejects_invalid_encodings_and_constants(self) -> None:
        invalid = (
            b"{", _BOM + b"{}", b'{"bad":"\xff"}',
            "{}".encode("utf-16"), "{}".encode("utf-16-le"),
            "{}".encode("utf-32"), "{}".encode("utf-32-le"),
            b'{"n":NaN}', b'{"n":Infinity}', b'{"n":-Infinity}',
        )
        for content in invalid:
            with self.subTest(settings=content):
                self.write_sources({"settings.json": content})
                self.assert_bundle_failure(r"settings\.json")

    def test_json_validation_does_not_add_a_settings_schema(self) -> None:
        self.write_sources({"settings.json": b"null"})
        self.assertTrue(self.run_build(dry_run=True).installers)

    def test_json_rejects_unpaired_surrogates_in_nested_values_and_keys(self) -> None:
        for escape in (b"\\ud800", b"\\udfff"):
            for content in (
                b'{"nested":[{"value":"' + escape + b'"}]}',
                b'{"nested":[{"' + escape + b'":"value"}]}',
                b'{"value":"' + escape + b'","value":"valid"}',
                b'"' + escape + b'"',
            ):
                with self.subTest(settings=content):
                    self.write_sources({"settings.json": content})
                    self.assert_bundle_failure(r"settings\.json.*invalid UTF-8 JSON")

    def test_json_accepts_surrogate_pairs_preserving_original_escaped_bytes(self) -> None:
        content = b'{"\\ud83d\\ude00":["\\ud83d\\ude00"]}'
        self.write_sources({"settings.json": content})
        dry_result = self.run_build(dry_run=True)
        self.assertFalse(self.output.exists())
        real_result = self.run_build()
        self.assertEqual(dry_result.installers, real_result.installers)
        expected = b'SETTINGS_B64 = "eyJcdWQ4M2RcdWRlMDAiOlsiXHVkODNkXHVkZTAwIl19"'
        for name in ("install.sh", "install.ps1"):
            self.assertIn(expected, (
                self.output / "claude" / "@setup" / name
            ).read_bytes())

    def test_exact_constant_assignment_cardinality(self) -> None:
        for assignment in (_STATUS_ASSIGNMENT, _SETTINGS_ASSIGNMENT):
            for count in (0, 2):
                with self.subTest(assignment=assignment, count=count):
                    setup = _SETUP.replace(assignment, assignment * count)
                    self.write_sources({"setup.py": setup})
                    self.assert_bundle_failure(r"setup\.py.*exactly one")

    def test_marker_pair_required_in_each_platform(self) -> None:
        for name, source in (("install.sh", _SHELL_SOURCE), ("install.ps1", _PS_SOURCE)):
            for marker in (_BEGIN, _END):
                with self.subTest(name=name, marker=marker):
                    self.write_sources({name: source.replace(marker, b"missing")})
                    self.assert_bundle_failure("markers.*" + name.replace(".", r"\."))

    def test_version_placeholder_required_after_block_replacement(self) -> None:
        for name, source in (("install.sh", _SHELL_SOURCE), ("install.ps1", _PS_SOURCE)):
            with self.subTest(name=name):
                source = source.replace(_VERSION, b"none")
                # A placeholder in the removed first span does not satisfy the check.
                source = source.replace(b"first span", _VERSION)
                self.write_sources({name: source})
                self.assert_bundle_failure("placeholder.*" + name.replace(".", r"\."))

    def test_python_heredoc_safety_rejections(self) -> None:
        for unsafe, message in (
            (b"# embedded __BUNDLED_PY_END__ marker", "reserved heredoc"),
            (b"'@ anything", "line starting"),
        ):
            with self.subTest(unsafe=unsafe):
                self.write_sources({"setup.py": _SETUP + unsafe + b"\r\n"})
                self.assert_bundle_failure(message)

    def test_naive_clock_is_interpreted_in_moscow(self) -> None:
        self.write_sources()
        build(self.source, self.output, now=datetime(2026, 10, 1, 1, 34, 1))
        self.assertEqual(
            (self.output / "claude" / "@setup" / "install.sh").read_bytes(),
            _EXPECTED_SH,
        )

    def test_aware_clock_uses_moscow_historical_offset(self) -> None:
        self.write_sources()
        build(
            self.source, self.output,
            now=datetime(2012, 9, 30, 22, 34, tzinfo=timezone.utc),
        )
        self.assertEqual(
            (self.output / "claude" / "@setup" / "install.sh").read_bytes(),
            _EXPECTED_SH.replace(_STAMP, b"12.10.010234"),
        )

    def test_repeated_tree_replacement_produces_fresh_installers(self) -> None:
        self.write_sources()
        plugin = self.source / "demo"
        plugin.mkdir()
        (plugin / "ai-plugin.yml").write_text(
            "name: demo\nversion: 1.0.0\ndescription: Demo plugin\n", encoding="utf-8",
        )
        self.run_build()
        setup = self.output / "claude" / "@setup"
        (setup / "install.sh").write_bytes(b"stale installer")
        (setup / "stale").write_bytes(b"remove")
        (self.sources / "install.sh").write_bytes(_SHELL_SOURCE + b"fresh\n")
        self.run_build()
        self.assertEqual((setup / "install.sh").read_bytes(), _EXPECTED_SH + b"fresh\n")
        self.assertEqual((setup / "install.ps1").read_bytes(), _EXPECTED_PS)
        self.assertFalse((setup / "stale").exists())
        self.assertFalse((self.output / "codex" / "@setup").exists())
        self.assertFalse((self.output / "pi" / "@setup").exists())

    def test_installer_only_output_symlinks_preserve_targets(self) -> None:
        self.write_sources()
        target = self.root / "target"
        target.mkdir()
        sentinel = target / "install.sh"
        sentinel.write_bytes(b"keep")
        claude = self.output / "claude"
        claude.mkdir(parents=True)
        (claude / "@setup").symlink_to(target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.run_build()
        self.assertEqual(sentinel.read_bytes(), b"keep")
        (claude / "@setup").unlink()
        (claude / "@setup").mkdir()
        (claude / "@setup" / "install.sh").symlink_to(sentinel)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.run_build()
        self.assertEqual(sentinel.read_bytes(), b"keep")


if __name__ == "__main__":
    unittest.main()
