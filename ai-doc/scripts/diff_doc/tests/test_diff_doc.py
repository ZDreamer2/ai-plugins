"""Real-repository CLI tests. Run: python3 -m unittest discover -s scripts/diff_doc/tests

Run from the ai-doc plugin root. Fixtures live outside the checkout.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1]


class DiffDocTests(unittest.TestCase):
	def setUp(self):
		self.temporary = tempfile.TemporaryDirectory()
		self.addCleanup(self.temporary.cleanup)
		self.root = Path(self.temporary.name)
		self.repo = self.root / "repo"
		self.repo.mkdir()
		self.env = dict(os.environ)
		for key in list(self.env):
			if key.startswith("GIT_"):
				del self.env[key]
		self.env.update({"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
		self.init_repo(self.repo)

	def git(self, *args, repo=None):
		return subprocess.run(
			["git", *args], cwd=repo or self.repo, env=self.env,
			capture_output=True, text=True, check=True,
		).stdout

	def init_repo(self, repo):
		self.git("init", "--quiet", repo=repo)
		self.git("config", "user.name", "Test", repo=repo)
		self.git("config", "user.email", "test@example.invalid", repo=repo)

	def write(self, name, content, repo=None):
		path = (repo or self.repo) / name
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(content, encoding="utf-8")
		return path

	def commit(self, repo=None):
		self.git("add", "--all", repo=repo)
		self.git("commit", "--quiet", "-m", "fixture", repo=repo)

	def run_script(self, path="Doc.md", repo=None, cwd=None):
		path = Path(path)
		if not path.is_absolute():
			path = (repo or self.repo) / path
		return subprocess.run(
			[sys.executable, str(SCRIPT), str(path)], cwd=cwd or self.root,
			env=self.env, capture_output=True, text=True,
		)

	def successful(self, result):
		self.assertEqual(result.returncode, 0, result.stderr)
		self.assertEqual(result.stderr, "")
		return result.stdout

	def test_staged_and_unstaged_pair_diff_against_head_without_index_changes(self):
		self.write("Doc.md", "old document\n")
		self.write("Doc.meta.md", "old meta\n")
		self.commit()
		self.write("Doc.md", "staged document\n")
		self.git("add", "Doc.md")
		self.write("Doc.md", "final document\n")
		self.write("Doc.meta.md", "final meta\n")
		index = (self.repo / ".git/index").read_bytes()
		output = self.successful(self.run_script())
		self.assertIn("-old document", output)
		self.assertIn("+final document", output)
		self.assertNotIn("staged document", output)
		self.assertIn("-old meta", output)
		self.assertIn("+final meta", output)
		self.assertEqual(index, (self.repo / ".git/index").read_bytes())

	def test_unchanged_pair_has_no_diff(self):
		self.write("Doc.md", "unchanged\n")
		self.write("Doc.meta.md", "unchanged meta\n")
		self.commit()
		output = self.successful(self.run_script())
		self.assertIn("No changes in document or meta.", output)
		self.assertNotIn("diff --git", output)

	def test_missing_meta_is_optional(self):
		self.write("Doc.md", "before\n")
		self.commit()
		self.write("Doc.md", "after\n")
		output = self.successful(self.run_script())
		self.assertIn("+after", output)
		self.assertNotIn("Doc.meta.md", output)

	def test_only_changed_meta_shown(self):
		self.write("Doc.md", "unchanged\n")
		self.write("Doc.meta.md", "before\n")
		self.commit()
		self.write("Doc.meta.md", "after\n")
		output = self.successful(self.run_script())
		self.assertIn("diff --git a/Doc.meta.md b/Doc.meta.md", output)
		self.assertNotIn("diff --git a/Doc.md b/Doc.md", output)

	def test_new_pair_reports_status_only_and_leaves_index_unchanged(self):
		self.write("Existing.md", "baseline\n")
		self.commit()
		self.write("Doc.md", "PRIVATE UNTRACKED CONTENT\n")
		self.write("Doc.meta.md", "PRIVATE STAGED CONTENT\n")
		self.git("add", "Doc.meta.md")
		self.write("Unrelated.md", "unrelated\n")
		index = (self.repo / ".git/index").read_bytes()
		output = self.successful(self.run_script())
		self.assertIn("untracked: Doc.md", output)
		self.assertIn("added: Doc.meta.md", output)
		self.assertNotIn("CONTENT", output)
		self.assertNotIn("diff --git", output)
		self.assertNotIn("Unrelated.md", output)
		self.assertEqual(index, (self.repo / ".git/index").read_bytes())

	def test_unborn_repository_reports_indexed_and_untracked_as_new(self):
		self.write("Doc.md", "new indexed document\n")
		self.write("Doc.meta.md", "new untracked meta\n")
		self.git("add", "Doc.md")
		output = self.successful(self.run_script())
		self.assertIn("added: Doc.md", output)
		self.assertIn("untracked: Doc.meta.md", output)
		self.assertNotIn("new indexed", output)
		self.assertNotIn("new untracked", output)

	def test_new_meta_status_alongside_existing_doc_diff(self):
		self.write("Doc.md", "before\n")
		self.commit()
		self.write("Doc.md", "after\n")
		self.write("Doc.meta.md", "new meta content\n")
		output = self.successful(self.run_script())
		self.assertIn("+after", output)
		self.assertIn("untracked: Doc.meta.md", output)
		self.assertNotIn("new meta content", output)

	def test_deleted_doc_and_meta_are_diffed_even_when_parent_is_removed(self):
		self.write("docs/Doc.md", "document deletion\n")
		self.write("docs/Doc.meta.md", "meta deletion\n")
		self.commit()
		self.git("rm", "docs/Doc.md")
		(self.repo / "docs/Doc.meta.md").unlink()
		(self.repo / "docs").rmdir()
		output = self.successful(self.run_script("docs/Doc.md"))
		self.assertIn("-document deletion", output)
		self.assertIn("-meta deletion", output)
		self.assertEqual(output.count("deleted file mode"), 2)

	def test_format_doc_uses_meta_before_final_extension(self):
		self.write("Doc.format.md", "before\n")
		self.write("Doc.format.meta.md", "meta before\n")
		self.commit()
		self.write("Doc.format.meta.md", "meta after\n")
		output = self.successful(self.run_script("Doc.format.md"))
		self.assertIn("Doc.format.meta.md", output)
		self.assertIn("+meta after", output)

	def test_closest_nested_repository_wins_from_unrelated_cwd(self):
		self.write(".gitignore", "nested/\n")
		self.write("Doc.md", "outer before\n")
		self.commit()
		self.write("Doc.md", "outer after\n")
		nested = self.repo / "nested"
		nested.mkdir()
		self.init_repo(nested)
		self.write("docs/Doc.md", "nested before\n", repo=nested)
		self.commit(repo=nested)
		self.write("docs/Doc.md", "nested after\n", repo=nested)
		output = self.successful(self.run_script("docs/Doc.md", repo=nested))
		self.assertIn(f"Repository: {nested}", output)
		self.assertIn("+nested after", output)
		self.assertNotIn("outer after", output)

	def test_worktree_git_file_is_supported(self):
		self.write("Doc.md", "before\n")
		self.commit()
		worktree = self.root / "worktree"
		self.git("worktree", "add", "--quiet", "--detach", str(worktree))
		self.assertTrue((worktree / ".git").is_file())
		self.write("Doc.md", "worktree after\n", repo=worktree)
		output = self.successful(self.run_script(repo=worktree))
		self.assertIn(f"Repository: {worktree}", output)
		self.assertIn("+worktree after", output)

	def test_tracked_symlink_retarget_is_diffed_as_the_requested_file(self):
		self.write("A.md", "first destination content\n")
		self.write("B.md", "second destination content\n")
		document = self.repo / "Doc.md"
		document.symlink_to("A.md")
		self.commit()
		document.unlink()
		document.symlink_to("B.md")
		output = self.successful(self.run_script())
		self.assertIn("diff --git a/Doc.md b/Doc.md", output)
		self.assertIn("-A.md", output)
		self.assertIn("+B.md", output)
		self.assertNotIn("destination content", output)

	def test_symlink_keeps_its_own_repository_and_companion_meta(self):
		nested = self.repo / "nested"
		nested.mkdir()
		self.init_repo(nested)
		self.write("Target.md", "target before\n", repo=nested)
		self.commit(repo=nested)
		self.write(".gitignore", "nested/\n")
		(self.repo / "Doc.md").symlink_to("nested/Target.md")
		self.write("Doc.meta.md", "meta before\n")
		self.commit()
		self.write("Target.md", "unrelated target after\n", repo=nested)
		self.write("Doc.meta.md", "meta after\n")
		output = self.successful(self.run_script())
		self.assertIn(f"Repository: {self.repo}\n", output)
		self.assertIn("+meta after", output)
		self.assertNotIn("unrelated target after", output)

	def test_untracked_dangling_symlinks_report_status_only(self):
		(self.repo / "Doc.md").symlink_to("Missing.md")
		(self.repo / "Doc.meta.md").symlink_to("Missing.meta.md")
		output = self.successful(self.run_script())
		self.assertIn("untracked: Doc.md", output)
		self.assertIn("untracked: Doc.meta.md", output)
		self.assertNotIn("Missing", output)
		self.assertNotIn("diff --git", output)

	def test_literal_paths_do_not_match_other_files(self):
		self.write("Doc[1].md", "before\n")
		self.write("Doc1.md", "unrelated before\n")
		self.commit()
		self.write("Doc[1].md", "requested after\n")
		self.write("Doc1.md", "unrelated after\n")
		output = self.successful(self.run_script("Doc[1].md"))
		self.assertIn("+requested after", output)
		self.assertNotIn("unrelated after", output)

	def test_relative_argument_resolves_from_cwd(self):
		self.write("Doc.md", "before\n")
		self.commit()
		self.write("Doc.md", "after\n")
		result = subprocess.run(
			[sys.executable, str(SCRIPT), "repo/Doc.md"], cwd=self.root,
			env=self.env, capture_output=True, text=True,
		)
		self.assertIn("+after", self.successful(result))

	def test_missing_target_is_an_error(self):
		result = self.run_script()
		self.assertEqual(result.returncode, 1)
		self.assertIn("does not exist", result.stderr)
		self.assertEqual(result.stdout, "")

	def test_target_outside_repository_is_an_error(self):
		path = self.write("Doc.md", "outside\n", repo=self.root)
		result = self.run_script(path)
		self.assertEqual(result.returncode, 1)
		self.assertIn("not in a Git repository", result.stderr)

	def test_git_failure_is_not_reported_as_no_changes(self):
		(self.repo / ".git").rename(self.repo / "git-backup")
		(self.repo / ".git").write_text("gitdir: missing-directory\n", encoding="utf-8")
		self.write("Doc.md", "content\n")
		result = self.run_script()
		self.assertEqual(result.returncode, 1)
		self.assertIn("error:", result.stderr)
		self.assertNotIn("No changes", result.stdout)


if __name__ == "__main__":
	unittest.main()
