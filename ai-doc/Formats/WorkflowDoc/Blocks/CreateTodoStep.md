# Create Todo List Step Block Format

## CreateTodoStep template

```markdown
### Step [N]: Create todo list for execution

Create a detailed task breakdown:
- Transform the plan into specific, actionable tasks
- Todo list MUST include verification tasks at the end:
  - [Verification task]
  - [Verification task]
```

## Template Notes

This step bridges planning and execution phases in the workflow structure (context -> plan -> todo -> execute).

### [N]

Step number where todo creation occurs, typically follows immediately after planning step.

### [Verification task]

- Domain-specific verification requirements that ensure work quality and completeness
- Each workflow determines its own verification tasks based on context
- Write verification tasks as actionable items using MUST/SHOULD/MAY directive language when appropriate

## CreateTodoStep example

From the [AiDoc creation workflow](../../../workflows/build/do.md):

```markdown
### Step 3: Create todo list for execution

Create a detailed task breakdown:
- Transform the plan into specific, actionable tasks
- Todo list MUST include verification tasks at the end:
  - Verify against AiDocFormat specified in AiDocMetaDoc using its Validation Rules section
  - Verify all AiDocMetaDoc goals and principles are met
```

## Validation Rules

- MUST follow template structure from template section
- MUST include verification tasks requirement
- MUST position step immediately after planning step in workflow sequence
- Verification tasks SHOULD be specific to workflow domain rather than generic
