"""Separate build-only configuration from published Markdown frontmatter."""

import re

from marketplace import dump_yaml, parse_yaml


def source_frontmatter(content: str, path: str) -> tuple[str, str, bool]:
    """Return runtime header, body, and whether Jinja is enabled."""
    if not content.startswith('---\n'):
        return '', content, True
    close = content.find('\n---\n', 3)
    if close < 0:
        return '', content, True
    raw = content[4:close + 1]
    header, body = content[:close + 5], content[close + 5:]
    build_keys = {'edit-only-context', 'build-template'}
    if not any(key in raw for key in build_keys):
        return header, body, True
    try:
        data = parse_yaml(raw)
    except ValueError:
        if 'build-template' in raw:
            raise ValueError(f'{path}: malformed template frontmatter') from None
        return header, body, True
    if not isinstance(data, dict) or not build_keys.intersection(data):
        return header, body, True
    enabled = 'build-template' not in data
    if not enabled and data.pop('build-template') is not False:
        raise ValueError(f'{path}: build-template must be false to disable Jinja')
    editing = 'edit-only-context' in data
    data.pop('edit-only-context', None)
    if not data:
        return '', body, enabled
    if not enabled and not editing:
        # Keep the spelling of static host metadata when only removing the opt-out.
        kept, count = re.subn(r'^build-template:[ \t]+false[ \t]*\n', '', raw, flags=re.M)
        if count == 1 and parse_yaml(kept) == data:
            return '---\n' + kept + '---\n', body, enabled
    return '---\n' + dump_yaml(data) + '---\n', body, enabled
