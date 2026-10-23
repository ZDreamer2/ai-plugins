"""Intent: expose source facts and separate Git-derived publishing identity.

Usage:
    from marketplace.source import discover_source, resolve_identity

    source = discover_source("/path/to/marketplace", excluded_dirs=("@build",))
    raw_manifest = source.plugins[0].manifest
    publishing = resolve_identity(source)

Source roots and entry points use logical relative POSIX paths. Discovery
requires no Git history. Identity resolution returns copied manifests with
extra fields retained for host rendering. Python 3.10+ uses the library's
bundled YAML parser; neither pip nor the shared Bico SDK is required.
Default identity formatting uses Europe/Moscow from the system timezone
database; callers may supply an explicit tzinfo. Discovery needs no timezone
database.
"""

from ._identity import resolve_identity
from ._inventory import (
    SourceInventory,
    SourcePlugin,
    codex_skill_names,
    discover_source,
    pi_skill_for_invocation,
    pi_skill_name,
    pi_source_skill_names,
    plugin_name,
    plugin_root_of,
    source_skill_name,
)
from ._manifest import read_manifest

__all__ = [
    "SourceInventory", "SourcePlugin", "read_manifest", "discover_source",
    "plugin_name", "plugin_root_of", "source_skill_name", "pi_skill_name",
    "pi_skill_for_invocation", "codex_skill_names", "pi_source_skill_names",
    "resolve_identity",
]
