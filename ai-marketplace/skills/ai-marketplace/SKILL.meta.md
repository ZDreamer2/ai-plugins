# SKILL.meta.md

Specification for creating and editing the [ai-marketplace entry skill](SKILL.md). Defines purpose, usage patterns, and constraints.

## SKILL.md goals and principles

- Provides a valid, discoverable entry point for development work in an AI plugin marketplace.
- Routes planning and implementation to the existing codebase guidance instead of duplicating marketplace conventions in the skill.
- Keeps host-specific build and Markdown rules in their owning guidance so the entry remains stable as distributions evolve.

## AiDocFormat

[SKILL format](AI_DOC_PLUGIN/Formats/SkillDoc/SKILL.format.md)

## MUST read before editing SKILL.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps this entry limited to the established planning and build routes.
- [Marketplace planning guidance](../../codebase/on-plan.md) - Defines the organization and ownership model this skill exposes.
- [Marketplace build guidance](../../codebase/on-build.md) - Defines implementation, documentation, and verification rules this skill routes to.

## MAY read for additional context before editing SKILL.md

- [Markdown authoring syntax](../../docs/AuthoringSyntax.md) - Read when changing frontmatter or document references.

## SKILL.md typical use context

### 💡 Distinct usage patterns for SKILL.md

#### Selected for marketplace development

User asks to plan or implement work in an AI plugin marketplace -> the agent selects this skill -> SKILL.md loads the relevant codebase guidance.

### Role SKILL.md serves during use

- Discovery surface for AI plugin marketplace development.
- Context router to marketplace planning and build guidance.
