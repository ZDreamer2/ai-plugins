"""Compose source preflight, three host trees, metadata and installer bundles."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import json
import math
from pathlib import Path
import re
from typing import Any

from marketplace import TaggedValue
from marketplace.source import discover_source, resolve_identity

from ._installers import build_installers
from ._readme import distribution_readmes
from ._tree import render_tree, source_entries, write_bytes
from .rendering import (
    claude_marketplace_metadata, claude_plugin_metadata,
    codex_marketplace_metadata, codex_plugin_metadata,
    pi_package_metadata, pi_plugin_metadata, preflight_pi,
)


@dataclass(frozen=True)
class TreeResult:
    """Facts about one tree, identical for real builds and dry runs."""

    host: str
    source_file_count: int
    generated_files: tuple[str, ...]
    metadata: dict[str, str]
    report_text: str | None
    report_summaries: dict[str, str]
    report_total: str | None


@dataclass(frozen=True)
class BuildResult:
    """Completed output locations and narration facts, with no printed output."""

    source_dir: Path
    output_dir: Path
    plugin_count: int
    trees: tuple[TreeResult, ...]
    installers: dict[str, int]


def _json(value: Any, level: int = 0) -> str:
    """Encode retained YAML values with PHP array shapes and JSON formatting."""
    if isinstance(value, TaggedValue):
        # Symfony's tagged record has private properties, so JSON sees an object
        # with no public fields rather than the parser's Python record fields.
        return "{}"
    if isinstance(value, bytes):
        value = value.decode("utf-8")
    if isinstance(value, dict):
        normalized = {}
        for key, item in value.items():
            if isinstance(key, str) and re.fullmatch(r"-?(?:0|[1-9][0-9]*)", key):
                number = int(key)
                if str(number) == key and -(2 ** 63) <= number < 2 ** 63:
                    key = number
            normalized[key] = item
        if all(type(key) is int and key == index for index, key in enumerate(normalized)):
            value = list(normalized.values())
        else:
            value = normalized
    if isinstance(value, (dict, list)):
        if not value:
            return "[]"
        indent = "\t" * (level + 1)
        if isinstance(value, dict):
            entries = [
                _json(str(key)) + ": " + _json(item, level + 1)
                for key, item in value.items()
            ]
            opening, closing = "{", "}"
        else:
            entries = [_json(item, level + 1) for item in value]
            opening, closing = "[", "]"
        return (
            opening + "\n" + indent + (",\n" + indent).join(entries)
            + "\n" + "\t" * level + closing
        )
    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("Non-finite YAML value cannot be encoded as JSON.")
        if value == 0:
            return "-0" if math.copysign(1, value) < 0 else "0"
        text = repr(value)
        if 1e-4 <= abs(value) < 1e17:
            text = format(Decimal(text), "f")
            return text[:-2] if text.endswith(".0") else text
        mantissa, exponent = text.lower().split("e")
        if "." not in mantissa:
            mantissa += ".0"
        number = int(exponent)
        return mantissa + "e" + ("+" if number >= 0 else "-") + str(abs(number))
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False)
        .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    )


def build(
    source_dir: str | Path, output_dir: str | Path | None = None,
    dry_run: bool = False, *, now: datetime | None = None,
) -> BuildResult:
    source = Path(source_dir).resolve(strict=True)
    if not source.is_dir():
        raise ValueError(f"Source marketplace '{source}' must be a directory.")
    output = (
        Path(output_dir) if output_dir is not None else source / "@build"
    ).resolve()
    trees = tuple(output / host for host in ("claude", "codex", "pi"))
    if output == source or any(
        tree == source or tree in source.parents for tree in trees
    ):
        raise ValueError(f"Output '{output}' overlaps source input '{source}'.")
    inventory = resolve_identity(
        discover_source(source, excluded_dirs=(output,)), now=now,
    )
    # Description validation is inventory-wide and precedes Pi name/content preflight.
    codex_manifests = [
        codex_plugin_metadata(plugin) for plugin in inventory.plugins
    ]
    preflight_pi(inventory)
    readmes = distribution_readmes(source)
    results: list[TreeResult] = []
    entries, excluded_inputs = (
        source_entries(source, output) if inventory.plugins else ((), ())
    )
    # Read-only inputs excluded from copying still need protection from writes.
    inputs = [entry.path for entry in entries] + list(excluded_inputs)
    if readmes:
        inputs.append(source / ".marketplace/readme.json")
    for plugin in inventory.plugins:
        inputs.append(plugin.directory / "ai-plugin.yml")
        inputs.extend(
            plugin.directory / skill / "SKILL.md" for skill in plugin.skills
        )
    installer_source = source / "@common/@setup-sources"
    inputs.extend(installer_source / name for name in (
        "install.sh", "install.ps1", "setup.py", "status-line.py", "settings.json",
    ))
    written_files = {
        output / "claude/@setup/install.sh", output / "claude/@setup/install.ps1",
    }
    if inventory.plugins:
        written_files.update(
            output / f"{host}-report.md" for host in ("codex", "pi")
        )
    for path in inputs:
        origin = path.resolve()
        tree_overlap = inventory.plugins and any(
            not tree.is_symlink() and (origin == tree or tree in origin.parents)
            for tree in trees
        )
        if tree_overlap or origin in written_files:
            raise ValueError(f"Output '{output}' overlaps source input '{path}'.")
    if inventory.plugins:
        for host, tree in zip(("claude", "codex", "pi"), trees):
            count, generated, report = render_tree(
                inventory, entries, tree, host, dry_run, readmes.get(host),
            )
            metadata: dict[str, str] = {}

            def emit(relative: str, data: dict[str, Any], note: str) -> None:
                metadata[relative] = note
                if not dry_run:
                    content = _json(data) + "\n"
                    write_bytes(tree / relative, content.encode("utf-8"))

            for index, plugin in enumerate(inventory.plugins):
                prefix = "" if plugin.root == "." else plugin.root + "/"
                version = plugin.manifest["version"]
                if host == "claude":
                    emit(prefix + ".claude-plugin/plugin.json",
                         claude_plugin_metadata(plugin), version)
                elif host == "codex":
                    emit(prefix + ".codex-plugin/plugin.json",
                         codex_manifests[index], version)
                else:
                    emit(prefix + "package.json",
                         pi_package_metadata(plugin), version)
                    emit(prefix + ".pi-plugin/plugin.json",
                         pi_plugin_metadata(plugin), version)
            if host == "claude":
                emit(".claude-plugin/marketplace.json",
                     claude_marketplace_metadata(inventory),
                     f"{len(inventory.plugins)} plugin(s)")
            elif host == "codex":
                emit(".agents/plugins/marketplace.json",
                     codex_marketplace_metadata(inventory),
                     f"{len(inventory.plugins)} plugin(s)")
            report_text = report.render() if report is not None else None
            if report_text is not None and not dry_run:
                write_bytes(output / f"{host}-report.md",
                            report_text.encode("utf-8", "surrogateescape"))
            results.append(TreeResult(
                host, count, generated, metadata, report_text,
                report.summaries() if report is not None else {},
                report.total() if report is not None else None,
            ))
    installers = build_installers(
        source / "@common/@setup-sources", output / "claude/@setup", dry_run, now,
    )
    return BuildResult(source, output, len(inventory.plugins), tuple(results), installers)
