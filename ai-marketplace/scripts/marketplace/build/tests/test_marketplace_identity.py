"""Marketplace branding is shared by every host and independent Pi validation."""

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from marketplace.build import build
from marketplace.source import MarketplaceIdentity, read_marketplace_identity
from marketplace.validation import validate_pi_distribution


BICO = {
    "name": "bc-plugins", "owner": "Bico",
    "description": "Claude Code плагины для Bico",
    "display_name": "Bico plugins", "pi_package_prefix": "@bico/pi-plugin-",
}


class MarketplaceIdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        self.output = Path(self.temp.name) / "output"
        plugin = self.root / "example"
        plugin.mkdir()
        (plugin / "ai-plugin.yml").write_text("description: Example\n", encoding="utf-8")
        self.config = self.root / ".marketplace/identity.json"
        self.config.parent.mkdir()

    def configure(self, value: object) -> None:
        self.config.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

    def build(self, dry_run: bool = False) -> None:
        build(self.root, self.output, dry_run,
              now=datetime(2026, 2, 3, 0, 4, 5, tzinfo=timezone.utc))

    def metadata(self, relative: str) -> dict:
        return json.loads((self.output / relative).read_text(encoding="utf-8"))

    def test_defaults_explicit_defaults_and_bico_across_hosts(self) -> None:
        for config in (None, vars(MarketplaceIdentity()), BICO):
            with self.subTest(config=config):
                if config is not None:
                    self.configure(config)
                expected = config or vars(MarketplaceIdentity())
                identity = read_marketplace_identity(self.root)
                self.assertEqual(vars(identity), expected)
                self.build()
                claude = self.metadata("claude/.claude-plugin/marketplace.json")
                self.assertEqual(claude["name"], expected["name"])
                self.assertEqual(claude["owner"], {"name": expected["owner"]})
                self.assertEqual(claude["metadata"], {"description": expected["description"]})
                codex = self.metadata("codex/.agents/plugins/marketplace.json")
                self.assertEqual(codex["name"], expected["name"])
                self.assertEqual(codex["interface"], {"displayName": expected["display_name"]})
                package = self.metadata("pi/example/package.json")
                self.assertEqual(package["name"], expected["pi_package_prefix"] + "example")
                for relative in ("claude/example/.claude-plugin/plugin.json",
                                 "codex/example/.codex-plugin/plugin.json",
                                 "pi/example/package.json", "pi/example/.pi-plugin/plugin.json"):
                    self.assertEqual(self.metadata(relative)["version"], "26.2.3030405")
                self.assertEqual(validate_pi_distribution(
                    self.root, self.output / "pi", self.output), 1)
                for host in ("claude", "codex", "pi"):
                    self.assertFalse((self.output / host / ".marketplace").exists())

    def test_complete_package_name_length_boundary_preserves_output(self) -> None:
        for scope in ("", "@bico/"):
            with self.subTest(scope=scope):
                prefix = scope + "a" * (214 - len(scope) - 1 - len("example")) + "-"
                self.configure(dict(BICO, pi_package_prefix=prefix))
                self.build()
                self.assertEqual(len(self.metadata("pi/example/package.json")["name"]), 214)
                self.assertEqual(validate_pi_distribution(
                    self.root, self.output / "pi", self.output), 1)
                before = {path.relative_to(self.output): path.read_bytes()
                          for path in self.output.rglob("*") if path.is_file()}
                oversized_prefix = prefix[:-1] + "a-"
                self.configure(dict(BICO, pi_package_prefix=oversized_prefix))
                self.assertEqual(len(oversized_prefix + "example"), 215)
                for dry_run in (False, True):
                    with self.assertRaisesRegex(ValueError, "214-character limit"):
                        self.build(dry_run)
                    after = {path.relative_to(self.output): path.read_bytes()
                             for path in self.output.rglob("*") if path.is_file()}
                    self.assertEqual(after, before)
                package_path = self.output / "pi/example/package.json"
                package = self.metadata("pi/example/package.json")
                package["name"] = oversized_prefix + "example"
                package_path.write_text(json.dumps(package), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "214-character limit"):
                    validate_pi_distribution(self.root, self.output / "pi", self.output)
                # Also reject an oversized artifact against valid source identity.
                self.configure(dict(BICO, pi_package_prefix=prefix))
                with self.assertRaisesRegex(ValueError, "214-character limit"):
                    validate_pi_distribution(self.root, self.output / "pi", self.output)

    def test_validator_rejects_prefix_not_matching_source_config(self) -> None:
        self.configure(BICO)
        self.build()
        self.config.unlink()
        with self.assertRaisesRegex(ValueError, "Incorrect Pi package identity"):
            validate_pi_distribution(self.root, self.output / "pi", self.output)

    def test_invalid_config_never_mutates_output_even_without_plugins(self) -> None:
        self.build()
        before = {path.relative_to(self.output): path.read_bytes()
                  for path in self.output.rglob("*") if path.is_file()}
        invalid = [None, [], {}, dict(BICO, extra="ignored"),
                   dict(BICO, name="Upper"), dict(BICO, name="../escape"),
                   dict(BICO, pi_package_prefix="@Bico/pi-plugin-"),
                   dict(BICO, pi_package_prefix="@bico/"),
                   dict(BICO, pi_package_prefix="../"),
                   dict(BICO, owner=" Bico"), dict(BICO, owner="Bico\n"),
                   dict(BICO, owner="Bi\u007fco"),
                   dict(BICO, description="\ud800")]
        for field in BICO:
            invalid.extend(({key: value for key, value in BICO.items() if key != field},
                            dict(BICO, **{field: " "}), dict(BICO, **{field: 42})))
        texts = [json.dumps(value) for value in invalid]
        texts.extend(("{", '{"name":"one","name":"two"}'))
        for no_plugins in (False, True):
            if no_plugins:
                (self.root / "example/ai-plugin.yml").unlink()
            for text in texts:
                self.config.write_text(text, encoding="utf-8")
                for dry_run in (False, True):
                    with self.subTest(text=text, dry_run=dry_run, no_plugins=no_plugins):
                        with self.assertRaisesRegex(ValueError, "Invalid marketplace identity config"):
                            self.build(dry_run)
                        with self.assertRaisesRegex(ValueError, "Invalid marketplace identity config"):
                            validate_pi_distribution(self.root, self.output / "pi", self.output)
                        after = {path.relative_to(self.output): path.read_bytes()
                                 for path in self.output.rglob("*") if path.is_file()}
                        self.assertEqual(after, before)

    def test_unreadable_and_dangling_config_fail_closed(self) -> None:
        self.config.mkdir()
        with self.assertRaisesRegex(ValueError, "Invalid marketplace identity config"):
            self.build()
        self.config.rmdir()
        self.config.symlink_to("missing.json")
        with self.assertRaisesRegex(ValueError, "Invalid marketplace identity config"):
            self.build()
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
