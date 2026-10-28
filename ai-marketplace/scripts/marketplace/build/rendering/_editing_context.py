"""Remove source-only editing references before Markdown composition."""

from marketplace import dump_yaml, parse_yaml


def strip_editing_context(content: str) -> str:
    """Keep runtime frontmatter properties, dropping an empty header entirely."""
    if not content.startswith("---\n"):
        return content
    close = content.find("\n---\n", 3)
    if close < 0:
        return content
    frontmatter = content[4:close + 1]
    if "edit-only-context" not in frontmatter:
        return content
    try:
        data = parse_yaml(frontmatter)
    except ValueError:
        return content
    if not isinstance(data, dict) or "edit-only-context" not in data:
        return content
    del data["edit-only-context"]
    body = content[close + 5:]
    return "---\n" + dump_yaml(data) + "---\n" + body if data else body
