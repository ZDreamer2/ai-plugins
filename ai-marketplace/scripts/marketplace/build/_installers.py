"""Bundle the Claude installers without decoding their source payloads."""

import base64
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


_SOURCE_NAMES = (
    "install.sh", "install.ps1", "setup.py", "status-line.py", "settings.json",
)
_BOM = b"\xef\xbb\xbf"
_PY_TAG = b"__BUNDLED_PY_END__"
_VERSION = b"__INSTALLER_VERSION__"
_BLOCK = re.compile(
    rb"\# === BUNDLE_REPLACE_BEGIN ===.*?\# === BUNDLE_REPLACE_END ===",
    re.DOTALL,
)


def build_installers(
    source_dir: Path,
    output_dir: Path,
    dry_run: bool,
    now: datetime | None = None,
) -> dict[str, int]:
    """Read and bundle five sources; return byte sizes, with optional writes."""
    if not source_dir.exists():
        return {}
    sources = {}
    for name in _SOURCE_NAMES:
        path = source_dir / name
        if not path.is_file():
            raise ValueError(f"Installer source not found: {path}")
        sources[name] = path.read_bytes()
    built = _bundle(sources, now)
    if not dry_run:
        _write_installers(output_dir, built)
    return {name: len(content) for name, content in built.items()}


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"Nonstandard JSON constant: {value}")


def _validate_json_strings(value: object) -> None:
    """Reject unpaired escaped surrogates, including nested object keys."""
    if isinstance(value, str):
        value.encode("utf-8")
    elif isinstance(value, list):
        for item in value:
            _validate_json_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            _validate_json_strings(key)
            _validate_json_strings(item)


def _validated_json_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    # Validate before collapsing duplicate keys, which can hide invalid values.
    for key, value in pairs:
        _validate_json_strings(key)
        _validate_json_strings(value)
    return dict(pairs)


def _bundle(sources: dict[str, bytes], now: datetime | None) -> dict[str, bytes]:
    # Decode explicitly: json.loads(bytes) would also accept UTF-16 and UTF-32.
    try:
        settings = json.loads(
            sources["settings.json"].decode("utf-8"),
            parse_constant=_reject_json_constant,
            object_pairs_hook=_validated_json_object,
        )
        _validate_json_strings(settings)
    except (UnicodeError, ValueError) as exc:
        raise ValueError(f"settings.json: invalid UTF-8 JSON: {exc}") from exc

    python = sources["setup.py"]
    for variable, placeholder, source_name in (
        (b"STATUS_LINE_B64", b"__STATUS_LINE_PLACEHOLDER__", "status-line.py"),
        (b"SETTINGS_B64", b"__SETTINGS_PLACEHOLDER__", "settings.json"),
    ):
        needle = variable + b' = "' + placeholder + b'"'
        if python.count(needle) != 1:
            raise ValueError(
                f"setup.py: expected exactly one assignment {needle.decode('ascii')}"
            )
        python = python.replace(
            needle, variable + b' = "' + base64.b64encode(sources[source_name]) + b'"',
        )
    if _PY_TAG in python:
        raise ValueError("setup.py contains reserved heredoc marker __BUNDLED_PY_END__")
    if re.search(rb"^'@", python, re.MULTILINE):
        raise ValueError("setup.py contains a line starting with '@")

    moscow = ZoneInfo("Europe/Moscow")
    clock = now if now is not None else datetime.now(moscow)
    if clock.tzinfo is None:
        clock = clock.replace(tzinfo=moscow)
    version = clock.astimezone(moscow).strftime("%y.%m.%d%H%M").encode("ascii")
    built = {}
    for name, replacement in (
        ("install.sh", _sh_replacement(python)),
        ("install.ps1", _ps1_replacement(python)),
    ):
        content, count = _BLOCK.subn(lambda match: replacement, sources[name], count=1)
        if count != 1:
            raise ValueError(f"BUNDLE_REPLACE_BEGIN/END markers not found in {name}")
        if _VERSION not in content:
            raise ValueError(f"__INSTALLER_VERSION__ placeholder not found in {name}")
        content = content.replace(_VERSION, version)
        if name == "install.ps1" and not content.startswith(_BOM):
            content = _BOM + content
        built[name] = content
    return built


def _sh_replacement(python: bytes) -> bytes:
    return b"\n".join((
        b"_py_tmpfile=$(mktemp /tmp/bc_setup_XXXXXX.py)",
        b'cat > "$_py_tmpfile" << \'__BUNDLED_PY_END__\'',
        python,
        _PY_TAG,
        b"PY_ARGS=()",
        b'[ "$AUTO_YES" = "true" ] && PY_ARGS+=("-y")',
        b'python3 "$_py_tmpfile" "${PY_ARGS[@]}"',
        b'rm -f "$_py_tmpfile"',
    ))


def _ps1_replacement(python: bytes) -> bytes:
    return b"\n".join((
        b"$pyCode = @'",
        python,
        b"'@",
        b"",
        b"$tempFile = New-TemporaryFile",
        b"$pyCode | Set-Content -Path $tempFile -Encoding utf8",
        b"",
        b"try {",
        b"\t$pyArgs = @()",
        b'\tif ($Yes) { $pyArgs += "-y" }',
        b"\t& $python $tempFile @pyArgs",
        b"} finally {",
        b"\tRemove-Item $tempFile -ErrorAction SilentlyContinue",
        b"}",
    ))


def _write_installers(output_dir: Path, built: dict[str, bytes]) -> None:
    for directory in (output_dir, *output_dir.parents):
        if directory.is_symlink():
            raise ValueError(f"Installer output directory is a symlink: {directory}")
    for name in built:
        path = output_dir / name
        if path.is_symlink():
            raise ValueError(f"Installer output file is a symlink: {path}")
    missing = []
    current = output_dir
    while not current.exists():
        missing.append(current)
        current = current.parent
    for directory in reversed(missing):
        directory.mkdir(mode=0o755)
        directory.chmod(0o755)
    for name, content in built.items():
        path = output_dir / name
        with path.open("wb") as stream:
            if stream.write(content) != len(content):
                raise OSError(f"Incomplete installer write: {path}")
        path.chmod(0o755 if name == "install.sh" else 0o644)
