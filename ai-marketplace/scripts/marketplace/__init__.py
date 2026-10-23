"""Intent: Provide standalone marketplace source and validation capabilities.

Usage:
    from marketplace import dump_yaml, parse_yaml
    manifest = parse_yaml("name: example")
    text = dump_yaml(manifest, inline=2, indent=4)

Requires Python 3.10+. The YAML dependency is bundled; no installed packages
are required. Source and validation APIs live in their respective subpackages.
Parsing returns ordinary containers and Symfony-compatible scalar values.
Binary tags return text when their bytes are UTF-8, otherwise bytes. Invalid or
unsupported YAML raises ValueError. Importing this package does not load YAML.
Tagged mapping block scalars retain their tag and text in a TaggedValue record.
Emission follows Symfony's default formatting for these scalar/container values,
including ordered PHP-array keys and empty containers emitted as ``{  }``.
Inline depth selects flow collections; indent sets nested block spacing. Strings
containing line breaks use quoted escapes. Emission accepts no general YAML flags;
unsupported objects or circular containers raise ValueError.
"""

from dataclasses import dataclass

__all__ = ["TaggedValue", "dump_yaml", "parse_yaml"]


@dataclass(frozen=True)
class TaggedValue:
    """An inert tagged block scalar accepted by Symfony's default parser."""

    tag: str
    value: str


def parse_yaml(text: str) -> object:
    """Parse YAML using the marketplace's bundled compatibility parser."""
    from ._yaml import parse_yaml as parse

    return parse(text)


def dump_yaml(value: object, inline: int = 2, indent: int = 4) -> str:
    """Emit retained YAML values using bounded Symfony default formatting."""
    from ._yaml_dump import dump_yaml as dump

    return dump(value, inline=inline, indent=indent)
