"""Intent: Check local links, code fences and narrow AiDoc meta/target pairing.

Usage:
    python3 scripts/check_doc DOC [DOC ...]

The package's public entry point is main(), which implements the documented CLI.
"""

from ._check import main

__all__ = ["main"]
