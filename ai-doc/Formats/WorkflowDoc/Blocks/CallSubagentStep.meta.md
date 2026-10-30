# CallSubagentStep.meta.md

Specification for editing [Subagent delegation step](CallSubagentStep.md). Defines purpose, usage patterns, and constraints.

## CallSubagentStep.md goals and principles

- Extends [WorkflowDoc format](../WorkflowDoc.format.md) for steps that delegate work to subagents
- MUST NOT duplicate information from [WorkflowDoc format](../WorkflowDoc.format.md)
- Covers two distinct subagent modes: fork (inherits parent context) and fresh (independent context)
- Each mode states how it is called, not only what it is, so an author copying the template ends up with a tool named in the step
- Loaded when a workflow needs to call subagents via ${AGENT_SUBAGENT_TOOL} tool

## AiDocFormat

[Block format specification](../../BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing CallSubagentStep.md

- [WorkflowDoc editing context](../WorkflowDoc.format.meta.md) - Understand parent format context and what WorkflowDoc.format.md already covers
- [Workflow design theory](../Theory/WorkflowTheory.md) - Apply its design principles to the structure of delegation steps
- [StartSimple methodology](../../../Theory/StartSimple.md) - Start minimal and expand only when evidence shows gaps

## CallSubagentStep.md typical use context

### 💡 Distinct usage patterns for CallSubagentStep.md

#### Loaded during WorkflowDoc creation when defining subagent step

User asks to create workflow with subagent delegation -> BuildDocMeta loads WorkflowDoc.format.md -> WorkflowDoc.format.md references CallSubagentStep.md for subagent step pattern guidance

### Role CallSubagentStep.md serves during use

- Template provider for creating subagent invocation steps in workflow documents
- Defines when to use fork vs fresh context and how to express this in workflow steps
