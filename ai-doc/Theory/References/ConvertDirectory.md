# Convert references in a directory

## Input

A source directory and any requested exclusions.

## Workflow

### Step 1: Inventory files

Read the [file conversion workflow](ConvertFiles.md). Recursively list Markdown files with their absolute paths and byte sizes, including meta documents and hidden or ignored source files. Exclude repository metadata, generated output, installed caches, and dependencies; record exclusions. Count each physical file once and stay within the requested directory.

Keep an inventory of files, batch ownership, and results outside the conversion scope.

### Step 2: Distribute batches

Group files into batches of at most 20 KB (20,000 bytes) total source size. A file larger than that limit gets a batch of its own. Launch a fresh-context worker for each batch, up to the available concurrency, supplying this prompt with absolute paths:

```text
Follow <path to ConvertFiles.md> for these files:
<assigned file paths>
```

Assign each file to only one worker at a time. Dispatch remaining batches as workers finish and record their results. Before reassigning interrupted work, confirm the previous worker has stopped and inspect any partial edits.

### Step 3: Verify completion

Reconcile worker results against the inventory and a fresh directory listing. Review the combined changes for scope and reference integrity; resolve or report incomplete conversions. Every in-scope file needs a result before the run is finished.

Report file counts, exclusions, checks performed, and remaining issues. Leave changes uncommitted.
