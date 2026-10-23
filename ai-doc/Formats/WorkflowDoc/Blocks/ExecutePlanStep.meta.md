# ExecutePlanStep.meta.md

Specification for editing [Execute plan step](ExecutePlanStep.md). Defines purpose, usage patterns, and constraints.

## ExecutePlanStep.md goals and principles

- Guide creation of minimal "Execute plan" steps that trust todo list guidance
- Reinforce 4-step workflow pattern (context -> plan -> todo -> execute)
- Prevent redundant instructions that duplicate todo list content
- Explain WHY minimal guidance works better than detailed prescription
- Connect minimal approach to [constraint theory](../../../Theory/GuideVsGiveFreedom.md) principles

## AiDocFormat

[BaseDoc format](../../BaseDoc/BaseDoc.format.md)

## MUST read before editing ExecutePlanStep.md

- [Why execution uses minimal guidance](../Theory/PlanExecutePattern.md#why-execute-uses-minimal-guidance) - Apply the rationale for relying on the prepared todo list during execution
- [Constraint theory](../../../Theory/GuideVsGiveFreedom.md) - Understand when to constrain vs trust AI judgment, apply to execution step context
- [AiDoc creation workflow](../../../workflows/build/do.md) - Examine Step 3 for concise instructions to create or improve the AiDoc
- [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) - Examine Step 3 for concise instructions to create or improve the AiDocMetaDoc

## ExecutePlanStep.md typical use context

### Distinct usage patterns for ExecutePlanStep.md

#### Loaded during WorkflowDoc creation when defining execution step

User asks to create new workflow -> BuildDocMeta workflow loads WorkflowDoc.format.md -> WorkflowDoc.format.md references ExecutePlanStep.md for guidance on execution step pattern

#### Referenced during WorkflowDoc editing to understand execution step design

User asks to improve workflow execution step -> BuildDoc workflow loads WorkflowDoc.meta.md -> WorkflowDoc.meta.md points to ExecutePlanStep.md for execution step guidance

### Role ExecutePlanStep.md serves during use

- Prevent over-specification of execution steps that would duplicate todo list guidance
- Explain workflow structure rationale to help authors understand the pattern
- Point to concrete examples demonstrating the minimal approach in practice
- Reinforce consistency across all WorkflowDoc documents
