"""Intent: Inspect source syntax and independent Pi artifacts without writes.

Usage:
    from marketplace.validation import check_syntax
    result = check_syntax({'root': '/checkout', 'changes': [
        {'repo': '.', 'path': 'script.py', 'kind': 'modified'},
    ]})
    from marketplace.validation import validate_pi_distribution
    count = validate_pi_distribution('/checkout', '/downloaded/pi',
                                     output_dir='/checkout/@build')

Syntax findings are returned; input and filesystem errors reach the caller.
Importing this unit needs neither YAML, source inventory nor Git.
"""

from pathlib import Path

from ._syntax import Change, CheckGroup, CheckResult, Finding, RanCheck, check_syntax


def validate_pi_distribution(
    source_dir: str | Path, tree_dir: str | Path,
    output_dir: str | Path | None = None,
) -> int:
    """Return the validated package count; input/artifact errors reach callers.

    The selected output defaults to source/@build and excludes generated source
    content. Explicit relative output paths resolve against the working directory.
    Neither Git history nor rendering or building is needed.
    """
    from ._pi_distribution import validate_pi_distribution as validate

    return validate(source_dir, tree_dir, output_dir)


__all__ = [
    'Change', 'CheckGroup', 'CheckResult', 'Finding', 'RanCheck', 'check_syntax',
    'validate_pi_distribution',
]
