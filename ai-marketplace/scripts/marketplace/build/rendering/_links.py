"""Rebase authored Markdown destinations without changing literal code or prose."""

import posixpath
import re


_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_DEFINITION = re.compile(r"^ {0,3}\[[^\]\n]+\]:[ \t]*")
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def rebase_links(text: str, source: str, destination: str) -> str:
    """Move relative link targets from source's logical directory to destination's."""
    source_dir = posixpath.dirname(source)
    destination_dir = posixpath.dirname(destination)
    if source_dir == destination_dir:
        return text
    result: list[str] = []
    prose: list[str] = []
    fence_char = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = _FENCE.match(line)
        literal = bool(fence_char or match or line.startswith(("    ", "\t")))
        if fence_char:
            if (match and match.group(1)[0] == fence_char
                    and len(match.group(1)) >= fence_length
                    and not match.group(2).strip()):
                fence_char = ""
        elif match:
            fence_char = match.group(1)[0]
            fence_length = len(match.group(1))
        if literal or not line.strip():
            if prose:
                result.append(_rebase_prose("".join(prose), source_dir, destination_dir))
                prose.clear()
            result.append(line)
        else:
            prose.append(line)
    if prose:
        result.append(_rebase_prose("".join(prose), source_dir, destination_dir))
    return "".join(result)


def _rebase_prose(text: str, source_dir: str, destination_dir: str) -> str:
    """Rebase a prose block while masking code spans across its lines."""
    mask = _code_mask(text)
    result: list[str] = []
    offset = 0
    for line in text.splitlines(keepends=True):
        protected = mask[offset:offset + len(line)]
        offset += len(line)
        definition = _DEFINITION.match(line)
        if definition and not any(protected[:definition.end()]):
            start = definition.end()
            end, value = _destination(line, start, definition=True)
            if end != start:
                path_start = start + (line[start] == "<")
                line = (line[:path_start] + _rebase(value, source_dir, destination_dir)
                        + line[end:])
                result.append(line)
                continue
        result.append(_inline_links(line, protected, source_dir, destination_dir))
    return "".join(result)


def _code_mask(line: str) -> list[bool]:
    """Mask paired backtick spans, including their delimiters."""
    mask = [False] * len(line)
    index = 0
    while index < len(line):
        if line[index] != "`" or _escaped(line, index):
            index += 1
            continue
        end = index
        while end < len(line) and line[end] == "`":
            end += 1
        width = end - index
        close = end
        while close < len(line):
            if line[close] != "`":
                close += 1
                continue
            after = close
            while after < len(line) and line[after] == "`":
                after += 1
            if after - close == width:
                mask[index:after] = [True] * (after - index)
                index = after
                break
            close = after
        else:
            index = end
    return mask


def _escaped(text: str, index: int) -> bool:
    start = index
    while start and text[start - 1] == "\\":
        start -= 1
    return (index - start) % 2 == 1


def _destination(line: str, start: int, *, definition: bool = False) -> tuple[int, str]:
    """Return the destination's end and original spelling, excluding angle brackets."""
    if start >= len(line):
        return start, ""
    if line[start] == "<":
        end = start + 1
        while end < len(line):
            if line[end] == ">" and not _escaped(line, end):
                return end, line[start + 1:end]
            if line[end] in "\r\n":
                break
            end += 1
        return start, ""
    end = start
    depth = 0
    while end < len(line):
        char = line[end]
        if char in "\r\n" or (char in " \t" and not _escaped(line, end)):
            break
        if char == "(" and not _escaped(line, end):
            depth += 1
        elif char == ")" and not _escaped(line, end):
            if depth == 0:
                break
            depth -= 1
        end += 1
    if depth or (not definition and end == start):
        return start, ""
    return end, line[start:end]


def _rebase(value: str, source_dir: str, destination_dir: str) -> str:
    if (not value or value.startswith(("/", "\\", "#", "?"))
            or _SCHEME.match(value)):
        return value
    suffix_at = min((index for char in ("?", "#")
                     if (index := value.find(char)) >= 0), default=len(value))
    path, suffix = value[:suffix_at], value[suffix_at:]
    if not path:
        return value
    target = posixpath.normpath(posixpath.join(source_dir, path))
    return posixpath.relpath(target, destination_dir or ".") + suffix


def _inline_links(line: str, protected: list[bool], source_dir: str,
                  destination_dir: str) -> str:
    replacements: list[tuple[int, int, str]] = []
    index = 0
    while index < len(line) - 1:
        if line[index:index + 2] != "](" or protected[index] or _escaped(line, index):
            index += 1
            continue
        # Require an unescaped opening label outside code, optionally preceded by '!'.
        opening = index - 1
        depth = 0
        while opening >= 0:
            if not protected[opening] and not _escaped(line, opening):
                if line[opening] == "]":
                    depth += 1
                elif line[opening] == "[":
                    if not depth:
                        break
                    depth -= 1
            opening -= 1
        if (opening < 0 or line[opening] != "[" or protected[opening]
                or _escaped(line, opening)):
            index += 2
            continue
        start = index + 2
        while start < len(line) and line[start] in " \t":
            start += 1
        end, value = _destination(line, start)
        closing = end + 1 if start < len(line) and line[start] == "<" else end
        tail = line[closing:] if closing < len(line) else ""
        valid_title = re.match(r"[ \t]+(?:\"[^\"\r\n]*\"|'[^'\r\n]*'|\([^()\r\n]*\))[ \t]*\)", tail)
        if end != start and (re.match(r"[ \t]*\)", tail) or valid_title):
            replacements.append((start + (line[start] == "<"), end,
                                 _rebase(value, source_dir, destination_dir)))
            index = end + 1
        else:
            index += 2
    for start, end, value in reversed(replacements):
        line = line[:start] + value + line[end:]
    return line
