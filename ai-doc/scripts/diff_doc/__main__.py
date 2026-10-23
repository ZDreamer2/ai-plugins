#!/usr/bin/env python3
"""Show a document and its companion meta's uncommitted changes.

Uses the nearest Git repository, including nested repositories and worktrees.
Existing files are compared against HEAD (staged and unstaged changes together).
New files are reported as added or untracked, without printing their contents.
Only the requested pair is inspected; the index is never modified.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path | None:
	for directory in [start, *start.parents]:
		if (directory / ".git").exists():
			return directory
	return None


def run_git(root: Path, args: list[str], ok_codes: tuple[int, ...] = (0,)) -> str:
	result = subprocess.run(
		["git", "--no-pager", "--literal-pathspecs", *args],
		cwd=root,
		capture_output=True,
		text=True,
	)
	if result.returncode not in ok_codes:
		raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
	return result.stdout


def show_diff(document: Path) -> None:
	root = find_repo_root(document.parent)
	if root is None:
		raise RuntimeError(f"not in a Git repository: {document}")

	meta = document.with_suffix(".meta.md")
	paths = [document, meta]
	names = [str(path.relative_to(root)) for path in paths]
	indexed = set(run_git(root, ["ls-files", "-z", "--", *names]).split("\0"))
	has_head = bool(run_git(root, ["rev-parse", "--verify", "--quiet", "HEAD"], (0, 1)).strip())
	committed = set()
	if has_head:
		committed = set(run_git(root, ["ls-tree", "--name-only", "-z", "HEAD", "--", *names]).split("\0"))

	if not (document.is_file() or document.is_symlink()) and names[0] not in indexed | committed:
		raise RuntimeError(f"document does not exist and is not tracked: {document}")

	output = []
	for path, name in zip(paths, names):
		if path.exists() and not (path.is_file() or path.is_symlink()):
			raise RuntimeError(f"not a file: {path}")

		if name not in committed:
			if name in indexed:
				output.append(f"added: {name}\n")
			elif path.is_file() or path.is_symlink():
				output.append(f"untracked: {name}\n")
			continue

		diff = run_git(root, [
			"diff", "--no-color", "--no-ext-diff", "--no-textconv", "--no-renames",
			"HEAD", "--", name,
		])
		if diff:
			output.append(diff)

	print(f"Repository: {root}")
	if output:
		for section in output:
			print(section, end="" if section.endswith("\n") else "\n")
	else:
		print("No changes in document or meta.")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("document", type=Path, help="Markdown document path, relative to the current directory or absolute")
	arguments = parser.parse_args()
	if arguments.document.suffix != ".md":
		parser.error("expected a Markdown document (.md)")

	try:
		# Resolve directory aliases, but diff a document symlink itself, not its target.
		show_diff(arguments.document.parent.resolve() / arguments.document.name)
	except (OSError, RuntimeError) as error:
		print(f"error: {error}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
