# WorkflowDoc.md underlying theory

## Important Definitions section handling

Some workflows may have an "Important Definitions" section at the very beginning, added by users to define key terms specific to that workflow. When present, this section should be preserved without modification unless explicitly asked otherwise - the definitions are carefully chosen for the workflow's specific context and domain.

## Step boundaries

Separate actions into distinct steps when their order matters or a later action depends on an earlier result. Otherwise, keep related work together.

## Content principle: reference rather than duplicate

When a workflow requires AI to understand concepts documented elsewhere, reference that documentation instead of copying content into the workflow. This ensures knowledge stays in one place, remains maintainable, and workflows stay focused on procedure rather than explanation.
