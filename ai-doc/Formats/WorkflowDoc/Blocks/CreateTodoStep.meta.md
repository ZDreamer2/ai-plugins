# CreateTodoStep.meta.md

Specification for editing [Todo creation step](CreateTodoStep.md). Defines purpose, usage patterns, and constraints.

## CreateTodoStep.md goals and principles

- Provides authoritative pattern for "Create todo list" step in WorkflowDoc format documents
- Reinforces complete workflow structure through this single step (context -> plan -> todo -> execute)
- Applies consistent "todo list" and "task" terminology across hosts while allowing each agent to track tasks with its available mechanism
- Keeps step minimal - execution guidance belongs in the actual todo list, not the step description

## AiDocFormat

[AiDocBlockFormatDoc format](../../BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing CreateTodoStep.md

- [Workflow design theory](../Theory/WorkflowTheory.md) - Use the planning/execution distinction to position todo creation in the workflow
- [Validation rules block](../../../Blocks/ValidationRules/ValidationRules.md) - Apply when writing verification requirements guidance

## MAY read for additional context before editing CreateTodoStep.md

- [AiDoc creation workflow](../../../workflows/build/do.md) - Read when comparing how an AiDoc workflow connects planning, execution, and verification
- [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) - Read when checking a workflow that makes task breakdown conditional on complexity
- [AiDoc writing principles](../../../Theory/AiDocBaseFormat.md) - Read when clarifying directive language usage (MUST/SHOULD/MAY)

## CreateTodoStep.md typical use context

### 💡 Distinct usage patterns for CreateTodoStep.md

#### Loaded during WorkflowDoc creation when defining todo creation step

User asks to create new workflow -> BuildDocMeta workflow loads WorkflowDoc.format.md -> WorkflowDoc.format.md references CreateTodoStep.md for todo creation step pattern guidance

### Role CreateTodoStep.md serves during use

- Provides standard template for transforming plans into actionable todo lists
- Reinforces workflow structure by positioning todo step between planning and execution
- Guides inclusion of verification tasks in todo lists
- Maintains terminology consistency across all workflow documents
