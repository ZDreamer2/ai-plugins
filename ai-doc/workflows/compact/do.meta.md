# do.meta.md

Specification for creating and editing the [AiDoc compaction workflow](do.md). Defines purpose, usage context and authoring constraints.

## do.md goals and principles

- The workflow reduces the recurring effort of reading an AiDoc while preserving what its intended reader needs to understand and act. Success is improved usefulness, not minimum length; leaving a document unchanged is a valid outcome.
- Compaction can reconsider what content belongs and where it belongs, unlike refinement focused on expressing user edits clearly. This authority serves the document's existing purpose and essential meaning, rather than redesigning the subject it documents.
- A target meta is required because role, goals, usage context and altitude are the basis for judging content. Missing authoring context is established before compaction rather than replaced with assumptions.
- Recent changes deserve particular scrutiny, including changes to the target's meta. They provide a focus, not a boundary: the workflow assesses the resulting document as a whole, without automatically preserving or rejecting newly added content.
- Satellite extraction is available when it improves combined reading and navigation effort, not an expected outcome of compaction. The main document remains useful on its own at its intended altitude; compact local explanations may coexist with fuller satellite detail. Satellites are maintained AiDocs with their own metas, not overflow files.
- The usefulness guidance owns editorial judgment. This workflow owns gathering context, coordinating edits and checking the resulting documents together. The [meta](../meta/do.md) and [build](../build/do.md) workflows own creation mechanics; compaction connects them without developing parallel procedures.

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [Documentation usefulness](../../Theory/docs-usefulness.md) - Owns the reader, abstraction, ownership and reading-cost judgment this workflow applies, including when satellite extraction is worthwhile.
- [Ai-doc skill](../../skills/ai-doc/SKILL.md) - Establishes the dispatch context and neighboring handlers; compact is a distinct branch rather than a broader meaning of refine.
- [StartSimple methodology](../../Theory/StartSimple.md) - Explains why the workflow provides light coordination for established needs rather than an exhaustive editing checklist.

## MAY read for additional context before editing do.md

- [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md) - Relevant when changing how target or satellite metas provide authoring context.
- [Refinement workflow](../refine/do.md) - Relevant when adjusting compact's authority relative to preserving user edits.
- [Shared editorial criteria](../build/workflows/on-build-done.md) - Relevant when shaping final validation; owns the general editorial failure patterns rather than a compact-specific checklist.
- `../../scripts/diff_doc/` - Relevant when changing how the workflow obtains the target and meta's Git changes. The helper chooses the nearest repository and reports new files without printing their contents; current documents provide that content.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Loaded through the ai-doc skill

User requests compaction of an AiDoc -> ai-doc skill dispatches to this workflow -> agent applies shared usefulness guidance with the target's authoring context, including satellite creation when justified.

### Role do.md serves during use

- Coordinates purpose-aware compaction of a selected AiDoc and its directly affected documentation.
- Connects shared editorial judgment with existing AiDoc creation workflows while preserving a coherent main document and satellite set.
