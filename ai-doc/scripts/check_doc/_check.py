#!/usr/bin/env python3
"""Check local inline links, fences and narrow AiDoc meta/target pairing.

Run from any directory: python3 /path/to/ai-doc/scripts/check_doc DOC [DOC ...]
Only supplied documents receive full checks; companions receive pairing checks.
"""

import argparse
from collections.abc import Iterator
import os
import re
import stat
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
ESCAPE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])")
ResolvedLink = tuple[int, str, Path | None]
DocumentData = tuple[list[ResolvedLink], int | None]


def blank(text: str) -> str:
	return "".join("\n" if char == "\n" else " " for char in text)


def markup(text: str) -> tuple[str, int | None]:
	"""Mask code without moving offsets; retain an unclosed fence's line."""
	lines = text.splitlines(keepends=True)
	opening = None
	regions = []
	offset = start = 0
	for number, line in enumerate(lines, 1):
		body = line.rstrip("\r\n")
		match = FENCE.match(body)
		if opening:
			char, length, _ = opening
			lines[number - 1] = blank(line)
			if match and match[1][0] == char and len(match[1]) >= length and not match[2].strip():
				opening = None
		elif match and not (match[1][0] == "`" and "`" in match[2]):
			opening = (match[1][0], len(match[1]), number)
			lines[number - 1] = blank(line)
		if lines[number - 1] != line or opening:
			regions.append((start, offset))
			start = offset + len(line)
		offset += len(line)
	# Code spans may cross lines, but never a fenced block.
	masked = "".join(lines)
	regions.append((start, len(masked)))
	chars = list(masked)
	for start, end in regions:
		segment = masked[start:end]
		i = 0
		while i < len(segment):
			if segment[i] == "\\":
				i += 2
				continue
			# Recognize code before comments so `<!--` inside a span is literal.
			if segment.startswith("<!--", i):
				closing = segment.find("-->", i + 4)
				stop = len(segment) if closing < 0 else closing + 3
				segment = segment[:i] + blank(segment[i:stop]) + segment[stop:]
				i = stop
				continue
			if segment[i] != "`":
				i += 1
				continue
			j = i + 1
			while j < len(segment) and segment[j] == "`":
				j += 1
			# Inline code may cross a line, but not a blank-line paragraph boundary.
			boundary = re.search(r"\r?\n[ \t]*(?:\r?\n|$)", segment[j:])
			limit = j + boundary.start() if boundary else len(segment)
			closing = re.search(r"(?<!`)`{" + str(j - i) + r"}(?!`)", segment[j:limit])
			if closing:
				stop = j + closing.end()
				segment = segment[:i] + blank(segment[i:stop]) + segment[stop:]
				i = stop
			else:
				i = j
		chars[start:end] = segment
	return "".join(chars), opening[2] if opening else None


def destination(text: str, start: int) -> tuple[str, int] | None:
	"""Parse the bounded inline destination/title subset; reject uncertain syntax."""
	i = start
	while i < len(text) and text[i].isspace():
		i += 1
	if i == len(text):
		return None
	if text[i] == "<":
		begin = i + 1
		i = begin
		while i < len(text) and text[i] not in "<>\n":
			i += 2 if text[i] == "\\" else 1
		if i >= len(text) or text[i] != ">":
			return None
		value = text[begin:i]
		i += 1
	else:
		begin = i
		depth = 0
		while i < len(text):
			char = text[i]
			if char == "\\":
				i += 2
				continue
			if char.isspace() or (char == ")" and depth == 0):
				break
			if char == "(":
				depth += 1
			elif char == ")":
				depth -= 1
			elif char in "<>":
				return None
			i += 1
		if depth:
			return None
		value = text[begin:i]
	separator = i
	while i < len(text) and text[i].isspace():
		i += 1
	if i < len(text) and text[i] == ")":
		return value, i + 1
	if i == separator or i >= len(text) or text[i] not in "\"'(":
		return None
	quote = ")" if text[i] == "(" else text[i]
	i += 1
	while i < len(text) and text[i] != quote:
		i += 2 if text[i] == "\\" else 1
	if i >= len(text):
		return None
	i += 1
	while i < len(text) and text[i].isspace():
		i += 1
	return (value, i + 1) if i < len(text) and text[i] == ")" else None


def is_escaped(text: str, index: int) -> bool:
	backslashes = 0
	index -= 1
	while index >= 0 and text[index] == "\\":
		backslashes += 1
		index -= 1
	return backslashes % 2 == 1


