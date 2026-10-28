"""Intent: render host content and metadata without writing files.

Usage:
    from marketplace.build.rendering import (
        codex_marketplace_metadata, codex_plugin_metadata, render_file_result,
    )

    text = source_bytes.decode("utf-8", "surrogateescape")
    result = render_file_result(text, "plugin/skills/run/SKILL.md", "codex", source)
    output_bytes = result.content.encode("utf-8", "surrogateescape")
    manifest = codex_plugin_metadata(resolved.plugins[0])
    catalog = codex_marketplace_metadata(resolved)

Paths are logical, marketplace-relative POSIX paths, including consuming
plugin @common paths. Included Markdown links/images and reference definitions
are rebased from the included document's consuming logical directory to the
including file's directory; standalone content and literal code stay unchanged.
File rendering selects case-sensitive .md paths;
render_file_result strips edit-only-context frontmatter, then runs includes,
placeholders, host adaptation and scanning,
returning content, extra_files (relative to the document folder) and findings.
The tree owner writes companions and aggregates findings. render_file returns
only the complete pipeline's content. render_markdown intentionally exposes
only reusable editing-context stripping and shared includes/placeholders,
without selection or adaptation. Included documents lose editing context before
validation and composition too.
Callers preserve source bytes with UTF-8 surrogateescape; include reads use
the same representation and retain line endings. Metadata consumes identity
already resolved by the caller and returns independent mutable mappings.
Codex reduces skill frontmatter and reports unsupported constructs. Pi strictly
validates and reduces inventoried skills; its lexical findings remain report-only.
preflight_pi checks all names before reading and rendering every source skill
under its inventoried consuming owner, without Git resolution or writes. Ordinary
file rendering uses the nearest manifest owner. The builder must resolve identity and perform
manifest/description checks before invoking preflight. Pi metadata describes
independent packages and script identity; no root registry is generated.
"""

from ._claude import claude_marketplace_metadata, claude_plugin_metadata
from ._codex import codex_marketplace_metadata, codex_plugin_metadata
from ._constructs import (
    CodexConstruct, CodexConstructFinding, PiConstruct, PiConstructFinding,
    scan_codex, scan_pi,
)
from ._markdown import render_file, render_file_result, render_markdown
from ._pi import pi_package_metadata, pi_plugin_metadata, preflight_pi
from ._result import FileRendering

__all__ = [
    "render_file", "render_file_result", "render_markdown", "FileRendering",
    "claude_plugin_metadata", "claude_marketplace_metadata",
    "codex_plugin_metadata", "codex_marketplace_metadata", "CodexConstruct",
    "CodexConstructFinding", "scan_codex",
    "pi_package_metadata", "pi_plugin_metadata", "preflight_pi",
    "PiConstruct", "PiConstructFinding", "scan_pi",
]
