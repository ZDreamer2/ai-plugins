"""Intent: Preserve Symfony's default YAML values without unsafe constructors."""

import base64
import binascii
from datetime import datetime, timedelta, timezone
import math
import re

from . import TaggedValue
from ._vendor.yaml import BaseLoader, YAMLError
from ._vendor.yaml.events import AliasEvent, Event
from ._vendor.yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode
from ._vendor.yaml.tokens import (
    AnchorToken, BlockEntryToken, DocumentStartToken, FlowEntryToken,
    StreamStartToken, Token, ValueToken,
)

_TAG = "tag:yaml.org,2002:"
_PLAIN = "marketplace:plain"
_INT_MIN = -(2 ** 63)
_INT_MAX = 2 ** 63 - 1
_NUMBER = re.compile(
    r"^[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?$"
)
_FLOAT_PREFIX = re.compile(
    r"^[ \t]*([+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)"
)
_TIMESTAMP = re.compile(
    r"^(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})"
    r"(?:(?:[Tt]|[ \t]+)(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})"
    r":(?P<second>[0-9]{2})(?:\.(?P<fraction>[0-9]*))?"
    r"(?:[ \t]*(?:Z|(?P<sign>[-+])(?P<tz_hour>[0-9]{1,2})"
    r"(?::(?P<tz_minute>[0-9]{2}))?))?)?$"
)


class _Loader(BaseLoader):
    """Compose nodes with local resolution; never call YAML constructors."""

    def __init__(self, stream: str) -> None:
        self._recent_tokens: list[Token] = []
        self._ignore_flow_suffix = False
        super().__init__(stream)

    def get_token(self) -> Token | None:
        token = super().get_token()
        if token is not None:
            self._recent_tokens = (self._recent_tokens + [token])[-2:]
        return token

    def fetch_flow_collection_start(self, token_class: type[Token]) -> None:
        if not self.flow_level:
            preceding = self._recent_tokens + self.tokens
            previous = preceding[-1] if preceding else None
            # Parser::parseValue extracts a block anchor before lexing a flow
            # value. Tags instead go through Inline::parse, which checks tails.
            if isinstance(previous, AnchorToken) and len(preceding) > 1:
                previous = preceding[-2]
                self._ignore_flow_suffix = isinstance(
                    previous, (ValueToken, BlockEntryToken)
                ) and previous.start_mark.line == preceding[-1].start_mark.line
            else:
                self._ignore_flow_suffix = isinstance(
                    previous,
                    (ValueToken, BlockEntryToken, StreamStartToken, DocumentStartToken),
                )
        super().fetch_flow_collection_start(token_class)

    def fetch_flow_collection_end(self, token_class: type[Token]) -> None:
        super().fetch_flow_collection_end(token_class)
        if not self.flow_level and self._ignore_flow_suffix:
            # Symfony's lexInlineStructure returns at the outer closing token;
            # Parser ignores the rest of that physical line. Let the scanner
            # find that token (respecting nesting, quotes and comments), rather
            # than rewriting source text or touching block-scalar contents.
            while self.peek() not in "\0\r\n\x85\u2028\u2029":
                self.forward()
            self._ignore_flow_suffix = False

    def parse_flow_sequence_entry(self, first: bool = False) -> Event:
        # Symfony treats an omitted flow-sequence entry as null. Handle actual
        # separator tokens so commas inside quoted strings are untouched.
        if self.check_token(FlowEntryToken):
            if not first:
                self.get_token()
                if not self.check_token(FlowEntryToken):
                    return super().parse_flow_sequence_entry(first=True)
            self.state = self.parse_flow_sequence_entry
            return self.process_empty_scalar(self.peek_token().start_mark)
        return super().parse_flow_sequence_entry(first=first)

    def resolve(
        self, kind: type, value: object, implicit: bool | tuple[bool, bool]
    ) -> str:
        if kind is ScalarNode and implicit[0]:
            return _PLAIN
        return super().resolve(kind, value, implicit)

    def compose_node(self, parent: Node | None, index: object) -> Node:
        # Symfony permits a later definition to replace an anchor.
        alias = self.check_event(AliasEvent)
        if not alias:
            event = self.peek_event()
            anchor = event.anchor
            if anchor is not None:
                self.anchors.pop(anchor, None)
        node = super().compose_node(parent, index)
        if not alias:
            node.anchor = anchor
            node.definition_context = (
                "mapping" if isinstance(parent, MappingNode)
                else "sequence" if isinstance(parent, SequenceNode)
                else "root"
            )
            node.header = event.start_mark.buffer[
                event.start_mark.pointer:
            ].split("\n", 1)[0]
            if (
                anchor and isinstance(parent, MappingNode)
                and not parent.flow_style and isinstance(index, ScalarNode)
                and index.value == "<<" and node.header.strip() != "&" + anchor
            ):
                # Inline content under an anchored block merge key is ignored
                # by Symfony, and its anchor is not made available to aliases.
                self.anchors.pop(anchor, None)
        return node

    def compose_scalar_node(self, anchor: str | None) -> ScalarNode:
        tag = self.peek_event().tag
        node = super().compose_scalar_node(anchor)
        node.explicit_tag = tag
        return node

    def compose_sequence_node(self, anchor: str | None) -> SequenceNode:
        tag = self.peek_event().tag
        node = super().compose_sequence_node(anchor)
        node.explicit_tag = tag
        return node

    def compose_mapping_node(self, anchor: str | None) -> MappingNode:
        tag = self.peek_event().tag
        node = super().compose_mapping_node(anchor)
        node.explicit_tag = tag
        return node


