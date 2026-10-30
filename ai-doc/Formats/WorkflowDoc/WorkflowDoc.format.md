# WorkflowDoc Format Specification

## What is document in WorkflowDoc format

A WorkflowDoc is a step-by-step procedure that instructs AI agents to complete a task while balancing structured coordination with investigative freedom.

## MUST read before planning WorkflowDoc document

- [Constraint theory](../../Theory/GuideVsGiveFreedom.md) - Apply when determining step specificity vs flexibility
- [Workflow design theory](Theory/WorkflowTheory.md) - Use its guidance to choose the workflow structure and reference shared concepts
- [AiDocMetaDoc creation workflow](../../workflows/meta/do.md) - Study its conditional context gathering and validation as a structure example
- [AiDoc creation workflow](../../workflows/build/do.md) - Study its ordered reading dependencies and validation as a structure example

## MAY read for additional context before planning WorkflowDoc document

- [User approval step](Blocks/UserApprovalStep.md) - Read when workflow needs user approval before proceeding
- [Subagent delegation step](Blocks/CallSubagentStep.md) - Read when workflow delegates work to subagents

## WorkflowDoc template

```markdown
# [Workflow Name] Documentation

## Important Definitions (optional)

[Rarely needed. Domain-specific terminology required for this workflow]

## Overview

[One-sentence purpose statement]

### Prerequisites (optional)
- [Required conditions, tools, or knowledge]

### Input
- [What the workflow receives or requires to start]

### Output
- [What the workflow produces or accomplishes]

## Workflow

### Step 1: [Active Verb + Clear Action]
[Guidance for this step]

### Step 2: [Next Action]
[Guidance for next step]

### Step N: [Final Action]
[Guidance for final step]

## Key Principles (optional)

- [Critical constraint or pattern]
- [Important consideration]
```

## Template Notes

### "Important Definitions" section

Rarely needed. When present, preserve without modification unless explicitly asked otherwise.

### Workflow Steps section

Number steps sequentially. Each step title MUST start with an active verb describing the action.

### "Key Principles" section

Include when workflows have important constraints or patterns that don't fit naturally within step descriptions.

## WorkflowDoc example

Study these workflow examples to understand practical patterns:

- [AiDoc creation workflow](../../workflows/build/do.md) - Demonstrates ordered context gathering, execution, and validation
- [AiDocMetaDoc creation workflow](../../workflows/meta/do.md) - Demonstrates conditional context gathering and format selection

## Validation Rules

- MUST follow template structure from template section
- MUST comply with [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- Each step title MUST start with active verb
- MUST number steps sequentially
- MUST balance specificity (coordination, proven patterns) with flexibility (investigation, problem-solving)
- SHOULD reference existing documentation rather than duplicating knowledge
