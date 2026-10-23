# UserApprovalStep Block Format

## UserApprovalStep template

UserApprovalStep is used when a workflow needs user confirmation before proceeding. Common in workflows where AI proposes changes, options, or plans that require explicit approval.

```markdown
### Step [N]: Present [what] for approval

Present findings to user:
- [What to present and how]
- Consider ${AGENT_QUESTION_TOOL} to structure approval, including multiple selections when useful
- Wait for user approval before proceeding
```

Template notes:
- `[N]` - Step number in the workflow sequence
- `[what]` - Brief description of what's being presented (e.g., "optimization plan", "migration strategy")
- `[What to present and how]` - Specific guidance for this workflow's approval content
- The question tool is a consideration, not a requirement - AI chooses based on context

## UserApprovalStep example

```markdown
### Step 3: Present optimization plan

Present findings to user:
- List each optimization opportunity with rationale
- Consider ${AGENT_QUESTION_TOOL} to structure approval, including multiple selections when useful
- Wait for user approval before proceeding
```

## Validation Rules

- MUST include "Wait for user approval before proceeding" or equivalent gate
- MUST mention the available question tool as a consideration for structured approval
- SHOULD specify what content to present to user
