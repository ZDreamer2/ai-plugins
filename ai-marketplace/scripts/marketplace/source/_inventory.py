"""Discover logical source facts without resolving Git identity."""

from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import posixpath
from typing import Any, Iterable

from ._manifest import read_manifest


@dataclass(frozen=True)
class SourcePlugin:
    """A logical plugin root and its original source data and entry points."""

    root: str
    directory: Path
    manifest: dict[str, Any]
    skills: tuple[str, ...]
    extensions: tuple[str, ...]


@dataclass(frozen=True)
class SourceInventory:
    """Canonical marketplace location with plugins in manifest-path order."""

    directory: Path
    plugins: tuple[SourcePlugin, ...]


_VCS_DIRS = {
    ".svn", "_svn", "CVS", "_darcs", ".arch-params", ".monotone", ".bzr",
    ".git", ".hg",
}


def discover_source(
    source_dir: str | Path, excluded_dirs: Iterable[str | Path] = (),
) -> SourceInventory:
    """Discover manifests with exclusions resolved relative to source_dir.

    Callers choose output exclusions. Hidden/VCS directories and directory
    symlinks are skipped, but a source-root manifest is permitted.
    Exclusions also omit skill and extension entry points under those paths.
    """
    directory = Path(source_dir).resolve(strict=True)
    if not directory.is_dir():
        raise ValueError(
            f"Source marketplace '{directory}' must be a directory."
        )
    exclusions = {
        (path if path.is_absolute() else directory / path).resolve()
        for path in map(Path, excluded_dirs)
    }
    entry_exclusions = {
        path for path in exclusions if path not in directory.parents
    }

    manifest_exclusions = {
        path for path in exclusions if path == directory or directory in path.parents
    }

    def excluded_entry(path: Path, targets: set[Path] = entry_exclusions) -> bool:
        origin = path.resolve()
        return any(origin == excluded or excluded in origin.parents
                   for excluded in targets)

    manifests: list[Path] = []

    def walk_error(error: OSError) -> None:
        raise error

    for current, dirs, files in os.walk(
        directory, followlinks=False, onerror=walk_error,
    ):
        current_path = Path(current)
        if current_path in exclusions:
            dirs[:] = []
            continue
        dirs[:] = [
            name for name in dirs
            if not name.startswith(".") and name not in _VCS_DIRS
            and not (current_path / name).is_symlink()
            and (current_path / name) not in exclusions
        ]
        manifest = current_path / "ai-plugin.yml"
        if ("ai-plugin.yml" in files and manifest.is_file()
                and not excluded_entry(manifest, manifest_exclusions)):
            manifests.append(manifest)

    plugins = []
    for manifest in sorted(manifests):
        plugin_dir = manifest.parent
        skills = tuple(sorted(
            path.parent.relative_to(plugin_dir).as_posix()
            for path in plugin_dir.glob("skills/*/SKILL.md")
            if not path.parent.name.startswith(".") and path.is_file()
            and not excluded_entry(path)
        ))
        extensions = tuple(sorted(
            path.relative_to(plugin_dir).as_posix()
            for suffix in ("js", "mjs", "ts")
            for path in plugin_dir.glob(f"extensions/*/index.{suffix}")
            if not path.parent.name.startswith(".") and path.is_file()
            and not excluded_entry(path)
        ))
        plugins.append(SourcePlugin(
            root=plugin_dir.relative_to(directory).as_posix(),
            directory=plugin_dir,
            manifest=read_manifest(manifest),
            skills=skills,
            extensions=extensions,
        ))
    return SourceInventory(directory, tuple(plugins))


def plugin_name(plugin: SourcePlugin) -> Any:
    """Manifest identity with the missing/null directory fallback applied."""
    name = plugin.manifest.get("name")
    return plugin.directory.name if name is None else name


def plugin_root_of(
    inventory: SourceInventory, logical_path: str,
) -> str | None:
    """Find the nearest manifest ancestor using the consuming logical path.

    A plugin's materialized @common belongs to that plugin, even when its
    source points to marketplace-root shared content. Do not resolve symlinks.
    """
    path = posixpath.normpath(logical_path)
    if path.startswith("/") or path == ".." or path.startswith("../"):
        return None
    parent = PurePosixPath(path)
    while True:
        root = parent.as_posix()
        if (inventory.directory / root / "ai-plugin.yml").is_file():
            return root
        if parent == parent.parent:
            return None
        parent = parent.parent


def source_skill_name(plugin: SourcePlugin, path_in_plugin: str) -> str:
    path = PurePosixPath(path_in_plugin)
    if path.name != "SKILL.md" or path.parent.as_posix() not in plugin.skills:
        raise ValueError(
            f"'{path_in_plugin}' is not an inventoried skill "
            f"of '{plugin.root}'."
        )
    return path.parent.name


def pi_skill_name(plugin: SourcePlugin, path_in_plugin: str) -> str:
    name = plugin_name(plugin)
    skill = source_skill_name(plugin, path_in_plugin)
    return name if name == skill else f"{name}-{skill}"


def pi_skill_for_invocation(
    inventory: SourceInventory, invocation: str,
) -> str | None:
    plugin_identity, skill = (
        invocation.split(":", 1) if ":" in invocation
        else (invocation, invocation)
    )
    for plugin in inventory.plugins:
        if (
            plugin_name(plugin) == plugin_identity
            and f"skills/{skill}" in plugin.skills
        ):
            return pi_skill_name(plugin, f"skills/{skill}/SKILL.md")
    return None


def _scanner_skill_names(
    inventory: SourceInventory, resolved: bool,
) -> tuple[str, ...]:
    names: dict[str, None] = {}
    for plugin in inventory.plugins:
        namespace = plugin_name(plugin) if resolved else plugin.directory.name
        for skill_dir in plugin.skills:
            skill = PurePosixPath(skill_dir).name
            names[skill] = None
            names[f"{namespace}:{skill}"] = None
    return tuple(names)


def codex_skill_names(inventory: SourceInventory) -> tuple[str, ...]:
    return _scanner_skill_names(inventory, resolved=False)


def pi_source_skill_names(inventory: SourceInventory) -> tuple[str, ...]:
    return tuple(dict.fromkeys(
        _scanner_skill_names(inventory, resolved=False)
        + _scanner_skill_names(inventory, resolved=True)
    ))
