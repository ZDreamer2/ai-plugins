"""Original manifests remain distinct from publishing identity."""

from pathlib import Path
import tempfile
import unittest

from marketplace.source import read_manifest


class ManifestTests(unittest.TestCase):
    def test_retains_extra_fields_values_and_null_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ai-plugin.yml"
            path.write_text(
                "name: null\nversion: null\nauthor: null\n"
                "description: |\n  First line\n  Second line\n"
                "hooks: &hooks\n  enabled: true\n  command: on\n"
                "extra:\n  <<: *hooks\n  count: 0o17\n",
                encoding="utf-8",
            )
            raw = read_manifest(path)
            self.assertEqual(raw, {
                "name": None, "version": None, "author": None,
                "description": "First line\nSecond line\n",
                "hooks": {"enabled": True, "command": "on"},
                "extra": {"enabled": True, "command": "on", "count": 15},
            })
            self.assertIs(type(raw["hooks"]["enabled"]), bool)
            self.assertIs(type(raw["extra"]["count"]), int)

    def test_bad_yaml_and_non_mappings_report_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ai-plugin.yml"
            for content in (
                "name: [broken", "name: a\nname: b\n", "- entry\n",
                "null\n", "", "scalar",
            ):
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError) as error:
                        read_manifest(path)
                    self.assertIn(str(path), str(error.exception))

    def test_missing_and_non_utf8_inputs_report_source_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ai-plugin.yml"
            with self.assertRaises(ValueError) as error:
                read_manifest(path)
            self.assertIn(str(path), str(error.exception))
            path.write_bytes(b"description: \xff")
            with self.assertRaises(ValueError) as error:
                read_manifest(path)
            self.assertIn(str(path), str(error.exception))


if __name__ == "__main__":
    unittest.main()
