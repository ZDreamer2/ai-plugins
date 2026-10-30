"""Adapt inventoried Pi skills and reject defects before output mutation."""

from copy import deepcopy
import re
from typing import Any, NoReturn

from marketplace import dump_yaml, parse_yaml
from marketplace.source import (
    MarketplaceIdentity, SourceInventory, SourcePlugin, pi_skill_name, source_skill_name,
)

from ._result import FileRendering

_PHP_TRIM = b" \t\n\r\0\v"
_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_SUPPORTED_KEYS = (
    "disable-model-invocation", "license", "compatibility", "metadata",
    "allowed-tools",
)


def pi_package_metadata(
    plugin: SourcePlugin, identity: MarketplaceIdentity = MarketplaceIdentity(),
) -> dict[str, Any]:
    """Render package metadata, rejecting complete npm names over 214 characters."""
    name = identity.pi_package_prefix + plugin.manifest["name"]
    if len(name) > 214:
        raise ValueError(
            f"Pi package name for '{plugin.root}' exceeds the 214-character limit."
        )
    pi = {"skills": ["./" + path for path in plugin.skills]}
    if plugin.extensions:
        pi["extensions"] = ["./" + path for path in plugin.extensions]
    return {
        "name": name,
        "version": deepcopy(plugin.manifest["version"]),
        "description": deepcopy(plugin.manifest["description"]),
        "keywords": ["pi-package"], "pi": pi,
    }


def pi_plugin_metadata(plugin: SourcePlugin) -> dict[str, Any]:
    return {key: deepcopy(plugin.manifest[key]) for key in ("name", "version")}


def _fail(path: str, reason: str) -> NoReturn:
    raise ValueError(f"Pi skill '{path}' {reason}.")


def _string_bytes(value: str | bytes) -> bytes:
    return (
        value if isinstance(value, bytes)
        else value.encode("utf-8", "surrogateescape")
    )


def _description_length(value: str | bytes) -> int:
    # mb_strlen's UTF-8 counting includes malformed byte strings accepted by
    # Symfony !!binary; this policy stays local to the strict Pi adapter.
    return len(_string_bytes(value).decode("utf-8", "replace"))


def render_pi_skill(
    content: str, path_in_plugin: str, plugin: SourcePlugin,
) -> FileRendering:
    path = plugin.root + "/" + path_in_plugin
    close = content.find("\n---\n", 3) if content.startswith("---\n") else -1
    if close < 0:
        _fail(path, "has no complete YAML frontmatter")
    frontmatter, body = content[4:close + 1], content[close + 5:]
    if not _string_bytes(body).strip(_PHP_TRIM):
        _fail(path, "has no instructions after its frontmatter")
    try:
        data = parse_yaml(frontmatter)
    except ValueError as error:
        _fail(path, "has malformed YAML frontmatter: " + str(error))
    if not isinstance(data, (dict, list)) or not data:
        _fail(path, "must have a non-empty frontmatter mapping")
    data = data if isinstance(data, dict) else {}
    expected = source_skill_name(plugin, path_in_plugin)
    name = data.get("name")
    if not isinstance(name, (str, bytes)) or not name:
        _fail(path, f"must define name '{expected}'")
    if _string_bytes(name) != _string_bytes(expected):
        authored = (
            name.decode("utf-8", "surrogateescape")
            if isinstance(name, bytes) else name
        )
        _fail(path, f"defines name '{authored}', but its inventoried directory "
              f"names it '{expected}'")
    description = data.get("description")
    if (
        not isinstance(description, (str, bytes))
        or not _string_bytes(description).strip(_PHP_TRIM)
    ):
        _fail(path, "must define a non-empty string description")
    rendered = {
        "name": pi_skill_name(plugin, path_in_plugin), "description": description,
    }
    if _description_length(description) > 1024:
        _fail(path, "has a description longer than 1024 characters")
    rendered.update((key, data[key]) for key in _SUPPORTED_KEYS if key in data)
    return FileRendering(
        "---\n" + dump_yaml(rendered, inline=4, indent=2) + "---\n" + body,
    )


def preflight_pi(inventory: SourceInventory) -> None:
    """Validate all names before reading and fully rendering skills in order."""
    seen: dict[str, str] = {}
    for plugin in inventory.plugins:
        for skill_dir in plugin.skills:
            relative = skill_dir + "/SKILL.md"
            path = plugin.root + "/" + relative
            name = pi_skill_name(plugin, relative)
            if len(_string_bytes(name)) > 64:
                _fail(path, f"renders to '{name}', which exceeds the "
                      "64-character name limit")
            if _NAME_PATTERN.search(name) is None:
                _fail(path, f"renders to invalid name '{name}': use lowercase "
                      "letters, numbers and single hyphens")
            if name in seen:
                raise ValueError(
                    f"Pi skills '{seen[name]}' and '{path}' render to the "
                    f"same name '{name}'."
                )
            seen[name] = path

    # A nested manifest may be the nearest owner during ordinary tree rendering.
    # Preflight must still validate each skill with its inventoried consuming
    # owner, including the owner's document-relative include boundary.
    from ._markdown import _render_owned_file_result

    for plugin in inventory.plugins:
        for skill_dir in plugin.skills:
            relative = skill_dir + "/SKILL.md"
            path = (
                relative if plugin.root == "." else plugin.root + "/" + relative
            )
            content = (plugin.directory / relative).read_bytes().decode(
                "utf-8", "surrogateescape",
            )
            _render_owned_file_result(content, path, "pi", inventory, plugin.root)
