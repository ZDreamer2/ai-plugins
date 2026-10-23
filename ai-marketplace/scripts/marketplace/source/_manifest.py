"""Read source data without resolving identity or filtering host metadata."""

from pathlib import Path
from typing import Any

from marketplace import parse_yaml


def read_manifest(path: str | Path) -> dict[str, Any]:
    """Read a YAML mapping, retaining its values and extra fields."""
    manifest_path = Path(path)
    try:
        data = parse_yaml(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(
            f"Could not read manifest '{manifest_path}': {error}"
        ) from error
    if not isinstance(data, dict):
        raise ValueError(
            f"Manifest '{manifest_path}' must contain a YAML mapping."
        )
    return data
