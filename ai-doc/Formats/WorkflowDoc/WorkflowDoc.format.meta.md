# WorkflowDoc.format.meta.md

Specification for editing [WorkflowDoc format](WorkflowDoc.format.md). Defines purpose, usage patterns, and constraints.

## WorkflowDoc.format.md goals and principles

- Defines primary AiDocFormat for step-by-step workflow AiDocs that instruct AI agents to complete specific multi-step tasks
- Provides format standards for workflow documents typically found in /Workflows/ directories
- Emphasizes clarity in some steps while trusting AI investigation capabilities in other steps

## AiDocFormat

[AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md)

## MUST read before editing WorkflowDoc.format.md

- [Workflow design theory](Theory/WorkflowTheory.md)
  - Use its design principles to preserve the rationale for workflow structure
  - Essential for understanding WHY workflows are structured with separated planning, todo creation, and execution steps
- [AiDocMetaDoc creation workflow](../../workflows/meta/do.md)
  - Study its context gathering and validation as an example for workflow authors
  - WorkflowDoc.format.md MUST encourage to consider it as example when creating workflows
- [AiDoc creation workflow](../../workflows/build/do.md)
  - Study its reading dependencies and ordered execution as an example for workflow authors
  - WorkflowDoc.format.md MUST encourage to consider it as example when creating workflows

## MAY read for additional context before editing WorkflowDoc.format.md

- [CodeDoc format](../CodeDoc/CodeDoc.format.md) - Read when distinguishing workflow requirements from code-specific documentation patterns

## WorkflowDoc.format.md typical use context

### 💡 Distinct usage patterns for WorkflowDoc.format.md

- Create workflow documentation for building features following the [WorkflowDoc format](WorkflowDoc.format.md)
  - Direct reference when creating new workflow AiDocs
- Build `docs/Workflows/BuildFeature.md` following the [AiDoc creation workflow](../../workflows/build/do.md)
  - Will be automatically used, because AiDocMetaDoc document for BuildFeature.md will guide to use WorkflowDoc.format.md
  - And AiDocMetaDoc will be created to guide this way automatically by [AiDocMetaDoc format](../MetaDoc/AiDocMetaDoc.format.md) since BuildFeature.md is in workflows directory

### Role WorkflowDoc.format.md serves during use

- Primary format guide for creating step-by-step task instructions
- Ensures balance between procedural clarity and investigative freedom
- Establishes consistent structure across all workflow documents
- Bridge between theory (GuideVsGiveFreedom) and practical workflow implementation
