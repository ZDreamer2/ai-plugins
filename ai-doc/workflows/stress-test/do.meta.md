# do.meta.md

Specification for editing [stress-test workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables skeptical, passage-grounded review of uncommitted AiDocs, including the agent's own newly created documents.
- Gives each document a focused review pass in the builder's context. Tool-call boundaries separate the passes even when untracked files have empty diffs or current content needs no reload.
- Bases context loading on sufficiency and freshness. Authorship and Git tracking status do not determine whether a document needs scrutiny.
- Examines the document's contribution as well as its correctness. The motivating reviews improved wording while retaining weak meta goals; format-specific purpose remains relevant even when the text reads cleanly.
- Owns review coordination. The shared editorial criteria and the document's format own the standards applied during review, avoiding a competing checklist here.

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Explains the limit to review machinery justified by observed needs.
- [Shared editorial criteria](../build/workflows/on-build-done.md) - Owns the general editorial criteria used by this workflow.
- [Constraint theory](../../Theory/GuideVsGiveFreedom.md) - Explains the distinction between coordinating passes and prescribing review judgment.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Reviewing working-copy changes

User invokes ai-doc stress-test -> agent reviews the scoped changes with their task context.

#### Reviewing immediately after creation

Builder creates AiDocs -> invokes this workflow in the same session -> reviews new documents whose full text is already in context and may be absent from Git diffs.

### Role do.md serves during use

- Coordinates individual and collective critical review with justified edits and a concise report.
