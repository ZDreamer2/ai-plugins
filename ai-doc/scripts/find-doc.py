#!/usr/bin/env python3
"""Reference finder for doc moves.

Lists every file containing a path fragment, with its match count.

Traversal deliberately ignores `.gitignore`. Sibling repositories checked out
inside a project are usually ignored by the parent, yet their AiDocs reference
the project's docs by project-root path - so they hold the references most
likely to break, and an ignore-aware search omits them without saying so.

Prints the searched root, because a run started from the wrong directory
returns a short and entirely plausible list.

Exits 1 when nothing matches.
"""

import argparse
import codecs
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Iterator

DEFAULT_EXCLUDES: tuple[str, ...] = (".git", "node_modules", "vendor")
PROBE_SIZE = 8192
READ_SIZE = 1024 * 1024
RG_MIN_SIZE = READ_SIZE
RG_MAX_SIZE = 128 * 1024 * 1024  # rg can buffer an entire line; cap its input size.
PATH_BATCH_BYTES = 64 * 1024


def walk_files(root: Path, excludes: set[str]) -> Iterator[Path]:
	for dirpath, dirnames, filenames in os.walk(root):
		dirnames[:] = [name for name in dirnames if name not in excludes]
		for name in filenames:
			yield Path(dirpath) / name


def count_file(path: Path, fragment: str) -> int:
	"""Count exactly as str.count, without loading the entire file."""
	decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
	count = 0 if fragment else 1
	tail = ""
	try:
		with path.open("rb") as file:
			data = file.read(PROBE_SIZE)
			if b"\0" in data:
				return 0
			while True:
				text = tail + decoder.decode(data, final=not data)
				if fragment:
					start = 0
					while (match := text.find(fragment, start)) != -1:
						count += 1
						start = match + len(fragment)
					# Retain only the unconsumed characters that could start a match.
					tail = text[max(start, len(text) - len(fragment) + 1):]
				else:
					count += len(text)
				if not data:
					return count
				data = file.read(READ_SIZE)
	except OSError:
		return 0


def rg_candidates(rg: str, paths: list[Path], fragment: str) -> list[Path]:
	# Use explicit paths so traversal and directory exclusions stay identical.
	# Probe before calling rg, then disable its different binary and encoding
	# heuristics. rg only discovers candidates; Python computes exact counts.
	try:
		result = subprocess.run(
			[rg, "--no-config", "--encoding", "none", "--text", "--no-mmap",
			 "--files-with-matches", "--null", "--fixed-strings", "-e", fragment, "--", *paths],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
		)
	except OSError:
		return paths
	if result.returncode not in (0, 1) or result.stderr:
		return paths
	if result.returncode == 1:
		return paths if result.stdout else []
	if not result.stdout.endswith(b"\0"):
		return paths
	candidates = {Path(os.fsdecode(name)) for name in result.stdout[:-1].split(b"\0")}
	return list(candidates) if candidates.issubset(paths) else paths


def collect(root: Path, fragment: str, excludes: set[str]) -> list[tuple[Path, int]]:
	# Matches on replacement characters may have no literal UTF-8 counterpart.
	# Empty, multiline and NUL-containing patterns also need Python semantics.
	rg = shutil.which("rg") if fragment and not any(c in fragment for c in "\r\n\0\ufffd") else None
	matches = []
	batch: list[Path] = []
	batch_bytes = 0

	def flush_batch() -> None:
		assert rg is not None
		for path in rg_candidates(rg, batch, fragment):
			if count := count_file(path, fragment):
				matches.append((path, count))
		batch.clear()

	for path in walk_files(root, excludes):
		try:
			info = path.stat()
			if not stat.S_ISREG(info.st_mode):
				continue
			with path.open("rb") as file:
				head = file.read(PROBE_SIZE)
				if b"\0" in head:
					continue
				# Most paths are small. Count them in the initial open instead
				# of asking rg to reopen them. Bound the read even if size is stale.
				if info.st_size < RG_MIN_SIZE:
					data = head + file.read(RG_MIN_SIZE - len(head))
					if len(data) < RG_MIN_SIZE:
						if count := data.decode("utf-8", errors="replace").count(fragment):
							matches.append((path, count))
						continue
		except OSError:
			continue
		if not rg or info.st_size > RG_MAX_SIZE:
			if count := count_file(path, fragment):
				matches.append((path, count))
			continue
		batch.append(path)
		batch_bytes += len(os.fsencode(path)) + 1
		if batch_bytes >= PATH_BATCH_BYTES:
			flush_batch()
			batch_bytes = 0
	if batch:
		flush_batch()
	return sorted(matches)


def main() -> int:
	parser = argparse.ArgumentParser(description="Find files referencing a path fragment.")
	parser.add_argument("fragment", help="literal path fragment to find, e.g. Some/Module/oldName")
	parser.add_argument("root", nargs="?", default=".", help="directory to search (default: current)")
	parser.add_argument(
		"--exclude",
		action="append",
		default=[],
		metavar="NAME",
		help=f"directory name to skip, repeatable; always skipped: {', '.join(DEFAULT_EXCLUDES)}",
	)
	arguments = parser.parse_args()

	root = Path(arguments.root).resolve()
	if not root.is_dir():
		print(f"error: not a directory: {root}", file=sys.stderr)
		return 2

	matches = collect(
		root=root,
		fragment=arguments.fragment,
		excludes=set(DEFAULT_EXCLUDES) | set(arguments.exclude),
	)

	print(f"searched {root}")
	if not matches:
		return 1

	for path, count in matches:
		print(f"{path.relative_to(root)}  {count}")

	return 0


if __name__ == "__main__":
	sys.exit(main())
