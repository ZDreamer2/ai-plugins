# WorkflowDoc.format.meta.md

Specification for editing [WorkflowDoc format](WorkflowDoc.format.md). Defines purpose, usage patterns, and constraints.

## WorkflowDoc.format.md goals and principles

- Defines primary AiDocFormat for step-by-step workflow AiDocs that instruct AI agents to complete specific multi-step tasks
- Provides format standards for documents that guide AI through multi-step procedures
- Lets each procedure's task determine its steps while preserving necessary coordination and verification

## AiDocFormat

[AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md)

## MUST read before editing WorkflowDoc.format.md

- [Workflow design theory](Theory/WorkflowTheory.md) - Preserves the rationale for separating or combining workflow steps

## MAY read for additional context before editing WorkflowDoc.format.md

- [CodeDoc format](../CodeDoc/CodeDoc.format.md) - Read when distinguishing workflow requirements from code-specific documentation patterns

## WorkflowDoc.format.md typical use context

### 💡 Distinct usage patterns for WorkflowDoc.format.md

#### Loaded when creating or improving an AI procedure

User requests a multi-step procedure -> ai-doc selects WorkflowDoc format -> the format guides its structure and constraints

### Role WorkflowDoc.format.md serves during use

- Primary format guide for creating step-by-step task instructions
- Ensures balance between procedural clarity and investigative freedom
- Establishes consistent structure across all workflow documents
- Bridge between theory (GuideVsGiveFreedom) and practical workflow implementation
