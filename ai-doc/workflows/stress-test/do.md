# Stress-Test AiDoc Changes

## Overview

Critically review and improve current AiDoc changes through focused individual and collective review passes.

### Input

- Uncommitted AiDoc changes, including newly created files
- Optional narrower review scope or additional context

### Output

- Reviewed documents with justified improvements applied
- Brief report of improvements and unresolved questions

## Why separate review calls

Each tool round trip gives the next document a dedicated review inference, keeping scrutiny focused on its changes rather than a general impression of the change set. When sufficient, current context is already available, a no-output command separates the passes without reloading it.

## Workflow

### Step 1: Establish scope and understand changes

Review all AiDocs changed in the working copy, including untracked files, unless the invoking prompt narrows the scope. Use the task context and Git status to establish what changed and why. A new document's entire content is in scope; an empty Git diff does not exclude it.

Reuse document content, diffs, meta documents, and editorial criteria already available in context when sufficient and current, regardless of who authored the changes. You need to understand the current document and identify the changes under review. Read only what is missing or may be stale, including after truncated output, lost context, or concurrent edits.

### Step 2: Gather editing context

For each document, use its AiDocMetaDoc if present, reading it only when the available context is insufficient or stale. A missing meta does not block review. When the reviewed document is itself a meta, use the [meta format](../../Formats/MetaDoc/AiDocMetaDoc.format.md) and its target's purpose and use as the review context.

Use the [shared editorial criteria](../build/workflows/on-build-done.md) for the review passes; load them if not already available in context.

### Step 3: Stress-test each document

MUST start each document's pass with a separate tool call:

- Sufficient, current context is available: run `true` in the shell tool. You MAY refresh context when useful.
- Context is missing or stale: read the needed document content or diff. When both are needed for a tracked file, use `cat -- 'path/to/document.md' && git diff HEAD -- 'path/to/document.md'` to place the changes last for review.
- Untracked file needing context: read the needed content. Its entire content is in scope.

Use the actual document path. Git diff against HEAD includes staged and unstaged changes; regenerating it is unnecessary when the changes are already understood and current.

MUST review the changes immediately after the tool result, in their document context, before starting the next pass; do not batch these calls.

Apply the [shared editorial criteria](../build/workflows/on-build-done.md) to concrete passages and their consequences in the document's intended use. Ask what necessary knowledge each passage adds beyond the reader's existing context and required references. A plausible or correct statement can still be redundant. Remove or consolidate passages that add no decision value; correct guidance that would lead the reader astray.

For a meta, apply the format's [goals and principles criterion](../../Formats/MetaDoc/AiDocMetaDoc.format.md#aidocnamemd-goals-and-principles-section) to its contribution to future editing, not just its wording and structure.

Apply justified improvements. A clean result is valid when scrutiny supports it.

### Step 4: Stress-test the documents together

MUST begin the collective pass with a separate shell-tool call running `true` and review immediately after the result.

Review the resulting documents together against the [shared editorial criteria](../build/workflows/on-build-done.md), including their boundaries, repetition and reading dependencies. Apply justified improvements and revisit individual documents when findings warrant it.

If this pass changed anything, run one more collective pass, then stop. Surface decisions requiring user input instead of cycling around them; continue independent review work.

### Step 5: Report the result

Briefly state what was reviewed, what improved, and any unresolved questions. Distinguish a completed review from work awaiting user input.
