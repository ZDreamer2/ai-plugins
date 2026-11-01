#!/usr/bin/env python3
"""Prints ai-doc plugin file by short reference name, or help.md if unknown."""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", ".."))

REFS = {
	"stress-test": "workflows/build/workflows/on-build-done.md",
	"StartSimple": "Theory/StartSimple.md",
	"HumanDoc": "Formats/HumanDoc/HumanDoc.format.md",
	"AiDocBaseFormat": "Theory/AiDocBaseFormat.md",
}

arg = sys.argv[1].strip() if len(sys.argv) > 1 else ""
path = REFS.get(arg)

if path:
	target = os.path.join(PLUGIN_ROOT, path)
else:
	target = os.path.join(SCRIPT_DIR, "..", "help.md")

with open(target, "r") as f:
	print(f.read())
