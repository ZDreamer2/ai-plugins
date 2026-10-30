"""Intent: own marketplace output production and its rendering subunit.

Usage:
    from marketplace.build import build, CodexConstructReport, PiConstructReport
    from marketplace.build.rendering import render_file_result

    result = render_file_result(text, path, "codex", source)
    report = CodexConstructReport()
    report.add(path, plugin_root, result.findings)
    markdown = report.render()
    notes = report.summaries()
    total = report.total()

    built = build("/path/to/marketplace", output_dir="/path/to/output")
    preview = build("/path/to/marketplace", dry_run=True)

PiConstructReport exposes the same collection and formatting API for Pi's
report-only adaptation findings, all carrying rendered line numbers.
Report collection and formatting are read-only: callers supply logical paths
and findings, and decide whether and where to write the returned Markdown.
build accepts a source directory, optional output directory (default source/@build)
and dry_run. An optional datetime now controls fallback identities and the Moscow
installer stamp. Optional source-root .marketplace/identity.json supplies catalog
branding and the Pi package prefix; its five fields are validated even for dry
runs and empty inventories. Missing configuration preserves zd-plugins defaults.
It preflights all identities, descriptions and Pi skills before
replacing Claude/Codex/Pi trees, then bundles Claude installers when sources exist.
BuildResult returns canonical locations, plugin count, per-tree source counts,
companions, metadata notes, reports and installer byte counts without printing.
Dry runs render and validate without filesystem writes. Empty inventories leave
trees and reports intact, but can still bundle installers. ValueError describes
invalid inputs/rendering/bundling; filesystem failures raise OSError. Later failures
can leave partial output after successful preflight; source inputs remain unchanged.
"""

from ._build import BuildResult, TreeResult, build
from ._reports import CodexConstructReport, PiConstructReport

__all__ = ["build", "BuildResult", "TreeResult", "CodexConstructReport", "PiConstructReport"]
