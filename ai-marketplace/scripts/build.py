#!/usr/bin/env python3
"""Build standalone Claude Code, Codex and Pi marketplace distributions."""

import argparse
import sys

sys.dont_write_bytecode = True

from marketplace.build import build


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True, help="Source marketplace directory")
    parser.add_argument("--output-dir", help="Output directory (default: <dir>/@build)")
    parser.add_argument("--dry-run", action="store_true", help="Render and check without writing output")
    args = parser.parse_args()
    try:
        result = build(args.dir, args.output_dir, args.dry_run)
    except (OSError, ValueError, TypeError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1
    label = "[dry-run] " if args.dry_run else ""
    if result.plugin_count:
        print(f"{label}Building {result.plugin_count} plugin(s)...")
    else:
        print(f"{label}No ai-plugin.yml files found.")
    for tree in result.trees:
        print(f"{label}{tree.host}: {tree.source_file_count} source file(s)")
        for path in tree.generated_files:
            print(f"{label}{tree.host}/{path}: policy.allow_implicit_invocation: false")
        for path, note in tree.metadata.items():
            print(f"{label}{tree.host}/{path}: {note}")
        for section, summary in tree.report_summaries.items():
            print(f"{label}{tree.host}/{section}: {summary}")
        if tree.report_total is not None:
            print(f"{label}{tree.host}-report.md: {tree.report_total}")
    for name, size in result.installers.items():
        print(f"{label}{result.output_dir / 'claude/@setup' / name}: {size} byte(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
