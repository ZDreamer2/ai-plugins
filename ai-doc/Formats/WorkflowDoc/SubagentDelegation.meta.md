# SubagentDelegation.meta.md

Specification for editing [subagent delegation guidance](SubagentDelegation.md). Defines purpose, usage patterns, and constraints.

## SubagentDelegation.md goals and principles

- Helps workflow authors preserve stable delegation prompts for consistent reuse
- Distinguishes prompts that rely on inherited context from self-contained prompts
- Keeps guidance focused on reusable prompts and result dependencies without prescribing a step template

## AiDocFormat

[BaseDoc format](../BaseDoc/BaseDoc.format.md)

## MUST read before editing SubagentDelegation.md

- [WorkflowDoc editing context](WorkflowDoc.format.meta.md) - Preserves the parent format's scope and boundaries
- [StartSimple methodology](../../Theory/StartSimple.md) - Keeps guidance limited to non-obvious recurring delegation needs

## SubagentDelegation.md typical use context

### 💡 Distinct usage patterns for SubagentDelegation.md

#### Loaded when creating a workflow with recurring delegated work

WorkflowDoc format identifies a reusable subagent prompt -> loads SubagentDelegation.md for prompt and context guidance

### Role SubagentDelegation.md serves during use

- Concise guidance for preserving reusable subagent prompts
- Distinction between inherited and self-contained context
- Reminder to connect the returned result to dependent workflow work
