# Execute Plan Step

## Purpose

Guides AI to work through the todo list created in the previous step. This step marks the transition from planning to execution in the [Plan-Execute pattern](../Theory/PlanExecutePattern.md).

## Standard Template

```
### Step [N]: Execute plan

Work through todo list [completing the specific work]
```

## Template Explanations

- `[completing the specific work]` - Brief description matching the work scope from planning step (e.g., "creating/improving AiDoc", "building repository")
- Keep this step minimal - the todo list already contains all execution guidance, additional instructions would be redundant

## Why Minimal Guidance Works

The execute plan step deliberately contains minimal instruction. This design is based on several factors:

### Todo list provides execution guidance

The todo list created in the todo creation step already contains all specific tasks and verification requirements. The AI has full context from earlier workflow steps and specific tasks from the todo list. Adding more instructions would duplicate what's already there.

### Trust AI's task management abilities

AI agents excel at executing concrete tasks when given clear objectives and full context. The workflow already provided both through context loading and todo creation phases. Additional prescription constrains these capabilities without adding value.

### Aligns with proven principles

This minimal approach follows [constraint theory](../../../Theory/GuideVsGiveFreedom.md) - trust execution when proven patterns (the todo list) are already in place. Constrain coordination (via todo list), not problem-solving (during execution).

## Examples

Working implementations of this pattern:

- [AiDoc creation workflow](../../../workflows/build/do.md) - See Step 3 for minimal execution step in AiDoc creation workflow
- [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) - See Step 3 for minimal execution step in AiDocMetaDoc workflow
