"""Adapt Codex skills and metadata from explicit source facts, without writes."""

from copy import deepcopy
import re
from typing import Any

from marketplace import dump_yaml, parse_yaml
from marketplace.source import MarketplaceIdentity, SourceInventory, SourcePlugin

from ._constructs import CodexConstruct, CodexConstructFinding
from ._result import FileRendering

_PHP_TRIM = " \t\n\r\0\v"


def codex_plugin_metadata(plugin: SourcePlugin) -> dict[str, Any]:
    description = plugin.manifest.get("description")
    if not isinstance(description, str) or description == "":
        raise ValueError(
            f"Plugin '{plugin.root}' must define a description in "
            "ai-plugin.yml: Codex requires it."
        )
    result = {
        key: deepcopy(plugin.manifest[key])
        for key in ("name", "version", "description")
    }
    if plugin.manifest.get("author") is not None:
        result["author"] = deepcopy(plugin.manifest["author"])
    if (plugin.directory / "skills").is_dir():
        result["skills"] = "./skills/"
    return result


def codex_marketplace_metadata(
    inventory: SourceInventory, identity: MarketplaceIdentity = MarketplaceIdentity(),
) -> dict[str, Any]:
    return {
        "name": identity.name,
        "interface": {"displayName": identity.display_name},
        "plugins": [
            {
                "name": deepcopy(plugin.manifest["name"]),
                "source": {
                    "source": "local",
                    "path": "./" if plugin.root == "." else "./" + plugin.root,
                },
                "policy": {
                    "installation": "AVAILABLE", "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
            for plugin in inventory.plugins
        ],
    }


def _finding(line: int, text: str) -> CodexConstructFinding:
    return CodexConstructFinding(CodexConstruct.SKILL_FRONTMATTER, line, text)


def _report_only(content: str, reason: str) -> FileRendering:
    return FileRendering(content, findings=[_finding(1, reason)])


def _key_source(lines: list[str], key: str) -> tuple[int, str]:
    pattern = re.compile(r"^" + re.escape(key) + r"\s*:", re.ASCII)
    for index, line in enumerate(lines):
        if pattern.search(line):
            return index + 2, line.strip(_PHP_TRIM)
    return 1, key


def render_codex_skill(
    content: str, path_in_plugin: str, namespace: str,
) -> FileRendering:
    if not content.startswith("---\n"):
        return _report_only(content, "no frontmatter: Codex will not load this skill")
    close = content.find("\n---\n", 3)
    if close < 0:
        return _report_only(content, "no frontmatter: Codex will not load this skill")
    frontmatter, body = content[4:close + 1], content[close + 5:]
    try:
        parsed = parse_yaml(frontmatter)
    except ValueError:
        return _report_only(
            content, "frontmatter is not valid YAML: Codex will not load this skill",
        )
    data = parsed if isinstance(parsed, dict) else {}
    description = data.get("description")
    if not isinstance(description, str) or description == "":
        return _report_only(
            content, "no description: Codex has nothing to route this skill on",
        )

    lines = frontmatter.split("\n")
    kept = {}
    if data.get("name") is not None:
        kept["name"] = data["name"]
    hint = data.get("argument-hint")
    if hint is not None:
        if not isinstance(hint, str) or hint == "":
            hint = _key_source(lines, "argument-hint")[1][
                len("argument-hint") + 1:
            ].strip(_PHP_TRIM)
        if hint != "":
            if not re.search(r"[.!?]$", description):
                description += "."
            skill = path_in_plugin.split("/")[1]
            description += f" Usage: ${namespace}:{skill} {hint}."
    kept["description"] = description

    result = FileRendering("")
    for key, value in data.items():
        if key in ("name", "description", "argument-hint"):
            continue
        # PHP's defaults compare strictly; bools must not equal Python integers.
        if key == "disable-model-invocation" and value is False:
            continue
        if key == "user-invocable" and value is True:
            continue
        if value is None and key not in (
            "disable-model-invocation", "user-invocable",
        ):
            continue
        if key == "disable-model-invocation":
            result.extra_files["agents/openai.yaml"] = (
                "policy:\n  allow_implicit_invocation: false\n"
            )
        else:
            line, text = _key_source(lines, str(key))
            result.findings.append(_finding(line, text))
    result.content = "---\n" + dump_yaml(kept) + "---\n" + body
    return result
