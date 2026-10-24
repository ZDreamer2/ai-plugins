"""Check downloaded Pi packages against raw source facts, without rebuilding."""

import json
import os
from pathlib import Path
import re
import stat
from typing import Any

from marketplace.source import SourcePlugin, discover_source, plugin_name


_VCS_DIRS = {
    '.svn', '_svn', 'CVS', '_darcs', '.arch-params', '.monotone', '.bzr',
    '.git', '.hg',
}
_FORBIDDEN_ROOT = (
    'package.json', '@common', 'pi-report.md', 'codex-report.md',
    '.claude-plugin', '.agents', '@setup',
    '.gitlab-ci.yml', '.gitlab', '.github', '.marketplace',
)


def _within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _directory(path: str | Path, label: str) -> Path:
    try:
        directory = Path(path).resolve(strict=True)
        if not directory.is_dir():
            raise ValueError(f"{label} '{directory}' must be a directory.")
        return directory
    except (OSError, RuntimeError) as error:
        raise ValueError(f"Could not inspect {label.lower()} '{path}': {error}") from error


def _children(directory: Path, label: str) -> list[Path]:
    try:
        return sorted(directory.iterdir())
    except OSError as error:
        raise ValueError(f"Could not enumerate {label} '{directory}': {error}") from error


def _assert_distribution_content(tree: Path) -> None:
    for name in _FORBIDDEN_ROOT:
        if (tree / name).exists():
            raise ValueError(
                f"Source/report/root activation content '{name}' must not be published."
            )

    def walk(directory: Path) -> None:
        for path in _children(directory, 'Pi artifact directory'):
            if path.is_dir() and path.name in _VCS_DIRS:
                continue
            relative = path.relative_to(tree).as_posix()
            if path.is_symlink():
                raise ValueError(f"Pi artifact must materialize symlink '{relative}'.")
            if path.name == 'ai-plugin.yml':
                raise ValueError(f"Source manifests must not be published: '{relative}'.")
            if path.is_dir():
                walk(path)

    walk(tree)


def _assert_package_inventory(tree: Path, expected: list[str]) -> None:
    actual: list[str] = []

    def walk(directory: Path) -> None:
        for path in _children(directory, 'Pi package inventory directory'):
            if path.name.startswith('.'):
                continue
            if path.is_dir():
                if path.name not in _VCS_DIRS:
                    walk(path)
            elif path.name == 'package.json':
                actual.append(path.parent.relative_to(tree).as_posix())

    walk(tree)
    if sorted(actual) != sorted(expected):
        raise ValueError(
            'Pi package roots do not match the source plugin inventory: '
            f'expected {sorted(expected)}, found {sorted(actual)}.'
        )


def _php_key(key: Any) -> Any:
    if isinstance(key, str) and re.fullmatch(r'-?(?:0|[1-9][0-9]*)', key):
        number = int(key)
        if str(number) == key and -(2 ** 63) <= number < 2 ** 63:
            return number
    return key


def _same(left: Any, right: Any) -> bool:
    """Match PHP strict comparison for the source/JSON values checked here.

    Associative JSON objects and YAML mappings are ordered PHP arrays. Lists
    are those same arrays with integer keys; even {} and [] compare identically.
    """
    if isinstance(left, (dict, list)) and isinstance(right, (dict, list)):
        def items(value: dict | list) -> list[tuple[Any, Any]]:
            return list(
                {_php_key(key): item for key, item in value.items()}.items()
                if isinstance(value, dict) else enumerate(value)
            )

        first, second = items(left), items(right)
        return len(first) == len(second) and all(
            _same(key, other_key) and _same(value, other_value)
            for (key, value), (other_key, other_value) in zip(first, second)
        )
    return type(left) is type(right) and left == right


def _json_integer(text: str) -> int | float:
    number = int(text)
    return number if -(2 ** 63) <= number < 2 ** 63 else float(text)


def _reject_constant(text: str) -> Any:
    raise ValueError(f"Nonstandard JSON constant '{text}'.")


