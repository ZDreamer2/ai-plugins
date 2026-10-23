# PlanExecutePattern.meta.md

Specification for editing [Plan-Execute pattern](PlanExecutePattern.md). Defines purpose, usage patterns, and constraints.

## PlanExecutePattern.md goals and principles

- Explain the 4-step workflow pattern: context -> plan -> todo -> execute
- Document WHY each phase exists and WHY they are separate
- Focus on pattern mechanics and reasoning
- MUST NOT include "when to use" guidance (provided by referencing documents)

## AiDocFormat

[BaseDoc format](../../BaseDoc/BaseDoc.format.md)

## MUST read before editing PlanExecutePattern.md

- [AiDoc creation workflow](../../../workflows/build/do.md) - Compare its context and execution phases when explaining phase boundaries
- [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) - Compare its analysis and validation phases when explaining sequencing

## PlanExecutePattern.md typical use context

### Distinct usage patterns for PlanExecutePattern.md

#### Referenced from WorkflowDoc.format.md MAY read section

Create workflow according to the [WorkflowDoc format](../WorkflowDoc.format.md)

AI agent reads MAY read section, sees PlanExecutePattern.md is relevant for their workflow type, loads it.

### Role PlanExecutePattern.md serves during use

- Provides structural understanding of the 4-step pattern for workflow authors
- Explains separation rationale (consistent structure, execution contract)
- Informs workflow design decisions about phase boundaries