def links(text: str) -> Iterator[tuple[int, str]]:
	"""Yield line/destination for inline links, not images or reference links."""
	i = 0
	while i < len(text):
		if text[i] == "\\":
			i += 2
			continue
		if text[i] != "[":
			i += 1
			continue
		start = i
		image = i > 0 and text[i - 1] == "!" and not is_escaped(text, i - 1)
		i += 1
		depth = 1
		while i < len(text) and depth:
			if text[i] == "\\":
				i += 2
				continue
			if text[i] == "[":
				depth += 1
			elif text[i] == "]":
				depth -= 1
			i += 1
		if depth or i >= len(text) or text[i] != "(":
			# An unmatched '[' is literal and must not swallow later links.
			i = start + 1
			continue
		parsed = destination(text, i + 1)
		if parsed:
			value, i = parsed
			if not image:
				yield text.count("\n", 0, start) + 1, value


def local_path(document: Path, value: str) -> Path | None:
	value = ESCAPE.sub(r"\1", value)
	if not value or value.startswith(("#", "?", "//")) or SCHEME.match(value):
		return None
	# Split before decoding: encoded '?' and '#' belong to the filename.
	file_part = urlsplit(value).path
	if not file_part:
		return None
	file_part = unquote(file_part)
	if file_part.startswith("AI_DOC_PLUGIN/"):
		return (PLUGIN_ROOT / file_part[len("AI_DOC_PLUGIN/"):]).resolve()
	return (document.parent / file_part).resolve()


def display(path: Path) -> str:
	relative = os.path.relpath(path, Path.cwd())
	if relative == os.pardir or relative.startswith(os.pardir + os.sep):
		return str(path)
	return relative


def error_detail(error: Exception) -> str:
	if isinstance(error, OSError) and error.strerror:
		return error.strerror
	return str(error)


def read_document(path: Path) -> str:
	if path.suffix.lower() != ".md":
		raise ValueError("expected a Markdown (.md) file")
	return path.read_text(encoding="utf-8")


def main() -> int:
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("docs", metavar="DOC", nargs="+", help="Markdown file to validate")
	args = parser.parse_args()
	findings = []
	errors = []
	cache: dict[Path, DocumentData | None] = {}

	def load(path: Path) -> DocumentData | None:
		if path not in cache:
			try:
				text = read_document(path)
				visible, fence = markup(text)
				resolved = [(line, value, local_path(path, value)) for line, value in links(visible)]
				cache[path] = (resolved, fence)
			except (OSError, UnicodeError, ValueError, RuntimeError) as error:
				errors.append(f"error: {display(path)}: {error_detail(error)}")
				cache[path] = None
		return cache[path]

	def finding(path: Path, line: int, message: str) -> None:
		findings.append(f"{display(path)}:{line}: {message}")

	def is_file(path: Path) -> bool:
		try:
			return stat.S_ISREG(path.stat().st_mode)
		except (FileNotFoundError, NotADirectoryError):
			return False

	documents: list[Path] = []
	seen: set[Path] = set()
	for argument in args.docs:
		try:
			path = Path(argument).resolve()
		except (OSError, RuntimeError) as error:
			errors.append(f"error: {argument}: {error_detail(error)}")
			continue
		if path not in seen:
			seen.add(path)
			documents.append(path)

	metas: dict[Path, Path] = {}
	for path in documents:
		data = load(path)
		if data is None:
			continue
		is_meta = path.name.endswith(".meta.md")
		target = path.with_name(path.name[:-8] + ".md") if is_meta else None
		if is_meta:
			metas[path] = target
		else:
			meta = path.with_name(path.stem + ".meta.md")
			try:
				has_meta = meta.exists()
			except OSError as error:
				errors.append(f"error: {display(meta)}: {error_detail(error)}")
			else:
				if has_meta:
					metas[meta] = path
		resolved, fence = data
		if fence:
			finding(path, fence, "unclosed code fence")
		for line, value, linked in resolved:
			if linked is None or linked == target:
				continue
			try:
				exists = is_file(linked)
			except OSError as error:
				errors.append(f"error: {display(path)}:{line}: cannot access {display(linked)}: {error_detail(error)}")
			else:
				if not exists:
					finding(path, line, f"missing local file: {value}")
	for meta, target in metas.items():
		data = load(meta)
		if data is not None and not any(linked == target for _, _, linked in data[0]):
			finding(meta, 1, f"missing target reference: {target.name}")
	for item in findings:
		print(item)
	for error in errors:
		print(error, file=sys.stderr)
	return 2 if errors else 1 if findings else 0


if __name__ == "__main__":
	sys.exit(main())
