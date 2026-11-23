# Compile marketplace distributions

## Overview

Compile and validate the current working tree of one marketplace source checkout with the shared Python tooling bundled with ai-marketplace.

### Input

- The authoritative source checkout.
- Any repository-specific checks or requested fresh-session trial.

### Output

- Local Claude, Codex and Pi distributions under the source checkout's `@build/`.
- Compilation, validation and applicable domain-check results with source and tooling provenance.

## Workflow

### Step 1: Establish the source checkout and tooling

Select exactly one authoritative source checkout, rather than a generated distribution, and read its source-repository instructions. Set `SOURCE` to its absolute path and `OUTPUT` to `$SOURCE/@build`.

Resolve these paths from this document to absolute paths:

- `../../../../scripts/build.py` -> `BUILD_SCRIPT`
- `../../../../scripts/validate_pi.py` -> `PI_VALIDATOR`

Use these bundled shared tools rather than a marketplace's historical builder snapshot. Compilation requires Python 3.10+ and Git; the Python dependencies are bundled.

### Step 2: Compile and validate the working tree

Record the source revision and pending changes. Establish the tooling Git revision and any tooling working-tree changes when Git metadata is available; otherwise retain the resolved tooling path and report that its revision is unavailable.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -S "$BUILD_SCRIPT" --dir "$SOURCE" --output-dir "$OUTPUT"
PYTHONDONTWRITEBYTECODE=1 python3 -B -S "$PI_VALIDATOR" --dir "$SOURCE" --tree "$OUTPUT/pi" --output-dir "$OUTPUT"
```

The builder reads the current files, including uncommitted edits, and replaces the generated host trees under `@build/`. Do not clean, stash or commit source changes to make compilation run. Failed compilation or Pi validation is the reported result; do not synchronize or publish around it.

### Step 3: Run applicable domain checks

Follow the source repository's instructions for checks relevant to the changed plugins. Run skill self-tests against the rendered files in `@build/`, not against source templates, when that distinction applies. Inspect the generated construct reports and expected plugin inventory.

Compilation and Pi validation establish rendering and package structure, not domain behavior or installed-host acceptance. Keep additional domain verification visible in the result.

### Step 4: Report the result and support an isolated trial

Report:

- The source revision and whether uncommitted changes were included.
- The tooling revision and dirty state, or the tooling path and why no revision is available.
- The absolute output location and the compilation, Pi validation and domain-check outcomes.
- Any remaining verification boundary.

For a requested fresh-session trial, follow the source repository's host-specific procedure using the packages under `@build/` in a separate test workspace. Keep the user's normal installed plugins unchanged. If no isolated procedure is available, report the built package paths and stop rather than replacing an existing installation.

Compile does not commit, push, publish, trigger CI or rebuild consumers. Source sharing belongs to Sync; publication and consumer rebuilds are subsequent outcomes to verify separately.
