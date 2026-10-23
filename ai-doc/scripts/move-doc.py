#!/usr/bin/env python3
"""Submodule-aware `git mv` wrapper.

Resolves the nearest repo root (handling submodules, where `.git` is a file)
and runs `git mv` from there. Falls back to a plain filesystem move when the
file isn't tracked by any repo, or when source/destination live in different
repos.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path | None:
	for directory in [start, *start.parents]:
		if (directory / ".git").exists():
			return directory
	return None


def is_tracked(repo_root: Path, path: Path) -> bool:
	rel = path.relative_to(repo_root)
	result = subprocess.run(
		["git", "ls-files", "--error-unmatch", str(rel)],
		cwd=repo_root,
		stdout=subprocess.DEVNULL,
		stderr=subprocess.DEVNULL,
	)
	return result.returncode == 0


def plain_move(source: Path, destination: Path, reason: str) -> int:
	destination.parent.mkdir(parents=True, exist_ok=True)
	shutil.move(str(source), str(destination))
	print(f"note: moved without git history ({reason})", file=sys.stderr)
	return 0


def main() -> int:
	if len(sys.argv) != 3:
		print("usage: move-doc.py <source> <destination>", file=sys.stderr)
		return 2

	source = Path(sys.argv[1]).resolve()
	destination = Path(sys.argv[2]).resolve()

	if not source.exists():
		print(f"error: source does not exist: {source}", file=sys.stderr)
		return 1

	destination.parent.mkdir(parents=True, exist_ok=True)

	source_repo = find_repo_root(source.parent)
	if source_repo is None:
		return plain_move(source, destination, "source not in any git repo")

	dest_repo = find_repo_root(destination.parent if destination.parent.exists() else source.parent)
	if dest_repo != source_repo:
		return plain_move(source, destination, "source and destination in different repos")

	if not is_tracked(source_repo, source):
		return plain_move(source, destination, "source is untracked")

	rel_source = source.relative_to(source_repo)
	rel_destination = destination.relative_to(source_repo)

	result = subprocess.run(
		["git", "mv", str(rel_source), str(rel_destination)],
		cwd=source_repo,
	)
	return result.returncode


if __name__ == "__main__":
	sys.exit(main())
