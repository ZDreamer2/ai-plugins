# AiDoc Compaction Workflow

## Overview

Reduce the effort of reading an AiDoc while preserving what its intended reader needs to understand and act.

### Input

- Target AiDoc path
- Optional user emphasis or constraints

### Output

- Improved documentation and aligned metas and references, optionally including satellites; an unchanged result is valid
- Brief report of meaningful changes or reasons for leaving the document unchanged

## Workflow

### Step 1: Establish context

Reuse sufficient, current context already available; read what is missing.

- Read [AiDoc terminology](../../Theory/AiDocTerminology.md) and [writing principles](../../Theory/AiDocBaseFormat.md).
- Locate and read the target's meta. A target meta is required; if missing, create it through the [meta creation workflow](../meta/do.md) before compaction.
- Read the format specified by the meta, including its required context, and the meta's required editing sources. Read relevant optional sources as needed. Resolve `AI_DOC_PLUGIN/...` from this plugin's root (`../../` relative to this workflow); other document references are relative to their containing document.
- Read the complete current target and [documentation usefulness guidance](../../Theory/docs-usefulness.md).

Inspect the target and meta's uncommitted Git changes when available:

```bash
python3 ../../scripts/diff_doc <target-doc-path>
```

Resolve the helper path from this workflow's directory, not the shell's current directory. The target argument is relative to the shell's current directory or absolute. New files are reported by status only; their current contents provide the material to assess.

### Step 2: Assess content and boundaries

Apply usefulness guidance with the target's role, goals, usage context and altitude in mind:

- Assess what earns its reading cost across the whole document. Give recent changes particular scrutiny, including their effects on surrounding content and changes to the meta.
- Consider whether satellite extraction would improve combined reading and navigation effort while leaving the main document useful on its own.

Resolve material uncertainty about intent with the user before making dependent changes. Ordinary edits need no separate approval gate.

### Step 3: Apply justified changes

Revise the target and directly affected documentation according to the assessment, preserving the intended purpose and essential meaning. Leave content unchanged where editing would not improve usefulness.

When satellite extraction is justified:

- Create each satellite's meta through the [meta creation workflow](../meta/do.md).
- Create the satellite through the [AiDoc creation workflow](../build/do.md), using that meta.
- Transfer the detail and adjust the main document's explanation and links. Retain the compact local explanation its reader needs; useful overlap with fuller satellite detail is acceptable.

Align directly affected metas and references with the resulting documentation.

### Step 4: Validate and report

Reread the resulting main document, satellites and affected metas. Check that:

- The target's purpose and essential meaning survive, and the main document remains useful at its intended altitude.
- Changes improve combined reading and navigation effort under the usefulness guidance.
- Documents comply with their formats, metas remain appropriate authoring context and references resolve.

Apply the [shared editorial criteria](../build/workflows/on-build-done.md), then resolve findings and reread revised passages.

Briefly report meaningful cuts or extractions, including satellite paths and unresolved concerns. If the document remains unchanged, explain why.
