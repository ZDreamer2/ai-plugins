# CommandWorkflow.meta.md

Specification for editing [Command workflow patterns](CommandWorkflow.md). Defines purpose, usage patterns, and constraints.

## CommandWorkflow.md goals and principles

- Documents Claude Code skill/command-specific patterns for workflow authoring
- Covers syntax and mechanics unique to workflows invoked as skills (via /command)
- Complements WorkflowDoc.format.md with command-specific considerations

## AiDocFormat

[BaseDoc format](../../BaseDoc/BaseDoc.format.md)

## MUST read before editing CommandWorkflow.md

- [WorkflowDoc format](../WorkflowDoc.format.md) - Understand base workflow structure that CommandWorkflow.md extends with command-specific guidance

## CommandWorkflow.md typical use context

### 💡 Distinct usage patterns for CommandWorkflow.md

#### Loaded during WorkflowDoc creation when workflow is a skill/command

User asks to create workflow that will be invoked as /command -> BuildDoc workflow loads WorkflowDoc.format.md -> WorkflowDoc.format.md MAY reference CommandWorkflow.md for command-specific patterns

### Role CommandWorkflow.md serves during use

- Reference for command/skill-specific workflow patterns
- Explains Claude Code syntax elements relevant to skill workflows
