# UserApprovalStep.meta.md

Specification for editing [User approval step](UserApprovalStep.md). Defines purpose, usage patterns, and constraints.

## UserApprovalStep.md goals and principles

- Guide creation of steps where workflow pauses for user approval before proceeding
- Surface the active agent's question tool as an option for structured approval, including multiple selections
- Keep guidance light - trust AI to choose appropriate approval format based on context

## AiDocFormat

[AiDocBlockFormatDoc format](../../BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## UserApprovalStep.md typical use context

### Distinct usage patterns for UserApprovalStep.md

#### Loaded during WorkflowDoc creation when defining approval step

User asks to create workflow with approval gate -> BuildDocMeta loads WorkflowDoc.format.md -> WorkflowDoc.format.md references UserApprovalStep.md for approval step pattern guidance

### Role UserApprovalStep.md serves during use

- Template provider for creating approval steps in workflow documents
- Reminder that the active agent's question tool can structure approval
