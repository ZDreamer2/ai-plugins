#!/usr/bin/env python3
"""Run check_doc directly as a package directory or with python3 -m check_doc."""

import sys
from pathlib import Path

if __package__ in (None, ""):
	sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from check_doc import main  # noqa: E402


if __name__ == "__main__":
	sys.exit(main())
