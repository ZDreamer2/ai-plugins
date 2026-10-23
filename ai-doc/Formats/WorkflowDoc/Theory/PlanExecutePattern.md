# Plan-Execute Pattern

## The Pattern

Four sequential phases structure workflows with separated planning and execution:

1. Context phase - Read files, check prerequisites, initialize needed resources
2. Planning phase - Plan based on gathered content
3. Todo creation phase - Create concrete todo list from the plan
4. Execution phase - Execute the tasks

This core pattern (context -> plan -> todo -> execute) ensures each phase completes before the next begins.

## Why Sequential Phases

Separate phases earn their place when a later phase depends on an earlier one's actual output: a plan built from files' contents, or a plan the user reviews before execution. State that dependency where it exists; otherwise let the agent plan as it works.

## Why Planning and Todo Creation Are Separate

Separating planning from todo creation maintains clean workflow structure:

- Planning determines the approach; todo creation translates it into concrete tasks
- The todo list serves as the execution contract between planning and execution phases

## Why Execute Uses Minimal Guidance

The execution step deliberately contains minimal instruction ("Work through todo list"). The todo list created in the previous step already contains all execution guidance. The AI has full context from earlier steps and specific tasks from the todo list. Adding more instructions would just repeat what's already there.

## Terminology

Use the terms "todo list" and "task" consistently for the concrete work items, whether the agent tracks them with a task tool or in its working context. This avoids confusion with alternative terms like "plan items," "steps," or "actions."