def _error(node: Node, message: str) -> ValueError:
    return ValueError(f"{message} at line {node.start_mark.line + 1}")


def _bounded_integer(value: int) -> int | float:
    if _INT_MIN <= value <= _INT_MAX:
        return value
    try:
        return float(value)
    except OverflowError:
        return -math.inf if value < 0 else math.inf


def _timestamp(value: str, match: re.Match) -> int | float:
    parts = match.groupdict()
    year, month, day = (int(parts[name]) for name in ("year", "month", "day"))
    hour, minute, second = (
        int(parts[name] or 0) for name in ("hour", "minute", "second")
    )
    tz_hour, tz_minute = int(parts["tz_hour"] or 0), int(parts["tz_minute"] or 0)
    if (
        month > 12 or day > 31 or hour > 24 or minute > 59 or second > 60
        or tz_hour > 24 or tz_minute > 59
    ):
        raise ValueError(f"Invalid YAML timestamp {value!r}")
    offset = tz_hour * 60 + tz_minute
    if parts["sign"] == "-":
        offset = -offset
    # PHP accepts day overflow (for example February 30) and normalizes it.
    if month == 0:
        year, month = year - 1, 12
    # Use the Gregorian 400-year cycle for PHP dates before Python's year 1.
    cycle = 400 if year < 1 else 0
    date = datetime(year + cycle, month, 1, tzinfo=timezone.utc)
    date += timedelta(
        days=day - 1,
        hours=hour,
        minutes=minute - offset,
        seconds=second,
        microseconds=int(((parts["fraction"] or "") + "000000")[:6]),
    )
    seconds = int(date.replace(microsecond=0).timestamp())
    seconds -= 146097 * 86400 if cycle else 0
    if date.microsecond:
        # Symfony casts PHP's U.u text, so a negative whole second retains its
        # sign for the fraction too (23:59:59.5 before the epoch becomes -1.5).
        return float(f"{seconds}.{date.microsecond:06d}")
    return seconds


def _plain(value: str) -> object:
    lower = value.lower()
    if lower == "null" or value in ("", "~"):
        return None
    if lower in ("true", "false"):
        return lower == "true"
    if re.fullmatch(r"[+-]?0o[0-7_]+", value):
        digits = value.lstrip("+-")[2:].replace("_", "")
        return _bounded_integer(int(digits or "0", 8) * (-1 if value[0] == "-" else 1))
    if re.fullmatch(r"[+-]?[0-9][0-9_]*", value):
        value = value.replace("_", "")
    if re.fullmatch(r"-?[0-9]+", value):
        if len(value.lstrip("-")) > 19:
            return value
        integer = int(value)
        if str(integer) == value and _INT_MIN <= integer <= _INT_MAX:
            return integer
        return value
    if _NUMBER.fullmatch(value):
        return float(value)
    if re.fullmatch(r"0x[0-9a-f_]+", value, re.IGNORECASE):
        if not value.startswith("0x"):
            return 0.0
        return _bounded_integer(int(value[2:].replace("_", "") or "0", 16))
    if lower in (".inf", ".nan"):
        # Symfony's default evaluator returns positive infinity for .nan too.
        return math.inf
    if lower == "-.inf":
        return -math.inf
    if re.fullmatch(r"[+-]?[0-9][0-9_]*(?:\.[0-9_]+)?", value):
        return float(value.replace("_", ""))
    match = _TIMESTAMP.fullmatch(value)
    if match:
        return _timestamp(value, match)
    return value


