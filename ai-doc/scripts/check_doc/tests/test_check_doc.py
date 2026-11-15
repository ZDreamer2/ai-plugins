"""CLI tests with temporary fixtures.

From the plugin root: python3 -m unittest discover -s scripts/check_doc/tests -t scripts -v
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


UNIT = Path(__file__).resolve().parents[1]
SCRIPT = UNIT / "__main__.py"


class CheckDocTests(unittest.TestCase):
	def setUp(self):
		self.temporary = tempfile.TemporaryDirectory()
		self.addCleanup(self.temporary.cleanup)
		self.root = Path(self.temporary.name)

	def write(self, name, content=""):
		path = self.root / name
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_text(content, encoding="utf-8")
		return path

	def run_cli(self, *docs, script=SCRIPT, cwd=None, env=None, **kwargs):
		return subprocess.run(
			[sys.executable, str(script), *map(str, docs)], cwd=cwd or self.root,
			capture_output=True, text=True, env=env, **kwargs,
		)

	def check(self, result, status, lines=None):
		self.assertEqual(result.returncode, status, result.stderr + result.stdout)
		if status != 2:
			self.assertEqual(result.stderr, "")
		if lines is not None:
			self.assertEqual(result.stdout.splitlines(), lines)

	def test_existing_relative_file_fragments_queries_and_no_anchor_checks(self):
		self.write("sub/a.md", "[x](../file.md) [y](../file.md#nonexistent)\n"
			"[z](../file.md?raw=1#another) [q](../file.md?raw=1)\n"
			"**bold allowed** __proto__ [self](#unknown)\n")
		self.write("file.md")
		self.check(self.run_cli("sub/a.md"), 0, [])

	def test_missing_file_reports_original_link_and_correct_line(self):
		self.write("sub/a.md", "Heading\n\n[x](gone.md?raw=1#anchor)\n")
		self.check(self.run_cli("sub/a.md"), 1,
			["sub/a.md:3: missing local file: gone.md?raw=1#anchor"])

	def test_multiple_files_and_duplicate_inputs(self):
		self.write("a.md", "[a](one.md)\n")
		self.write("b.md", "\n[b](two.md)\n")
		self.check(self.run_cli("a.md", "b.md", "a.md"), 1, [
			"a.md:1: missing local file: one.md", "b.md:2: missing local file: two.md",
		])

	def test_absolute_input_outside_cwd_stays_absolute(self):
		path = self.write("docs/a.md", "[x](gone.md)")
		cwd = self.root / "elsewhere"
		cwd.mkdir()
		self.check(self.run_cli(path, cwd=cwd), 1,
			[f"{path}:1: missing local file: gone.md"])

	def test_pair_finding_uses_expected_companion_filename(self):
		path = self.write("docs/doc.meta.md", "[x](wrong.md)")
		self.write("docs/wrong.md")
		cwd = self.root / "elsewhere"
		cwd.mkdir()
		self.check(self.run_cli(path, cwd=cwd), 1,
			[f"{path}:1: missing target reference: doc.md"])

	def test_inline_code_runs_and_multiline_spans(self):
		self.write("a.md", "`[x](gone.md)` `` [x](gone.md) `tick` ``\n"
			"```inline [x](gone.md)```` still code ```\n"
			"text `multiline\n[x](gone.md)`\n"
			"text `` [x](gone.md) ``` not closing ``\n")
		self.check(self.run_cli("a.md"), 0, [])

	def test_inline_code_does_not_cross_a_blank_line(self):
		self.write("a.md", "`open\n\n[x](gone.md)\n\nclose`\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:3: missing local file: gone.md"])

	def test_unmatched_inline_ticks_are_literal(self):
		self.write("a.md", "text ` unmatched [x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:1: missing local file: gone.md"])

	def test_escaped_exclamation_does_not_make_link_an_image(self):
		self.write("a.md", "\\![x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:1: missing local file: gone.md"])

	def test_unmatched_label_does_not_hide_a_later_real_link(self):
		self.write("a.md", "a literal [ bracket\n[x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:2: missing local file: gone.md"])

	def test_escaped_ticks_and_links(self):
		self.write("a.md", "\\[x](ignored.md)\n\\` [x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:2: missing local file: gone.md"])

	def test_closed_fences_backticks_tildes_longer_close_and_indentation(self):
		self.write("a.md", "```python\n[x](gone.md)\n````\n"
			"   ~~~~ text\n[x](gone.md)\n~~~\n````\n    ~~~~~\n   ~~~~~\n")
		self.check(self.run_cli("a.md"), 0, [])

	def test_unclosed_fences_report_only_opening_line(self):
		for fence in ("```python", "~~~~"):
			with self.subTest(fence=fence):
				self.write("a.md", "heading\n" + fence + "\n[x](gone.md)\n~~~ nope\n")
				self.check(self.run_cli("a.md"), 1, ["a.md:2: unclosed code fence"])

	def test_fence_close_cannot_have_info_or_use_shorter_run(self):
		self.write("a.md", "````\n```\n```` not a close\n[x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:1: unclosed code fence"])

	def test_inline_spans_cannot_cross_fenced_blocks(self):
		self.write("a.md", "text ` [x](before.md)\n```\nexample\n```\n"
			"[x](after.md) ` text\n")
		self.check(self.run_cli("a.md"), 1, [
			"a.md:1: missing local file: before.md",
			"a.md:5: missing local file: after.md",
		])

	def test_live_link_after_fence_and_inline_code_line_numbers(self):
		self.write("a.md", "```\n[x](ignored.md)\n```\n"
			"`[x](ignored.md)`\n[x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:5: missing local file: gone.md"])

	def test_external_links_and_fragments_are_silent(self):
		self.write("a.md", "[x](https://does-not-exist.invalid/a.md)\n"
			"[x](http://127.0.0.1:1) [x](mailto:foo@example.invalid)\n"
			"[x](ftp://invalid/file) [x](custom:thing) [x](//invalid/a)\n"
			"[x](#nonexistent) [x](?query=1) [x]()\n")
		self.check(self.run_cli("a.md", timeout=5), 0, [])

	def test_plugin_root_from_script_not_cwd_or_environment(self):
		# Copy the package to a temporary plugin to avoid writing fixture files
		# into the checkout or relying on any existing plugin documents.
		script = self.root / "plugin/scripts/check_doc/__main__.py"
		shutil.copytree(UNIT, script.parent, ignore=shutil.ignore_patterns("__pycache__"))
		self.write("plugin/real.md")
		self.write("unrelated/doc.md", "[x](AI_DOC_PLUGIN/real.md#no-anchor)\n"
			"[x](AI_DOC_PLUGIN/gone.md?query)\n")
		env = dict(os.environ, AI_DOC_PLUGIN=str(self.root / "wrong"))
		self.check(self.run_cli("doc.md", script=script, cwd=self.root / "unrelated", env=env), 1,
			["doc.md:2: missing local file: AI_DOC_PLUGIN/gone.md?query"])

	def test_balanced_escaped_angle_and_encoded_destinations_with_titles(self):
		self.write("a.md", '[x](file(one).md) [x](file\\(one\\).md)\n'
			'[x](<space name.md> "Title") [x](space%20name.md \'Title\')\n'
			'[nested [label]](file(one).md (Title))\n'
			'[x](hash%23question%3F.md#anchor)\n')
		for name in ("file(one).md", "space name.md", "hash#question?.md"):
			self.write(name)
		self.check(self.run_cli("a.md"), 0, [])

	def test_unsupported_reference_links_images_comments_and_malformed_links_are_silent(self):
		self.write("a.md", "[x][ref]\n[ref]: gone.md\n![x](gone.md)\n"
			"<!-- [x](gone.md) -->\n[x](<unclosed)\n[x](a b c)\n")
		self.check(self.run_cli("a.md"), 0, [])

	def test_comment_marker_inside_inline_code_does_not_hide_live_link(self):
		self.write("a.md", "`<!--` [x](gone.md)\n")
		self.check(self.run_cli("a.md"), 1, ["a.md:1: missing local file: gone.md"])

	def test_target_without_companion_is_silent(self):
		self.write("doc.md", "# Target\n")
		self.check(self.run_cli("doc.md"), 0, [])

	def test_plugin_target_link_satisfies_meta_pairing(self):
		script = self.root / "plugin/scripts/check_doc/__main__.py"
		shutil.copytree(UNIT, script.parent, ignore=shutil.ignore_patterns("__pycache__"))
		self.write("plugin/doc.meta.md", "[target](AI_DOC_PLUGIN/doc.md#future)")
		self.check(self.run_cli("plugin/doc.meta.md", script=script), 0, [])

	def test_meta_first_missing_target_is_silent(self):
		self.write("doc.meta.md", "[planned](doc.md#future)\n")
		self.check(self.run_cli("doc.meta.md"), 0, [])

	def test_meta_suppresses_only_expected_target(self):
		self.write("doc.meta.md", "[planned](doc.md)\n[other](other.md)\n")
		self.check(self.run_cli("doc.meta.md"), 1,
			["doc.meta.md:2: missing local file: other.md"])

	def test_incorrect_reference_is_a_pair_finding_with_or_without_target(self):
		self.write("wrong.md")
		self.write("doc.meta.md", "[target](wrong.md)\n")
		for exists in (False, True):
			with self.subTest(target_exists=exists):
				if exists:
					self.write("doc.md")
				self.check(self.run_cli("doc.meta.md"), 1,
					["doc.meta.md:1: missing target reference: doc.md"])

	def test_missing_wrong_reference_yields_link_and_pair_findings(self):
		self.write("doc.meta.md", "[target](wrong.md)\n")
		self.check(self.run_cli("doc.meta.md"), 1, [
			"doc.meta.md:1: missing local file: wrong.md",
			"doc.meta.md:1: missing target reference: doc.md",
		])

	def test_unsupplied_meta_receives_only_pair_check(self):
		self.write("doc.md")
		self.write("doc.meta.md", "[target](doc.md) [other](gone.md)\n```\n")
		self.check(self.run_cli("doc.md"), 0, [])
		self.write("doc.meta.md", "[wrong](gone.md)\n")
		self.check(self.run_cli("doc.md"), 1,
			["doc.meta.md:1: missing target reference: doc.md"])

	def test_unsupplied_target_links_are_not_checked(self):
		self.write("doc.md", "[x](gone.md)\n```\n")
		self.write("doc.meta.md", "[target](doc.md)")
		self.check(self.run_cli("doc.meta.md"), 0, [])

	def test_format_meta_naming_and_duplicate_pair_suppression(self):
		self.write("doc.format.md")
		self.write("doc.format.meta.md", "[wrong](doc.md)")
		self.write("doc.md")
		for docs in (("doc.format.md", "doc.format.meta.md"),
				("doc.format.meta.md", "doc.format.md")):
			self.check(self.run_cli(*docs), 1,
				["doc.format.meta.md:1: missing target reference: doc.format.md"])
		self.write("doc.format.meta.md", "[target](./doc.format.md?raw=1#section)")
		self.check(self.run_cli("doc.format.md", "doc.format.meta.md"), 0, [])

	def test_code_examples_do_not_satisfy_pair_reference(self):
		self.write("doc.meta.md", "`[target](doc.md)`\n~~~\n[target](doc.md)\n~~~")
		self.check(self.run_cli("doc.meta.md"), 1,
			["doc.meta.md:1: missing target reference: doc.md"])

	def test_invalid_invocation_and_help(self):
		for args in ((), ("--unknown",), ("--forbid-bold", "a.md")):
			with self.subTest(args=args):
				result = self.run_cli(*args)
				self.check(result, 2, [])
				self.assertIn("usage:", result.stderr)
		result = self.run_cli("--help")
		self.check(result, 0)
		self.assertIn("DOC", result.stdout)

	def test_missing_invalid_directory_and_non_utf8_documents_are_errors(self):
		self.write("bad.txt", "not Markdown")
		(self.root / "directory.md").mkdir()
		(self.root / "binary.md").write_bytes(b"\xff")
		for name in ("gone.md", "bad.txt", "directory.md", "binary.md"):
			with self.subTest(name=name):
				result = self.run_cli(name)
				self.check(result, 2, [])
				self.assertIn("error:", result.stderr)
				self.assertIn(name, result.stderr)
				self.assertNotIn("[Errno", result.stderr)
		result = self.run_cli("gone.md")
		self.assertEqual(result.stderr, f"error: gone.md: {os.strerror(2)}\n")

	def test_unreadable_document_operational_error(self):
		path = self.write("private.md")
		path.chmod(0)
		self.addCleanup(path.chmod, 0o600)
		if os.access(path, os.R_OK):
			self.skipTest("current user can read mode-000 files")
		result = self.run_cli("private.md")
		self.check(result, 2, [])
		self.assertIn("private.md", result.stderr)

	def test_operational_error_does_not_hide_other_documents_findings(self):
		self.write("a.md", "[x](gone.md)")
		result = self.run_cli("absent.md", "a.md")
		self.check(result, 2, ["a.md:1: missing local file: gone.md"])
		self.assertIn("absent.md", result.stderr)

	def test_path_resolution_error_does_not_hide_other_documents_findings(self):
		(self.root / "loop.md").symlink_to("loop.md")
		self.write("a.md", "[x](gone.md)")
		result = self.run_cli("loop.md", "a.md")
		self.check(result, 2, ["a.md:1: missing local file: gone.md"])
		self.assertIn("loop.md", result.stderr)

	def test_unreadable_companion_is_an_operational_error(self):
		self.write("doc.md")
		(self.root / "doc.meta.md").write_bytes(b"\xff")
		result = self.run_cli("doc.md")
		self.check(result, 2, [])
		self.assertIn("doc.meta.md", result.stderr)


if __name__ == "__main__":
	unittest.main()