def _assert_unicode(value: Any) -> None:
    if isinstance(value, str):
        value.encode('utf-8')
    elif isinstance(value, list):
        for item in value:
            _assert_unicode(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            _assert_unicode(key)
            _assert_unicode(item)


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    # Check every parsed pair before duplicate keys discard earlier values.
    for key, value in pairs:
        _assert_unicode(key)
        _assert_unicode(value)
    return dict(pairs)


def _read_metadata(path: Path) -> dict | list:
    try:
        data = json.loads(
            path.read_bytes().decode('utf-8'),
            parse_int=_json_integer, parse_constant=_reject_constant,
            object_pairs_hook=_json_object,
        )
        _assert_unicode(data)
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(f"Could not read Pi metadata '{path}': {error}") from error
    if not isinstance(data, (dict, list)):
        raise ValueError(f"Pi metadata must be an object: '{path}'.")
    return data


def _read_resource(path: Path, label: str) -> bytes:
    try:
        return path.read_bytes()
    except OSError as error:
        raise ValueError(f"Could not read {label} resource '{path}': {error}") from error


def _assert_resources(plugin: SourcePlugin, package: Path, output: Path,
                      source: Path) -> None:
    exclude_output = _within(output, source)

    def walk(directory: Path, ancestors: frozenset[Path]) -> None:
        try:
            origin = directory.resolve(strict=True)
        except (OSError, RuntimeError) as error:
            raise ValueError(
                f"Could not resolve source directory '{directory}': {error}"
            ) from error
        if origin in ancestors:
            raise ValueError(f"Source directory symlink cycle at '{directory}'.")
        ancestors = ancestors | {origin}
        for path in _children(directory, 'source resource directory'):
            try:
                # Finder's notName applies to files (including dangling file
                # links), while a directory with this name still has resources.
                if path.name == 'ai-plugin.yml' and not path.is_dir():
                    continue
                canonical = path.resolve()
                if exclude_output and _within(canonical, output):
                    continue
                mode = path.stat().st_mode
                if stat.S_ISDIR(mode):
                    if path.name not in _VCS_DIRS:
                        walk(path, ancestors)
                    continue
                if not stat.S_ISREG(mode):
                    raise ValueError(f"Source resource '{path}' must be a file.")
                destination = package / path.relative_to(plugin.directory)
                if not destination.is_file():
                    raise ValueError(f"Missing bundled Pi resource '{destination}'.")
                # Read both inputs, including Markdown, so unreadable source and
                # artifact resources cannot slip through the rendering exemption.
                source_bytes = _read_resource(path, 'source')
                artifact_bytes = _read_resource(destination, 'bundled Pi')
                if path.name == 'SKILL.md' and not artifact_bytes:
                    raise ValueError(f"Empty Pi skill '{destination}'.")
                if os.access(path, os.X_OK) and not os.access(destination, os.X_OK):
                    raise ValueError(f"Executable mode lost for '{destination}'.")
                if not path.name.endswith('.md') and source_bytes != artifact_bytes:
                    raise ValueError(f"Stale or corrupt Pi resource '{destination}'.")
            except (OSError, RuntimeError) as error:
                raise ValueError(
                    f"Could not inspect source resource '{path}': {error}"
                ) from error

    walk(plugin.directory, frozenset())


def _assert_plugin(plugin: SourcePlugin, tree: Path, output: Path,
                   source: Path) -> None:
    package = tree / plugin.root
    metadata = _read_metadata(package / 'package.json')
    name = plugin_name(plugin)
    # PHP concatenation preserves scalar names; arrays stringify as 'Array'.
    text_name = (
        ('1' if name else '') if type(name) is bool
        else format(name, '.14g') if type(name) is float
        else 'Array' if isinstance(name, (dict, list)) else str(name)
    )
    if type(name) is float:
        if 'e' in text_name:
            mantissa, exponent = text_name.split('e')
            mantissa += '.0' if '.' not in mantissa else ''
            text_name = mantissa + 'E' + f'{int(exponent):+d}'
        elif text_name in ('inf', '-inf', 'nan'):
            text_name = text_name.upper()
    if not isinstance(metadata, dict) or not _same(
        metadata.get('name'), '@zdreamer2/pi-plugin-' + text_name,
    ):
        raise ValueError(f"Incorrect Pi package identity at '{package}'.")
    version = metadata.get('version')
    if type(version) is not str or not version:
        raise ValueError(f"Missing Pi package version at '{package}'.")
    if not _same(metadata.get('description'), plugin.manifest.get('description')):
        raise ValueError(f"Incorrect Pi package description at '{package}'.")
    if not _same(_read_metadata(package / '.pi-plugin/plugin.json'), {
        'name': name, 'version': version,
    }):
        raise ValueError(f"Pi script identity differs from package metadata at '{package}'.")
    expected = {'skills': ['./' + path for path in plugin.skills]}
    if plugin.extensions:
        expected['extensions'] = ['./' + path for path in plugin.extensions]
    if not _same(metadata.get('pi'), expected):
        raise ValueError(f"Pi entry points differ from source at '{package}'.")
    _assert_resources(plugin, package, output, source)


def validate_pi_distribution(
    source_dir: str | Path, tree_dir: str | Path,
    output_dir: str | Path | None = None,
) -> int:
    """Validate independent packages, retaining the caller's exclusion context."""
    source = _directory(source_dir, 'Source marketplace')
    tree = _directory(tree_dir, 'Pi artifact tree')
    output = (Path(output_dir) if output_dir is not None else source / '@build').resolve()
    _assert_distribution_content(tree)
    inventory = discover_source(source, excluded_dirs=(output,))
    if any(plugin.root == '.' for plugin in inventory.plugins):
        raise ValueError('The marketplace root must not be a plugin.')
    if not inventory.plugins:
        raise ValueError('No source plugins found; refusing to publish an empty Pi distribution.')
    _assert_package_inventory(tree, [plugin.root for plugin in inventory.plugins])
    for plugin in inventory.plugins:
        _assert_plugin(plugin, tree, output, source)
    return len(inventory.plugins)
