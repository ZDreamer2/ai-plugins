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
import os
import sys
from pathlib import Path
from typing import Iterator

DEFAULT_EXCLUDES: tuple[str, ...] = (".git", "node_modules", "vendor")


def walk_files(root: Path, excludes: set[str]) -> Iterator[Path]:
	for dirpath, dirnames, filenames in os.walk(root):
		dirnames[:] = [name for name in dirnames if name not in excludes]
		for name in filenames:
			yield Path(dirpath) / name


def read_text(path: Path) -> str | None:
	"""Returns None for unreadable and binary files, mirroring `grep -I`."""
	try:
		data = path.read_bytes()
	except OSError:
		return None

	if b"\0" in data[:8192]:
		return None

	return data.decode("utf-8", errors="replace")


def collect(root: Path, fragment: str, excludes: set[str]) -> list[tuple[Path, int]]:
	matches = []

	for path in walk_files(root, excludes):
		text = read_text(path)
		if text is None:
			continue

		count = text.count(fragment)
		if count > 0:
			matches.append((path, count))

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
