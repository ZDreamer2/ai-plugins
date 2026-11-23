import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).with_name("find-doc.py")
MODULE = runpy.run_path(str(SCRIPT))["collect"].__globals__


class FindDocTest(unittest.TestCase):
	def setUp(self):
		tmp = tempfile.TemporaryDirectory()
		self.addCleanup(tmp.cleanup)
		self.root = Path(tmp.name)
		self.excludes = set(MODULE["DEFAULT_EXCLUDES"]) | {"skip[1]"}

	def write(self, name, data):
		path = self.root / name
		path.parent.mkdir(parents=True, exist_ok=True)
		path.write_bytes(data)
		return path

	def test_coverage_and_counts(self):
		head = b"x" * 8192
		fragment = "éé"
		literal = fragment.encode()
		self.write(".gitignore", b"nested/\n")
		self.write("nested/.git/config", literal)
		self.write("nested/.hidden", head + b"\xff\0" + "ééééé".encode())
		self.write("nested/.binary", head[:-1] + b"\0" + literal)
		self.write("vendor/ignored", literal)
		self.write("skip[1]/ignored", literal)
		self.write("skip1/kept", literal)
		self.write("nested/vendor", literal)
		odd_name = "odd:\nname" if os.name == "posix" else "odd-name"
		self.write(odd_name, head[:-1] + literal)
		# No BOM transcoding: the original scanner decodes all input as UTF-8.
		self.write("bom", b"\xff\xfe" + head + literal)
		if os.name == "posix":
			(self.root / "file-link").symlink_to("nested/.hidden")
			(self.root / "dir-link").symlink_to("nested", target_is_directory=True)
			(self.root / "broken-link").symlink_to("missing")
			os.mkfifo(self.root / "fifo")

		expected = {"nested/.hidden": 2, "skip1/kept": 1, "nested/vendor": 1,
		            odd_name: 1, "bom": 1}
		if os.name == "posix":
			expected["file-link"] = 2
		for backend in [None, shutil.which("rg")]:
			with self.subTest(backend=backend), patch.dict(MODULE, {"RG_MIN_SIZE": 8192}), \
			     patch.object(shutil, "which", return_value=backend):
				matches = MODULE["collect"](self.root, fragment, self.excludes)
				self.assertEqual(matches, sorted((self.root / name, count) for name, count in expected.items()))

	def test_streaming_matches_full_decode(self):
		data = b"aaa\xff\xe2\x82\xacaaa\r\n\0\xf0\x9f"
		path = self.write("text", data)
		with patch.dict(MODULE, {"PROBE_SIZE": 3, "READ_SIZE": 2}):
			for fragment in ["", "aa", "a\ufffd€a", "\ufffd", "\r\n\0", "aaa", "missing"]:
				with self.subTest(fragment=fragment):
					self.assertEqual(MODULE["count_file"](path, fragment), data.decode("utf-8", "replace").count(fragment))

	def test_rg_failure_uses_python(self):
		path = self.write("large", b"x" * 8192 + b"needle")
		for result in [subprocess.CompletedProcess([], 2, b"", b"error"),
		               subprocess.CompletedProcess([], 0, b"unknown\0", b"")]:
			with patch.dict(MODULE, {"RG_MIN_SIZE": 8192}), \
			     patch.object(shutil, "which", return_value="rg"), \
			     patch.object(subprocess, "run", return_value=result):
				self.assertEqual(MODULE["collect"](self.root, "needle", self.excludes), [(path, 1)])

	def test_oversized_files_are_still_searched(self):
		path = self.write("large", b"x" * 8192 + b"needle")
		with patch.dict(MODULE, {"RG_MIN_SIZE": 8192, "RG_MAX_SIZE": 8192}), \
		     patch.object(shutil, "which", return_value="rg"), \
		     patch.object(subprocess, "run") as run:
			self.assertEqual(MODULE["collect"](self.root, "needle", self.excludes), [(path, 1)])
			run.assert_not_called()

	def test_cli(self):
		self.write("b", b"needle needle")
		self.write("a", b"needle")
		for fragment, status, output in [("needle", 0, "a  1\nb  2\n"), ("absent", 1, "")]:
			result = subprocess.run([sys.executable, SCRIPT, fragment], cwd=self.root, capture_output=True, text=True)
			self.assertEqual(result.returncode, status)
			self.assertEqual(result.stdout, f"searched {self.root.resolve()}\n" + output)
		result = subprocess.run([sys.executable, SCRIPT, "needle", self.root / "missing"], capture_output=True)
		self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
	unittest.main()
