"""Discovery and skill naming use source facts and logical ownership."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from marketplace.source import (
    codex_skill_names,
    discover_source,
    pi_skill_for_invocation,
    pi_skill_name,
    pi_source_skill_names,
    plugin_name,
    plugin_root_of,
    source_skill_name,
)


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(
        self, relative: str, content: str = "description: Example\n",
    ) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_sorted_discovery_hidden_vcs_exclusions_and_symlinks(self) -> None:
        for relative in (
            "z/ai-plugin.yml", "dev/group/b/ai-plugin.yml",
            "dev/a/ai-plugin.yml", ".hidden/ai-plugin.yml",
            "group/.nested/ai-plugin.yml", ".git/ai-plugin.yml",
            "CVS/ai-plugin.yml", "_darcs/ai-plugin.yml", "_svn/ai-plugin.yml",
            "output/nested/tree/ai-plugin.yml", "keep/tree/ai-plugin.yml",
        ):
            self.write(relative)
        (self.root / "alias").symlink_to(
            self.root / "dev", target_is_directory=True,
        )
        (self.root / "cycle").symlink_to(self.root, target_is_directory=True)
        # Output may not exist yet, or may be supplied as an absolute path.
        inventory = discover_source(self.root, (
            self.root / "output/nested", "future/output",
        ))
        self.assertEqual([p.root for p in inventory.plugins], [
            "dev/a", "dev/group/b", "keep/tree", "z",
        ])
        self.assertEqual(inventory.directory, self.root.resolve())
        self.assertEqual(inventory.plugins[0].directory, self.root / "dev/a")
        # Output exclusions belong to the caller.
        self.assertIn(
            "output/nested/tree",
            [p.root for p in discover_source(self.root).plugins],
        )

    def test_immediate_skills_and_combined_extension_order(self) -> None:
        self.write("plugin/ai-plugin.yml")
        for relative in (
            "skills/z/SKILL.md", "skills/a/SKILL.md",
            "skills/nested/deep/SKILL.md",
            "skills/.hidden/SKILL.md", "skills/no-entry/body.md",
            "extensions/z/index.ts", "extensions/a/index.ts",
            "extensions/a/index.js",
            "extensions/a/index.mjs", "extensions/deep/nested/index.js",
            "extensions/.hidden/index.js", "extensions/b/index.py",
        ):
            self.write("plugin/" + relative, "body")
        plugin = discover_source(self.root).plugins[0]
        self.assertEqual(plugin.skills, ("skills/a", "skills/z"))
        self.assertEqual(plugin.extensions, (
            "extensions/a/index.js", "extensions/a/index.mjs",
            "extensions/a/index.ts", "extensions/z/index.ts",
        ))

    def test_logical_shared_and_nearest_manifest_ownership(self) -> None:
        self.write("dev/plugin/ai-plugin.yml")
        self.write("dev/plugin/nested/ai-plugin.yml")
        self.write("@common/docs/example.md", "shared")
        (self.root / "dev/plugin/@common").symlink_to(
            self.root / "@common", target_is_directory=True,
        )
        inventory = discover_source(self.root, ("dev/plugin/nested",))
        self.assertEqual(
            plugin_root_of(inventory, "dev/plugin/@common/docs/example.md"),
            "dev/plugin",
        )
        self.assertEqual(
            plugin_root_of(inventory, "dev/plugin/nested/docs/file.md"),
            "dev/plugin/nested",
        )
        self.assertEqual(
            plugin_root_of(inventory, "dev/plugin/docs/future.md"),
            "dev/plugin",
        )
        for path in (
            "README.md", "@common/docs/example.md", "dev/plugin-extra/file.md",
            "../outside", "/outside",
        ):
            with self.subTest(path=path):
                self.assertIsNone(plugin_root_of(inventory, path))

    def test_exclusions_apply_to_skill_and_extension_entry_points(self) -> None:
        self.write("plugin/ai-plugin.yml")
        for path in (
            "skills/keep/SKILL.md", "skills/output/SKILL.md",
            "extensions/keep/index.ts", "extensions/output/index.ts",
        ):
            self.write("plugin/" + path, "resource")
        plugin = discover_source(self.root, (
            "plugin/skills/output", "plugin/extensions/output",
        )).plugins[0]
        self.assertEqual(plugin.skills, ("skills/keep",))
        self.assertEqual(plugin.extensions, ("extensions/keep/index.ts",))
        # An output ancestor is a valid external output location, not a reason
        # to discard every resource inside the independently selected source.
        plugin = discover_source(self.root, (self.root.parent,)).plugins[0]
        self.assertEqual(plugin.skills, ("skills/keep", "skills/output"))
        self.assertEqual(plugin.extensions, (
            "extensions/keep/index.ts", "extensions/output/index.ts",
        ))

    def test_empty_inventory_and_root_plugin_are_not_rejected(self) -> None:
        inventory = discover_source(self.root)
        self.assertEqual(inventory.plugins, ())
        self.write("ai-plugin.yml", "name: null\n")
        inventory = discover_source(self.root)
        self.assertEqual(inventory.plugins[0].root, ".")
        self.assertEqual(plugin_name(inventory.plugins[0]), self.root.name)
        self.assertEqual(plugin_root_of(inventory, "README.md"), ".")

    def test_output_manifest_file_aliases_are_excluded_before_reading(self) -> None:
        self.write("keep/ai-plugin.yml")
        generated = self.write("keep/generated/ai-plugin.yml", "invalid: [\n")
        alias = self.root / "alias/ai-plugin.yml"
        alias.parent.mkdir()
        alias.symlink_to(generated)
        inventory = discover_source(self.root, (generated.parent,))
        self.assertEqual(("keep",), tuple(p.root for p in inventory.plugins))
        # A manifest link to ordinary source remains a logical plugin.
        alias.unlink()
        alias.symlink_to(self.root / "keep/ai-plugin.yml")
        inventory = discover_source(self.root, (generated.parent,))
        self.assertEqual(("alias", "keep"), tuple(p.root for p in inventory.plugins))

    def test_external_output_manifest_alias_remains_a_source_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            generated = output / "manifest.yml"
            generated.write_text("description: External\n")
            alias = self.root / "plugin/ai-plugin.yml"
            alias.parent.mkdir()
            alias.symlink_to(generated)
            inventory = discover_source(self.root, (output,))
            self.assertEqual(("plugin",), tuple(p.root for p in inventory.plugins))

    def test_manifest_namespace_pi_lookup_and_scanner_order(self) -> None:
        self.write("dev/folder/ai-plugin.yml", "name: alpha\n")
        self.write("z-beta/ai-plugin.yml", "name: beta\n")
        for skill in ("alpha", "load"):
            self.write(
                f"dev/folder/skills/{skill}/SKILL.md", "unparsed frontmatter",
            )
        for skill in ("load", "z"):
            self.write(
                f"z-beta/skills/{skill}/SKILL.md", "unparsed frontmatter",
            )
        inventory = discover_source(self.root)
        plugin = inventory.plugins[0]
        self.assertEqual(
            source_skill_name(plugin, "skills/load/SKILL.md"), "load",
        )
        self.assertEqual(
            pi_skill_name(plugin, "skills/alpha/SKILL.md"), "alpha",
        )
        self.assertEqual(
            pi_skill_name(plugin, "skills/load/SKILL.md"), "alpha-load",
        )
        for invocation, expected in (
            ("alpha", "alpha"), ("alpha:alpha", "alpha"),
            ("alpha:load", "alpha-load"), ("beta:load", "beta-load"),
        ):
            self.assertEqual(
                pi_skill_for_invocation(inventory, invocation), expected,
            )
        for missing in (
            "folder:load", "folder", "beta", "load", "alpha:missing",
            "unknown:load",
        ):
            self.assertIsNone(pi_skill_for_invocation(inventory, missing))
        self.assertEqual(codex_skill_names(inventory), (
            "alpha", "folder:alpha", "load", "folder:load", "z-beta:load",
            "z", "z-beta:z",
        ))
        self.assertEqual(pi_source_skill_names(inventory), (
            "alpha", "folder:alpha", "load", "folder:load", "z-beta:load",
            "z", "z-beta:z",
            "alpha:alpha", "alpha:load", "beta:load", "beta:z",
        ))
        for path in (
            "skills/missing/SKILL.md", "skills/load/body.md", "docs/SKILL.md",
        ):
            with self.assertRaises(ValueError):
                source_skill_name(plugin, path)

    def test_discovery_does_not_enforce_future_pi_name_rules(self) -> None:
        self.write("folder/ai-plugin.yml", "name: UPPER_Name\n")
        self.write(
            "folder/skills/Long_Name/SKILL.md", "invalid Pi frontmatter",
        )
        plugin = discover_source(self.root).plugins[0]
        self.assertEqual(
            pi_skill_name(plugin, "skills/Long_Name/SKILL.md"),
            "UPPER_Name-Long_Name",
        )

    def test_discovery_does_not_need_timezone_data(self) -> None:
        self.write("plugin/ai-plugin.yml")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[3])
        env["PYTHONTZPATH"] = ""
        result = subprocess.run(
            [sys.executable, "-S", "-c",
             "import sys; from marketplace.source import discover_source; "
             "print(discover_source(sys.argv[1]).plugins[0].root)",
             str(self.root)],
            cwd=self.root, env=env, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, check=True,
        )
        self.assertEqual(result.stdout, "plugin\n")


if __name__ == "__main__":
    unittest.main()
