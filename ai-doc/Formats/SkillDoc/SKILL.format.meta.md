# SKILL.format.meta.md

Specification for editing [SKILL format](SKILL.format.md). Defines purpose, usage patterns, and constraints.

## SKILL.format.md goals and principles

- Define how to write SKILL.md files that conform to the [Agent Skills specification](https://agentskills.io/specification)
- Scope: SKILL.md file structure and content only (frontmatter + body), NOT skill directory organization (scripts/, references/, assets/)
- Host-specific variables, command expansion and plugin packaging belong to the target environment’s plugin build guidance, not this generic format
- MUST follow AiDocFormatDoc structure
- MUST apply StartSimple methodology - this is a new format domain, start minimal

## AiDocFormat

[AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md)

## MUST read before editing SKILL.format.md

- [Agent Skills specification](https://agentskills.io/specification) - Authoritative source for SKILL.md format: extract field constraints, required/optional status, and content guidelines
- [StartSimple methodology](../../Theory/StartSimple.md) - Apply minimal approach, expand only when real usage reveals gaps

## MAY read for additional context before editing SKILL.format.md

- [AiDoc creation workflow](../../workflows/build/do.md) - Read when checking how the creation workflow consumes format guidance
- [AiDocMetaDoc creation workflow](../../workflows/meta/do.md) - Read when checking how the meta workflow selects SKILL format
- [Reading context sections](../../Blocks/ReadingContext/ReadingContext.md) - Read when adding or editing "MAY read for additional context before planning SKILL document" section

## SKILL.format.md typical use context

### 💡 Distinct usage patterns for SKILL.format.md

#### Loaded during BuildDoc workflow when creating a new skill

User asks to create a skill -> BuildDoc workflow loads SKILL.format.meta.md -> extracts SKILL.format.md path -> SKILL.format.md guides SKILL.md creation

#### Direct reference when writing or improving a SKILL.md

Write a `SKILL.md` for the new code-review skill according to the [SKILL format](SKILL.format.md).

### Role SKILL.format.md serves during use

- Primary guide for writing SKILL.md files with correct frontmatter and body structure
- Ensures consistency across all project skills
