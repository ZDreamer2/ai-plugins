"""Materialize logical source copies and replace one host's output tree."""

from dataclasses import dataclass
import os
from pathlib import Path
import shutil

from marketplace.source import SourceInventory, plugin_root_of

from ._reports import CodexConstructReport, PiConstructReport
from .rendering import render_file_result


_VCS_DIRS = {
    ".svn", "_svn", "CVS", "_darcs", ".arch-params", ".monotone", ".bzr",
    ".git", ".hg",
}


@dataclass(frozen=True)
class SourceEntry:
    path: Path
    relative: str
    directory: bool


def source_entries(
    source: Path, output: Path,
) -> tuple[tuple[SourceEntry, ...], tuple[Path, ...]]:
    """Return origin-sorted logical copies and excluded input file aliases."""
    entries: list[SourceEntry] = []
    excluded_inputs: list[Path] = []
    exclude_output = output.is_relative_to(source)

    def walk(folder: Path, ancestors: frozenset[Path]) -> None:
        origin = folder.resolve(strict=True)
        if origin in ancestors:
            raise ValueError(f"Directory symlink cycle at '{folder}'.")
        ancestors = ancestors | {origin}
        for path in folder.iterdir():
            relative = path.relative_to(source).as_posix()
            resolved = path.resolve()
            if relative in {
                "@common", ".gitlab-ci.yml", ".gitlab", ".github", ".marketplace",
            }:
                # Shared roots, CI and build configuration are source-only.
                continue
            if exclude_output and (resolved == output or output in resolved.parents):
                # A file alias outside the logical output still exposes a source
                # input even though its canonical origin is excluded from copying.
                if (
                    path.is_symlink() and not path.is_dir()
                    and not path.is_relative_to(output)
                ):
                    excluded_inputs.append(path)
                continue
            directory = path.is_dir()
            if directory and path.name in _VCS_DIRS:
                continue
            if path.name != "ai-plugin.yml":
                entries.append(SourceEntry(path, relative, directory))
            if directory:
                walk(path, ancestors)

    walk(source, frozenset())

    def order(entry: SourceEntry) -> tuple[bytes, bytes]:
        try:
            origin = entry.path.resolve(strict=True)
        except FileNotFoundError:
            origin = entry.path
        return os.fsencode(origin), os.fsencode(entry.relative)

    return tuple(sorted(entries, key=order)), tuple(excluded_inputs)


def make_directory(path: Path) -> None:
    """Create normalized directories without following destination symlinks."""
    if path.is_symlink():
        raise ValueError(f"Output directory '{path}' is a symlink.")
    if path.is_dir():
        return
    if not path.parent.is_dir() or path.parent.is_symlink():
        make_directory(path.parent)
    path.mkdir(mode=0o755)
    path.chmod(0o755)


def write_bytes(path: Path, content: bytes, mode: int = 0o644) -> None:
    make_directory(path.parent)
    if path.is_symlink():
        path.unlink()
    if path.write_bytes(content) != len(content):
        raise OSError(f"Incomplete output write: '{path}'.")
    path.chmod(mode)


def replace_tree(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)
    make_directory(path)


def render_tree(
    inventory: SourceInventory, entries: tuple[SourceEntry, ...],
    tree: Path, host: str, dry_run: bool, readme: str | None = None,
) -> tuple[int, tuple[str, ...], CodexConstructReport | PiConstructReport | None]:
    report = (
        CodexConstructReport() if host == "codex"
        else PiConstructReport() if host == "pi" else None
    )
    if not dry_run:
        replace_tree(tree)
    count = 0
    generated: list[str] = []
    for entry in entries:
        if readme is not None and entry.relative == "README.md":
            continue
        destination = tree / entry.relative
        if entry.directory:
            if not dry_run:
                make_directory(destination)
            continue
        count += 1
        if entry.relative.endswith(".md"):
            text = entry.path.read_bytes().decode("utf-8", "surrogateescape")
            result = render_file_result(text, entry.relative, host, inventory)
            owner = plugin_root_of(inventory, str(Path(entry.relative).parent))
            if report is not None:
                report.add(entry.relative, owner, result.findings)
            for relative, content in result.extra_files.items():
                companion = Path(entry.relative).parent / relative
                if (entry.path.parent / relative).is_file():
                    raise ValueError(
                        f"The Codex render generates '{companion.as_posix()}' "
                        f"from '{entry.relative}', but the source ships that file."
                    )
                generated.append(companion.as_posix())
                if not dry_run:
                    write_bytes(tree / companion, content.encode("utf-8", "surrogateescape"))
            if not dry_run:
                mode = 0o755 if os.access(entry.path, os.X_OK) else 0o644
                write_bytes(destination, result.content.encode("utf-8", "surrogateescape"), mode)
        elif not dry_run:
            make_directory(destination.parent)
            shutil.copyfile(entry.path, destination)
            destination.chmod(0o755 if os.access(entry.path, os.X_OK) else 0o644)
    if readme is not None:
        generated.append("README.md")
        if not dry_run:
            write_bytes(tree / "README.md", readme.encode("utf-8"))
    return count, tuple(generated), report
