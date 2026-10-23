#!/usr/bin/env python3
"""Inspect a Pi distribution against its standalone source marketplace."""

import argparse
import sys

sys.dont_write_bytecode = True

from marketplace.validation import validate_pi_distribution


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True, help="Source marketplace directory")
    parser.add_argument("--tree", required=True, help="Pi distribution directory")
    parser.add_argument("--output-dir", help="Excluded build output (default: <dir>/@build)")
    args = parser.parse_args()
    try:
        count = validate_pi_distribution(args.dir, args.tree, args.output_dir)
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        print(f"Pi publication preflight failed: {error}", file=sys.stderr)
        return 1
    print(f"Validated {count} independent Pi packages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
