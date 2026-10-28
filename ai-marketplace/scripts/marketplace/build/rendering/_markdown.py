"""Compose read-only includes before a single shared value pass."""

from marketplace.source import SourceInventory, plugin_root_of

from ._codex import render_codex_skill
from ._constructs import scan_codex, scan_pi
from ._editing_context import strip_editing_context
from ._includes import splice
from ._placeholders import substitute
from ._pi import render_pi_skill
from ._result import FileRendering


def render_file(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
) -> str:
    """Return content from the complete file pipeline, discarding companions."""
    return render_file_result(content, logical_path, host, inventory).content


def render_file_result(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
) -> FileRendering:
    """Render a file with unwritten companions and report-only findings."""
    if not logical_path.endswith(".md"):
        return FileRendering(content)
    return _render_owned_file_result(
        content, logical_path, host, inventory,
        plugin_root_of(inventory, logical_path),
    )


def _render_owned_file_result(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
    root: str | None,
) -> FileRendering:
    """Retain explicit consuming ownership through the complete pipeline."""
    shared = _render_markdown(content, logical_path, host, inventory, root)
    result = FileRendering(shared)
    if host == "codex":
        relative = (
            logical_path if root == "." else logical_path[len(root) + 1:]
        ) if root is not None else None
        parts = relative.split("/") if relative is not None else []
        if len(parts) == 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
            namespace = (inventory.directory / root).name
            result = render_codex_skill(shared, relative, namespace)
        result.findings.extend(scan_codex(result.content, inventory))
    elif host == "pi":
        plugin = next((p for p in inventory.plugins if p.root == root), None)
        if plugin is not None:
            relative = logical_path if root == "." else logical_path[len(root) + 1:]
            parent, _, basename = relative.rpartition("/")
            if basename == "SKILL.md" and parent in plugin.skills:
                result = render_pi_skill(shared, relative, plugin)
        result.findings.extend(scan_pi(result.content, inventory))
    return result


def render_markdown(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
) -> str:
    return _render_markdown(
        content, logical_path, host, inventory,
        plugin_root_of(inventory, logical_path),
    )


def _render_markdown(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
    root: str | None,
) -> str:
    if host not in ("claude", "codex", "pi"):
        raise ValueError(f"Unknown agent tree '{host}'.")
    content = strip_editing_context(content)
    return substitute(
        splice(content, logical_path, host, inventory, root),
        logical_path, host, inventory,
    )
