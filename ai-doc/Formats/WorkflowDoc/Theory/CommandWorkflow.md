# Command Workflow Patterns

Patterns specific to workflows invoked as Claude Code skills/commands.

## Frontmatter

Command workflows use YAML frontmatter for skill system integration:

```yaml
---
description: Short description of what command does
user-invocable: true
disable-model-invocation: true
---
```

Required fields:
- `user-invocable: true` - registers as user command
- `disable-model-invocation: true` - prevents AI auto-invocation

Optional fields:
- `description:` - short description shown in command list

Frontmatter handling when editing:
- IF workflow has no frontmatter THEN add it with appropriate description
- IF workflow already has frontmatter THEN preserve it unless user explicitly asks to modify

## Explicit File References

Follow the [reference path rules](../../../Theory/References/ReferencePathManagement.md): use document-relative Markdown links and state required reading explicitly. MUST NOT use `@path` context injection. Reuse context already read when it remains sufficient and current.

Example for a workflow in `docs/workflows/`:
```markdown
### Step 1: Load foundational context

Read files that frame the investigation:
- [Code unit structure](../code/Unit/CodeUnit.md) - Use its conventions to identify the unit under investigation
- [Code documentation index](../code/on-plan.md) - Find relevant guidance for the investigation
```

## Command Registration via Symlink

When user provides a command name for the workflow, create a relative symlink in `.claude/commands/`.

Command name to path mapping:
- `/code:test:optimize` -> `.claude/commands/code/test/optimize.md`
- `/doc:build` -> `.claude/commands/doc/build.md`
- Colons (`:`) in command name become directory separators

Symlink creation:
- Target: relative path from symlink location to workflow file
- Use `ln -s` with relative path (e.g., `../../../../docs/Workflows/...`)

Example for `/code:test:optimize` pointing to `docs/Workflows/Code/Tests/OptimizeTest.md`:
```bash
mkdir -p .claude/commands/code/test
ln -s ../../../../docs/Workflows/Code/Tests/OptimizeTest.md .claude/commands/code/test/optimize.md
```

The workflow file itself contains all command frontmatter - no separate command file needed.

## AiDocMetaDoc Requirements

When a command workflow has an AiDocMetaDoc, the meta file SHOULD include [command workflow patterns](CommandWorkflow.md) in its "MUST read before editing" section. This ensures command-specific patterns are available when editing the workflow.
