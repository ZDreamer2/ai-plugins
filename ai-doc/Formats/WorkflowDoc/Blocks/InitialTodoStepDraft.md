# InitialTodoStep Block

## Purpose

Optional workflow block that creates a reminder todo list at workflow start. Leverages Claude Code's high attention to active todo items to prevent missing important steps.

## When to Use

When workflow has steps that are easy to miss or forget during main work. Not needed for linear workflows where each step naturally leads to the next.

## Key Design Principles

### Reminders, Not Task List

The todo list contains reminders for things easily missed - not the main work itself. Main activity is implicit (you're doing it), todos are checkpoints.

Wrong framing - task list that overshadows main work:
```
1. Load context
2. Research code
3. Check documentation
4. Assess sufficiency
5. Save plan
```

Right framing - reminders while doing main work:
```
"Don't forget while researching":
1. Check Index.md for relevant docs
2. Assess context sufficiency
3. Call /issue:chunk:savePlan
```

### Naming Convention

Name conveys that main task is implicit: "Don't forget while {MainActivity}"

Examples:
- "Don't forget while researching"
- "Don't forget while implementing"
- "Don't forget while reviewing"

### Step References

Link todo items to workflow steps for easy navigation to details:
```
1. Check Index.md for relevant docs (Step 2)
2. Assess context sufficiency (Step 3)
```

## Template

```markdown
### Step 0: Create todo list

Create todo list "Don't forget while {MainActivity}":
1. {Reminder item} (Step N)
2. {Reminder item} (Step M)
```

## Example

From PlanChunk workflow where main activity is research:

```markdown
### Step 0: Create todo list

Create todo list "Don't forget while researching":
1. Check Index.md for relevant docs (Step 2)
2. Assess context sufficiency (Step 3)
3. Call /issue:chunk:savePlan
```
