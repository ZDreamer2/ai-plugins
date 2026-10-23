"""Intent: Emit retained values with Symfony default YAML syntax."""

import base64
import math
import re

from . import TaggedValue

_NUMBER = re.compile(
    r"^[ ]*[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?[ ]*$"
)
_DATE = re.compile(
    r"^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}"
    r"(?:(?:[Tt]|[ \t]+)[0-9]{1,2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]*)?"
    r"(?:[ \t]*(?:Z|[-+][0-9]{1,2}(?::[0-9]{2})?))?)?$"
)
_ESCAPES = {
    "\\": "\\\\", '"': '\\"', "\0": "\\0", "\a": "\\a",
    "\b": "\\b", "\t": "\\t", "\n": "\\n", "\v": "\\v",
    "\f": "\\f", "\r": "\\r", "\x1b": "\\e", "\x7f": "\\x7f",
    "\x85": "\\N", "\xa0": "\\_", "\u2028": "\\L", "\u2029": "\\P",
}


def _double_quote(value: str) -> str:
    return '"' + "".join(
        _ESCAPES.get(char, f"\\x{ord(char):02x}" if ord(char) < 32 else char)
        for char in value
    ) + '"'


def _string(value: str | bytes) -> str:
    if isinstance(value, bytes):
        try:
            value = value.decode("utf-8")
        except UnicodeDecodeError:
            return "!!binary " + base64.b64encode(value).decode("ascii")
    try:
        binary = value.encode("utf-8", "surrogateescape")
    except UnicodeEncodeError as error:
        raise ValueError(
            "YAML strings must be UTF-8 or surrogateescaped bytes"
        ) from error
    # Symfony recognizes invalid UTF-8 and non-text control bytes as binary
    # before applying its quoted-string escapes. NUL remains an escaped string.
    if (
        any(0 < ord(char) < 7 or 13 < ord(char) < 27 or 27 < ord(char) < 32
            for char in value)
        or any(0xdc80 <= ord(char) <= 0xdcff for char in value)
    ):
        return "!!binary " + base64.b64encode(binary).decode("ascii")
    if _NUMBER.fullmatch(value):
        return "'" + value + "'"
    if not value:
        return "''"
    if any(char in _ESCAPES and char not in ('"', "\\") for char in value):
        return _double_quote(value)
    single_quote = (
        value.lower() in (
            "null", "~", "true", "false", "y", "n", "yes", "no", "on", "off"
        )
        or value[0] in "-?|<>=!%@`"
        or any(char.isspace() or char in "'\":{}[],&*#?" for char in value)
        or re.fullmatch(r"[0-9][_0-9]*|0x[0-9a-f_]+", value, re.IGNORECASE)
        or _DATE.fullmatch(value)
    )
    if single_quote:
        quoted = "'" + value.replace("'", "''") + "'"
        if "'" in value:
            double = _double_quote(value)
            if len(double.encode("utf-8")) < len(quoted.encode("utf-8")):
                return double
        return quoted
    return value


def _float(value: float) -> str:
    if math.isnan(value):
        return "NAN"
    if math.isinf(value):
        return "-.Inf" if value < 0 else ".Inf"
    # PHP's default string conversion uses precision=14, independent of its
    # serialize_precision setting. Scientific mantissas retain a decimal point.
    result = format(value, ".14g")
    if "e" in result:
        mantissa, exponent = result.split("e")
        if "." not in mantissa:
            mantissa += ".0"
        number = int(exponent)
        return f"{mantissa}E{'+' if number >= 0 else '-'}{abs(number)}"
    return result + ".0" if "." not in result and value.is_integer() else result


def _items(value: dict | list) -> tuple[bool, list[tuple[str | int, object]]]:
    if isinstance(value, list):
        return False, list(enumerate(value))
    normalized = {}
    for key, item in value.items():
        if type(key) not in (str, int):
            raise ValueError("YAML mapping keys must be strings or integers")
        if isinstance(key, str) and re.fullmatch(r"-?(?:0|[1-9][0-9]*)", key):
            integer = int(key)
            if str(integer) == key and -(2 ** 63) <= integer <= 2 ** 63 - 1:
                key = integer
        normalized[key] = item
    items = list(normalized.items())
    return not all(type(key) is int and key == index
                   for index, (key, _) in enumerate(items)), items


def _emit(value: object, inline: int, indent: int, level: int,
          ancestors: set[int]) -> str:
    prefix = " " * level
    if value is None:
        return prefix + "null"
    if type(value) is bool:
        return prefix + ("true" if value else "false")
    if type(value) is int:
        return prefix + str(value)
    if type(value) is float:
        return prefix + _float(value)
    if isinstance(value, (str, bytes)):
        return prefix + _string(value)
    if isinstance(value, TaggedValue):
        if not isinstance(value.tag, str) or not isinstance(value.value, str):
            raise ValueError(
                "Tagged YAML values must contain a string tag and text"
            )
        return prefix + "!" + value.tag + " " + _string(value.value) + (
            "\n" if inline > 0 else ""
        )
    if not isinstance(value, (dict, list)):
        raise ValueError(
            f"Unsupported YAML value type: {type(value).__name__}"
        )
    if id(value) in ancestors:
        raise ValueError("Circular YAML value")
    ancestors.add(id(value))
    try:
        mapping, items = _items(value)
        if not items:
            return prefix + "{  }"
        if inline <= 0:
            values = [
                (f"{_emit(key, 0, indent, 0, ancestors)}: " if mapping else "")
                + _emit(item, 0, indent, 0, ancestors)
                for key, item in items
            ]
            body = ", ".join(values)
            return prefix + (
                "{ " + body + " }" if mapping else "[" + body + "]"
            )
        output = ""
        for key, item in items:
            label = (
                _emit(key, 0, indent, 0, ancestors) + ":" if mapping else "-"
            )
            if isinstance(item, TaggedValue):
                output += (
                    prefix + label + " "
                    + _emit(item, 0, indent, 0, ancestors) + "\n"
                )
                continue
            inlined = (
                inline <= 1 or not isinstance(item, (list, dict)) or not item
            )
            output += prefix + label + (" " if inlined else "\n")
            output += _emit(
                item, inline - 1, indent,
                0 if inlined else level + indent, ancestors,
            )
            if inlined:
                output += "\n"
        return output
    finally:
        ancestors.remove(id(value))


def dump_yaml(value: object, inline: int = 2, indent: int = 4) -> str:
    """Dump scalar, list, mapping and retained tagged values without flags."""
    if type(inline) is not int or type(indent) is not int or indent < 1:
        raise ValueError(
            "YAML inline depth must be an integer and indent must be positive"
        )
    try:
        return _emit(value, inline, indent, 0, set())
    except RecursionError as error:
        raise ValueError("YAML value nesting is too deep") from error
