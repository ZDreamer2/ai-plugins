# SKILL Format Specification

## What is document in SKILL format

A SKILL.md file defines an Agent Skill per the agentskills.io specification. Contains YAML frontmatter with skill metadata and a Markdown body with instructions for AI agents.

Authoritative specification: [Agent Skills specification](https://agentskills.io/specification)

## MUST read before planning SKILL document

- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its formatting and writing principles
- [StartSimple methodology](../../Theory/StartSimple.md) - Start minimal and expand only when evidence shows gaps

## MAY read for additional context before planning SKILL document

- [HubSkill format](Types/HubSkill.format.md) - Read when the request mentions "HubSkill"

## SKILL template

```markdown
---
[Frontmatter]
---

[Skill instructions]
```

## Template Notes

### [Frontmatter]

See [SKILL frontmatter reference](SkillFrontmatter.md) for field specifications, naming rules, and description writing guidance.

### [Skill instructions]

Markdown body with no required structure. Write whatever helps agents perform the task effectively.

Skills that define multi-step procedures often follow [WorkflowDoc format](../WorkflowDoc/WorkflowDoc.format.md)

Host-specific variables, command expansion, and plugin packaging belong to the target environment’s plugin build guidance. They are not part of the generic SKILL format.

## Validation Rules

- MUST include required frontmatter fields: name and description
- MUST comply with [SKILL frontmatter](SkillFrontmatter.md) field constraints
