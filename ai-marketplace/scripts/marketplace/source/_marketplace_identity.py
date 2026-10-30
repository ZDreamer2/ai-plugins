"""Read optional marketplace branding shared by builders and validators."""

from dataclasses import dataclass
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class MarketplaceIdentity:
    """Marketplace branding; defaults preserve the standalone zd-plugins identity."""

    name: str = "zd-plugins"
    owner: str = "ZDreamer2"
    description: str = "AI documentation and marketplace authoring plugins"
    display_name: str = "ZDreamer2 plugins"
    pi_package_prefix: str = "@zdreamer2/pi-plugin-"


def read_marketplace_identity(source_dir: str | Path) -> MarketplaceIdentity:
    """Load .marketplace/identity.json, requiring all five fields when present.

    Reject unknown/duplicate keys, empty or padded strings, invalid catalog names
    and prefixes that cannot form lowercase npm package names. No files are written.
    """
    path = Path(source_dir) / ".marketplace/identity.json"
    if not path.exists() and not path.is_symlink():
        return MarketplaceIdentity()

    def object_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate field '{key}'")
            result[key] = value
        return result

    try:
        config = json.loads(path.read_text(encoding="utf-8"),
                            object_pairs_hook=object_pairs)
        fields = set(MarketplaceIdentity.__dataclass_fields__)
        if not isinstance(config, dict) or set(config) != fields:
            raise ValueError("expected exactly " + ", ".join(sorted(fields)))
        for key, value in config.items():
            if (not isinstance(value, str) or not value.strip()
                    or value != value.strip()
                    or any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value)):
                raise ValueError(
                    f"{key} must be a nonempty, unpadded string without controls"
                )
            value.encode("utf-8")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", config["name"]):
            raise ValueError(
                "name must use lowercase letters, digits and single hyphens"
            )
        if not re.fullmatch(r"(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*-",
                            config["pi_package_prefix"]):
            raise ValueError(
                "pi_package_prefix must be a lowercase npm prefix ending in '-'"
            )
        return MarketplaceIdentity(**config)
    except (OSError, UnicodeError, ValueError, TypeError) as error:
        raise ValueError(f"Invalid marketplace identity config '{path}': {error}") from error
