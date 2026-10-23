# Marketplace build guidance

## Documentation and plugin resources

Every `.md` edit MUST use ai-doc: the `meta` workflow for meta documents and the `build` workflow for other Markdown documents. If a build target has no companion meta, create it through `meta` first. This applies to minor edits too. Reuse sufficient, current context within those workflows. When moving knowledge, move its meta and update live references.

For Markdown edits, MUST apply [authoring syntax](../docs/AuthoringSyntax.md), reading it when sufficient, current context is not already available. It owns skill frontmatter, document references, command paths, agent placeholders and includes.

Shared guidance is authored in the marketplace-root `@common/docs/`; shared scripts and Python libraries belong in `@common/scripts/`.

Plugin manifest fields follow the target marketplace's contract.

## Python

Apply [Python file conventions](python/PythonFile.md) when writing Python and [Python units](python/PythonUnit.md) when changing package structure or public APIs. Read the relevant guidance when it is not already sufficiently available in context. Use the marketplace's supported runtime, dependency provisioning and import mechanism.

## Verification

`on-diff-check` checks Python syntax and JSON parsing for surviving routed files. It does not validate document semantics, run behavior tests or verify packaged artifacts. A result with no `ran` entries means no supported source files were checked.

Choose verification that can detect a plausible failure introduced by the change, while satisfying explicit project checks. Reuse passing evidence while the relevant code, configuration and environment remain unchanged.

- When adding or changing references, command paths or document locations, check the affected resolutions from their containing documents. Wording-only edits do not require a link audit.
- When changing executable behavior, run the tests covering that behavior. Add tests where they establish a useful regression check; a changed file alone does not create a testing requirement.
- When changing resource inclusion, dependency provisioning, rendering or host integration, verify the affected distribution contract. Use source inspection or focused tests where they establish it; build artifacts or run an installed host when the result depends on packaging or host behavior that those checks cannot establish.

Broaden verification when a failure or unresolved dependency warrants it. Full suites, distribution builds and installed-host sessions are not routine follow-ups to successful focused checks.
