"""Splice shared and host-selected documents using consuming logical paths."""

import os
import posixpath
from typing import NoReturn

from marketplace.source import SourceInventory

from ._links import rebase_links
from ._placeholders import MARKER_PATTERN, fail, parse


_PHP_TRIM = " \t\n\r\x00\x0b"


def splice(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
    plugin_root: str | None,
) -> str:
    """Validate all includes, including ones omitted for the current host."""
    lines = _lines(content)
    frontmatter_end = _frontmatter_end(lines)
    included = False
    for index, line in enumerate(lines):
        include = _include_on(line, logical_path)
        if include is None:
            continue
        marker, name, argument = include
        line_number = index + 1
        if index < frontmatter_end:
            _fail(
                marker, logical_path, line_number,
                "sits in the frontmatter, where nothing can be included",
            )
        lines[index] = _replacement(
            line, name, argument, marker, logical_path, line_number,
            plugin_root or ".", host, inventory,
        )
        included = True
    return "".join(lines) if included else content


def _lines(content: str) -> list[str]:
    """Split only after LF, retaining every other character and final LF."""
    pieces = content.split("\n")
    return [piece + "\n" for piece in pieces[:-1]] + [pieces[-1]]


def _frontmatter_end(lines: list[str]) -> int:
    if lines[0] != "---\n":
        return 0
    for index in range(1, len(lines)):
        if lines[index] == "---\n":
            return index + 1
    return 0


def _include_on(line: str, logical_path: str) -> tuple[str, str, str] | None:
    for match in MARKER_PATTERN.finditer(line):
        if match.group("escaped"):
            continue
        marker = match.group(0)
        name, argument = parse(marker, logical_path)
        if name in ("INCLUDE_DOC_FOR", "INCLUDE_DOC"):
            return marker, name, argument or ""
    return None


def _replacement(
    line: str, name: str, argument: str, marker: str, logical_path: str,
    line_number: int, plugin_root: str, host: str,
    inventory: SourceInventory,
) -> str:
    if line.strip(_PHP_TRIM) != marker:
        _fail(
            marker, logical_path, line_number,
            "shares its line with other text: an include stands alone on its line",
        )
    if name == "INCLUDE_DOC_FOR":
        parts = argument.split(",", 1)
        tree = parts[0].strip(_PHP_TRIM)
        path = parts[1].strip(_PHP_TRIM) if len(parts) == 2 else ""
        if tree not in ("claude", "codex", "pi"):
            _fail(
                marker, logical_path, line_number,
                "names no agent tree: write claude or codex or pi",
            )
    else:
        tree = host
        path = argument.strip(_PHP_TRIM)
    document_path = _document_path(
        path, marker, logical_path, line_number, plugin_root,
    )
    text = _document_text(
        document_path, marker, logical_path, line_number, inventory,
    )
    if tree != host:
        return ""
    text = rebase_links(text, document_path, logical_path).rstrip("\n")
    return text + "\n" if line.endswith("\n") else text


def _document_path(
    path: str, marker: str, logical_path: str,
    line_number: int, plugin_root: str,
) -> str:
    if not path or path.startswith("/") or not path.endswith(".md"):
        _fail(
            marker, logical_path, line_number,
            "names no document-relative path to a `.md` file",
        )
    segments: list[str] = []
    relative = posixpath.dirname(logical_path) + "/" + path
    for segment in relative.split("/"):
        if segment in ("", "."):
            continue
        if segment != "..":
            segments.append(segment)
        elif not segments:
            _fail(
                marker, logical_path, line_number,
                f"names '{path}', which leaves the plugin source",
            )
        else:
            segments.pop()
    document_path = "/".join(segments)
    if plugin_root != "." and not document_path.startswith(plugin_root + "/"):
        _fail(
            marker, logical_path, line_number,
            f"names '{document_path}', outside the plugin '{plugin_root}'",
        )
    return document_path


def _document_text(
    document_path: str, marker: str, logical_path: str,
    line_number: int, inventory: SourceInventory,
) -> str:
    path = inventory.directory / document_path
    try:
        text = (
            path.read_bytes().decode("utf-8", "surrogateescape")
            if path.is_file() and os.access(path, os.R_OK) else None
        )
    except (OSError, ValueError):
        text = None
    if text is None:
        _fail(
            marker, logical_path, line_number,
            f"names '{document_path}', which is not a readable file",
        )
    for line in _lines(text):
        if _include_on(line, document_path) is not None:
            _fail(
                marker, logical_path, line_number,
                f"names '{document_path}', which includes another document: "
                "an included document includes nothing",
            )
    return text


def _fail(
    marker: str, logical_path: str, line_number: int, reason: str,
) -> NoReturn:
    fail(marker, logical_path, f"on line {line_number} {reason}")
