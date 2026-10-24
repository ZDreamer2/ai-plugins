"""Guard the standalone two-plugin source and generated distribution seam."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from marketplace.build import build
from marketplace.build.rendering import render_file
from marketplace.source import discover_source
from marketplace.validation import validate_pi_distribution


ROOT = Path(__file__).resolve().parents[4]
PLUGIN_NAMES = {"ai-doc", "ai-marketplace"}


class ExtractionTests(unittest.TestCase):
    def test_source_boundary(self) -> None:
        inventory = discover_source(ROOT)
        self.assertEqual({plugin.manifest["name"] for plugin in inventory.plugins}, PLUGIN_NAMES)
        self.assertEqual(len(inventory.plugins), 2)
        self.assertFalse((ROOT / "ai").exists())
        for name in PLUGIN_NAMES:
            self.assertTrue((ROOT / name / "ai-plugin.yml").is_file())
            for path in (ROOT / name).rglob("*"):
                self.assertFalse(path.is_symlink(), str(path))
                self.assertNotIn(path.name, {"@common", "@setup", "@setup-sources"})
        vendor = ROOT / "ai-marketplace/scripts/marketplace/_vendor"
        self.assertTrue((vendor / "PyYAML.LICENSE").is_file())
        self.assertTrue((vendor / "PyYAML.provenance.md").is_file())

    def test_unpublished_rm_example_is_literal_for_every_host(self) -> None:
        path = "ai-doc/Formats/SkillDoc/Types/HubSkill.format.md"
        text = (ROOT / path).read_text(encoding="utf-8")
        inventory = discover_source(ROOT)
        for host in ("claude", "codex", "pi"):
            with self.subTest(host=host):
                rendered = render_file(text, path, host, inventory)
                self.assertEqual(rendered.count("${AGENT_SKILL(rm)}"), 3)
                self.assertNotIn("$${AGENT_SKILL(rm)}", rendered)

    def test_moved_authoring_context_has_no_shared_lifecycle_dependency(self) -> None:
        for name in ("AuthoringSyntax.meta.md", "HostRendering.meta.md"):
            text = (ROOT / "ai-marketplace/docs" / name).read_text(encoding="utf-8")
            self.assertNotIn("@common/docs/", text)
            self.assertIn("../../docs/Maintaining.md", text)
        for relative in (
            "ai-marketplace/codebase/on-plan.meta.md",
            "ai-marketplace/codebase/on-build.meta.md",
            "ai-doc/Theory/docs-usefulness.meta.md",
            "ai-doc/Formats/WorkflowDoc/Blocks/CallSubagentStep.meta.md",
        ):
            self.assertNotIn("dev/forge/", (ROOT / relative).read_text(encoding="utf-8"))

    def test_isolated_outputs_agree_on_identity_and_boundary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="zd-plugins-extraction-") as temporary:
            output = Path(temporary) / "output"
            result = build(ROOT, output)
            self.assertEqual(result.plugin_count, 2)
            self.assertEqual(result.installers, {})
            self.assertEqual(validate_pi_distribution(ROOT, output / "pi", output), 2)
            for host, registry in (
                ("claude", ".claude-plugin/marketplace.json"),
                ("codex", ".agents/plugins/marketplace.json"),
            ):
                catalog = json.loads((output / host / registry).read_text())
                self.assertEqual(catalog["name"], "zd-plugins")
                self.assertEqual({p["name"] for p in catalog["plugins"]}, PLUGIN_NAMES)
                self.assertEqual(len(catalog["plugins"]), 2)
                self.assertEqual(
                    {p["source"] if host == "claude" else p["source"]["path"]
                     for p in catalog["plugins"]},
                    {"./ai-doc", "./ai-marketplace"},
                )
                if host == "claude":
                    self.assertEqual(catalog["owner"], {"name": "ZDreamer2"})
            for host in ("claude", "codex", "pi"):
                tree = output / host
                readme = (tree / "README.md").read_text()
                self.assertIn("https://github.com/ZDreamer2/ai-plugins", readme)
                self.assertIn("## Install", readme)
                self.assertNotIn("## GitLab publication", readme)
                self.assertFalse((tree / ".marketplace").exists())
                for path in tree.rglob("*"):
                    self.assertFalse(path.is_symlink(), str(path))
                    self.assertNotIn(path.name, {"@common", "@setup", "@setup-sources"})
                for name in PLUGIN_NAMES:
                    plugin = tree / name
                    if host == "pi":
                        package = json.loads((plugin / "package.json").read_text())
                        self.assertEqual(package["name"], "@zdreamer2/pi-plugin-" + name)
                    else:
                        metadata = json.loads((plugin / f".{host}-plugin/plugin.json").read_text())
                        self.assertEqual(metadata["name"], name)
                for relative in (
                    "ai-doc/scripts/find-doc.py",
                    "ai-doc/scripts/move-doc.py",
                    "ai-doc/scripts/diff_doc/__main__.py",
                    "ai-doc/skills/ref/Tools/print-ai-doc-by-ref.py",
                ):
                    self.assertEqual((tree / relative).stat().st_mode & 0o777,
                                     (ROOT / relative).stat().st_mode & 0o777)
                helper = tree / "ai-doc/scripts/diff_doc/__main__.py"
                process = subprocess.run(
                    [sys.executable, "-B", "-S", str(helper), "--help"],
                    cwd=temporary, capture_output=True, text=True,
                )
                self.assertEqual(process.returncode, 0, process.stderr)


if __name__ == "__main__":
    unittest.main()
