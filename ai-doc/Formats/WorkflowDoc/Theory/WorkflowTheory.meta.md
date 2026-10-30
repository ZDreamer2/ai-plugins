# WorkflowTheory.meta.md

Specification for editing [workflow design theory](WorkflowTheory.md). Defines purpose, usage patterns, and constraints.

## WorkflowTheory.md goals and principles

- Provides theoretical foundation explaining design decisions in WorkflowDoc.format.md
- Explains how ordering and intermediate results shape workflow steps
- Contains theoretical principles behind workflow design patterns
- MUST NOT be used during workflow execution - only loaded when editing WorkflowDoc.format.md

## AiDocFormat

[BaseDoc format](../../BaseDoc/BaseDoc.format.md)

## MUST read before editing WorkflowTheory.md

- [WorkflowDoc format](../WorkflowDoc.format.md) - Keep the theory aligned with the workflow structure it explains
- [Constraint theory](../../../Theory/GuideVsGiveFreedom.md) - Apply its distinction between proven patterns and investigative freedom

## MAY read for additional context before editing WorkflowTheory.md

- [AiDoc creation workflow](../../../workflows/build/do.md) - Read when checking how ordered context gathering applies the theory
- [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) - Read when checking how conditional context gathering applies the theory

## WorkflowTheory.md typical use context

### 💡 Distinct usage patterns for WorkflowTheory.md

- Edit [WorkflowDoc format](../WorkflowDoc.format.md)
  - WorkflowDoc.format.meta.md will reference WorkflowTheory.md in its MUST read section
  - Provides theoretical foundation for understanding WorkflowDoc.format.md design decisions

### Role WorkflowTheory.md serves during use

- Explains rationale behind workflow structure patterns
- Clarifies when actions should be separated into steps or kept together
- Provides theoretical foundation for balancing structure with flexibility
- Connects high-level principles (GuideVsGiveFreedom.md) to concrete workflow patterns