def _scalar(node: ScalarNode, context: str = "root") -> object:
    value = node.value
    if node.style in ("|", ">") and node.explicit_tag is not None:
        if context == "mapping" and node.explicit_tag != "!":
            if node.tag != _TAG + "binary":
                tag = (
                    "!" + node.tag[len(_TAG):]
                    if node.tag.startswith(_TAG) else node.tag[1:]
                )
                return TaggedValue(tag, value)
        elif context == "sequence" and node.tag in (
            _TAG + "str", _TAG + "float", "!php/object", "!php/const", "!php/enum"
        ):
            header = re.search(r"[|>][0-9+-]*", node.header)
            value = header[0] + " " + " ".join(value.splitlines())
        else:
            raise _error(node, "Unsupported tagged block scalar in this context")
    if node.tag == _PLAIN:
        return _plain(value)
    if node.tag == _TAG + "str":
        if node.explicit_tag == _TAG + "str" and not value and node.style is None:
            raise _error(node, "Missing value for tag !!str")
        return value
    if node.tag in ("!php/object", "!php/const", "!php/enum"):
        return None
    if node.tag == _TAG + "float":
        if not value and node.style is None:
            raise _error(node, "Missing value for tag !!float")
        # PHP casts the raw scalar text, including any quote characters.
        match = _FLOAT_PREFIX.match(value) if node.style is None else None
        return float(match[1]) if match else 0.0
    if node.tag == _TAG + "binary":
        encoded = re.sub(r"\s", "", value)
        if len(encoded) % 4 or not re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", encoded):
            raise _error(node, "Invalid base64 binary scalar")
        binary = base64.b64decode(encoded, validate=True)
        try:
            return binary.decode("utf-8")
        except UnicodeDecodeError:
            return binary
    raise _error(node, f"Unsupported YAML tag {node.tag}")


def _key(node: Node, flow: bool) -> str | int:
    if not isinstance(node, ScalarNode):
        raise _error(node, "Non-scalar mapping keys are not supported")
    value = _scalar(node)
    if type(value) not in (str, int):
        raise _error(
            node, "Quote evaluable mapping keys that are not strings or integers"
        )
    if flow and node.tag == _PLAIN:
        value = node.value
    # PHP arrays also coerce quoted canonical decimal integer keys.
    if isinstance(value, str) and re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
        if len(value.lstrip("-")) > 19:
            return value
        integer = int(value)
        if str(integer) == value and _INT_MIN <= integer <= _INT_MAX:
            return integer
    return value


def _construct(node: Node, ancestors: set[int]) -> object:
    if id(node) in ancestors:
        raise _error(node, "Circular YAML reference")
    if isinstance(node, ScalarNode):
        # Aliases retain the value policy established at their definition,
        # including tagged block scalars moved between container contexts.
        return _scalar(node, node.definition_context)
    if node.explicit_tag not in (None, "!"):
        raise _error(node, f"Unsupported YAML collection tag {node.explicit_tag}")
    ancestors.add(id(node))
    try:
        if isinstance(node, SequenceNode):
            return [_construct(item, ancestors) for item in node.value]
        result = {}
        allow_overwrite = False
        for key_node, value_node in node.value:
            key = _key(key_node, node.flow_style)
            anchored_merge = (
                key == "<<" and value_node.anchor
                and key_node.start_mark.line == value_node.start_mark.line
            )
            if (
                anchored_merge and not node.flow_style
                and value_node.header.strip() != "&" + value_node.anchor
            ):
                result[key] = None
                continue
            value = _construct(value_node, ancestors)
            if key == "<<":
                if anchored_merge and node.flow_style:
                    raise _error(value_node, "Unsupported anchored flow merge")
                if not anchored_merge:
                    allow_overwrite = True
                mappings = value if isinstance(value, list) else [value]
                for mapping in mappings:
                    if not isinstance(mapping, dict):
                        raise _error(value_node, "YAML merge items must be mappings")
                    for merged_key, merged_value in mapping.items():
                        result.setdefault(merged_key, merged_value)
            elif not allow_overwrite and result.get(key) is not None:
                raise _error(key_node, f"Duplicate key {key!r}")
            else:
                result[key] = value
        return result
    finally:
        ancestors.remove(id(node))


def parse_yaml(text: str) -> object:
    """Parse one YAML document using Symfony's default scalar/tag policy."""
    if not isinstance(text, str):
        raise ValueError("YAML input must be text")
    loader = None
    try:
        loader = _Loader(text)
        node = loader.get_single_node()
        return _construct(node, set()) if node is not None else None
    except (YAMLError, binascii.Error, OverflowError, RecursionError) as error:
        raise ValueError(str(error)) from error
    finally:
        if loader is not None:
            loader.dispose()
