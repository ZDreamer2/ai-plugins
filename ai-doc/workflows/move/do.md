# MoveDocs Workflow Documentation

## Overview

Moves documentation files while maintaining reference integrity across the codebase.

### Input
- Source path (file or folder)
- Destination path

### Output
- Files moved to new location
- All references updated
- No broken references remain

## Workflow

### Step 1: Identify files to move

Review foundational document:
- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Apply the AiDocMetaDoc naming convention when pairing documents for the move

Determine all files that need moving:
- For single file: check for accompanying .meta.md file (per the [AiDocMetaDoc naming convention](../../Theory/AiDocTerminology.md#aidocmetadoc-files))
- For folder: list all contents including .meta.md files

### Step 2: Search for references

Before moving, find all references to the source paths:

```
../../scripts/find-doc.py <path fragment>
```

Search tools respect .gitignore by default and skip nested repositories without any signal, so this script SHOULD be used in their place for first pass at least.

Classify the results before editing. Live references are updated; append-only records - session logs, finished plans, IDE state - are left as written. Pass `--exclude <name>` to drop a classified directory from later runs.

Include Markdown links, frontmatter paths and legacy literal references. Interpret their bases using the [reference path rules](../../Theory/References/ReferencePathManagement.md).

### Step 3: Move files

For each identified file, call:

```
../../scripts/move-doc.py <source> <destination>
```

`<source>` and `<destination>` have the same meaning as in `git mv`.

### Step 4: Update references

Update all found references in source files:
- Replace old paths with new paths
- Maintain original reference format
- Rebase document-relative references inside moved files so they still resolve to the same targets. Keep `AI_DOC_PLUGIN/...` references plugin-root-relative.

### Step 5: Verify no broken references

Re-run the Step 2 search. What remains MUST be only the records deliberately left as written.

## Key Principles

- .meta.md files MUST move together with their main AiDocs
- Verification is mandatory - workflow incomplete without confirming no broken references
