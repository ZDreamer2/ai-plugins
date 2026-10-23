"""Publishing identity uses real Git history and an explicit clock."""

import copy
from datetime import datetime, timezone
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from marketplace.source import discover_source, resolve_identity


class IdentityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.now = datetime(2026, 9, 30, 21, 2, 3, tzinfo=timezone.utc)

    def write(
        self, relative: str, content: str = "description: Example\n",
    ) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def git(self, *args: str, env: dict[str, str] | None = None) -> str:
        result = subprocess.run(
            ["git", "-c", "commit.gpgsign=false", "-c",
             f"core.hooksPath={self.root / '.no-hooks'}", *args],
            cwd=self.root, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, check=True,
        )
        return result.stdout.strip()

    def init_git(self) -> None:
        self.git("init", "-q")

    def commit(
        self, path: str, timestamp: str, author: str = "Source Author",
    ) -> None:
        self.git("add", "--", path)
        env = os.environ.copy()
        env.update({
            "GIT_AUTHOR_NAME": author,
            "GIT_AUTHOR_EMAIL": "author@example.invalid",
            "GIT_COMMITTER_NAME": "Different Committer",
            "GIT_COMMITTER_EMAIL": "committer@example.invalid",
            "GIT_AUTHOR_DATE": "2020-01-01T00:00:00+0000",
            "GIT_COMMITTER_DATE": timestamp,
        })
        self.git("commit", "-q", "-m", "Fixture", env=env)

    def identities(self) -> dict[str, dict]:
        return {plugin.root: plugin.manifest for plugin in resolve_identity(
            discover_source(self.root), now=self.now,
        ).plugins}

    def test_commit_paths_and_distinct_author_committer(self) -> None:
        self.init_git()
        self.write("dev/one/ai-plugin.yml")
        self.commit("dev/one", "2026-09-28T23:59:58+0000", "First Author")
        self.write("other/ai-plugin.yml")
        self.commit("other", "2026-09-29T12:00:01+0000", "Other Author")
        data = self.identities()
        self.assertEqual(data["dev/one"]["version"], "26.09.29025958")
        self.assertEqual(data["dev/one"]["author"], {"name": "First Author"})
        self.assertEqual(data["other"]["version"], "26.09.29150001")
        self.write("@common/docs/shared.md", "shared")
        self.commit("@common", "2026-09-30T01:02:03+0000", "Shared Author")
        data = self.identities()
        for manifest in data.values():
            self.assertEqual(manifest["version"], "26.09.30040203")
            self.assertEqual(manifest["author"], {"name": "Shared Author"})
        self.write("README.md", "unrelated root content")
        self.commit("README.md", "2026-09-30T11:00:00+0000", "Root Author")
        self.assertEqual(self.identities(), data)

    def test_explicit_null_defaults_and_raw_mapping(self) -> None:
        self.init_git()
        self.write(
            "dev/folder/ai-plugin.yml",
            "name: null\nversion: null\nauthor: null\n"
            "extra:\n  values: [a, b]\n",
        )
        self.write(
            "explicit/ai-plugin.yml",
            "name: Published_Name\nversion: 2.3.4\n"
            "author: {name: Authored}\nextra: {flag: true}\n",
        )
        self.write("version-only/ai-plugin.yml", "version: 9.0.0\n")
        self.write("auto/ai-plugin.yml", "version: AUTO_VERSION\n")
        self.commit(".", "2026-09-30T01:02:03+0000", "History Author")
        inventory = discover_source(self.root)
        before = copy.deepcopy([p.manifest for p in inventory.plugins])
        resolved = resolve_identity(inventory, now=self.now)
        self.assertEqual([p.manifest for p in inventory.plugins], before)
        self.assertIsNot(resolved, inventory)
        data = {p.root: p.manifest for p in resolved.plugins}
        self.assertEqual(data["dev/folder"], {
            "name": "folder", "version": "26.09.30040203",
            "author": {"name": "History Author"},
            "extra": {"values": ["a", "b"]},
        })
        self.assertEqual(data["explicit"], {
            "name": "Published_Name", "version": "2.3.4",
            "author": {"name": "Authored"}, "extra": {"flag": True},
        })
        self.assertEqual(data["version-only"]["version"], "9.0.0")
        self.assertEqual(
            data["version-only"]["author"], {"name": "History Author"},
        )
        self.assertEqual(data["auto"]["version"], "26.09.30040203")
        raw = next(
            p.manifest for p in inventory.plugins if p.root == "dev/folder"
        )
        self.assertIs(data["dev/folder"]["extra"], raw["extra"])

    def test_no_repository_no_history_and_untracked_clock(self) -> None:
        self.write("missing/ai-plugin.yml")
        self.write(
            "null/ai-plugin.yml", "name: null\nversion: null\nauthor: null\n",
        )
        for init in (False, True):
            if init:
                self.init_git()
            with self.subTest(repository=init):
                data = self.identities()
                self.assertEqual(data["missing"]["version"], "26.10.01000203")
                self.assertNotIn("author", data["missing"])
                self.assertIsNone(data["null"]["author"])
        self.write("other/ai-plugin.yml")
        self.commit("other", "2026-09-28T00:00:00+0000")
        data = self.identities()
        self.assertEqual(data["missing"]["version"], "26.10.01000203")
        self.assertNotIn("author", data["missing"])

    def test_custom_timezone_and_naive_clock_are_explicit(self) -> None:
        self.write("plugin/ai-plugin.yml")
        inventory = discover_source(self.root)
        resolved = resolve_identity(
            inventory, now=self.now, timezone=timezone.utc,
        )
        self.assertEqual(
            resolved.plugins[0].manifest["version"], "26.09.30210203",
        )
        resolved = resolve_identity(
            inventory, now=self.now.replace(tzinfo=None),
        )
        self.assertEqual(
            resolved.plugins[0].manifest["version"], "26.09.30210203",
        )

    def test_duplicate_default_and_explicit_identity(self) -> None:
        self.write("a/duplicate/ai-plugin.yml")
        self.write("b/folder/ai-plugin.yml", "name: duplicate\n")
        inventory = discover_source(self.root)
        with self.assertRaises(ValueError) as error:
            resolve_identity(inventory, now=self.now)
        message = str(error.exception)
        self.assertIn("a/duplicate", message)
        self.assertIn("b/folder", message)
        self.assertIn("duplicate", message)
        self.assertNotIn("name", inventory.plugins[0].manifest)


if __name__ == "__main__":
    unittest.main()
