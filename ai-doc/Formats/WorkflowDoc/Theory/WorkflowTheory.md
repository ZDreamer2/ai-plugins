# WorkflowDoc.md underlying theory

## Important Definitions section handling

Some workflows may have an "Important Definitions" section at the very beginning, added by users to define key terms specific to that workflow. When present, this section should be preserved without modification unless explicitly asked otherwise - the definitions are carefully chosen for the workflow's specific context and domain.

## Plan-Execute Pattern

Some workflows benefit from separated planning and execution phases, particularly those involving creative/analytical work where users may want to review and iterate on plans before execution.

This 4-step pattern (context -> plan -> todo -> execute) is documented in the [Plan-Execute pattern](PlanExecutePattern.md).

Not all workflows need this structure. Procedural workflows with deterministic steps (like moving files) can use simpler sequential structures.

## Content principle: reference rather than duplicate

When a workflow requires AI to understand concepts documented elsewhere, reference that documentation instead of copying content into the workflow. This ensures knowledge stays in one place, remains maintainable, and workflows stay focused on procedure rather than explanation.
