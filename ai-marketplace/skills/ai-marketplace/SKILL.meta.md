# SKILL.meta.md

Specification for creating and editing the [ai-marketplace entry skill](SKILL.md). Defines purpose, usage patterns, and constraints.

## SKILL.md goals and principles

- Provides a valid, discoverable entry point for marketplace development, local compilation, repository configuration and source collaboration.
- Classifies each request and routes it to focused guidance instead of carrying procedures in the hub.
- Routes planning and implementation to the existing codebase guidance and local compilation through the shared builder.
- Makes source synchronization discoverable for both developers and domain experts without turning the hub into a general Git skill.
- Keeps host-specific build and Markdown rules in their owning guidance so the entry remains stable as distributions evolve.

## AiDocFormat

- [SKILL format](AI_DOC_PLUGIN/Formats/SkillDoc/SKILL.format.md) - Primary skill metadata and instruction contract.
- [HubSkill format](AI_DOC_PLUGIN/Formats/SkillDoc/Types/HubSkill.format.md) - Command and intent dispatch structure.

## MUST read before editing SKILL.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps this entry limited to the established build, compilation, configuration and synchronization routes.
- [Marketplace planning guidance](../../codebase/on-plan.md) - Defines the organization and ownership model this skill exposes.
- [Marketplace build guidance](../../codebase/on-build.md) - Defines implementation, documentation, and verification rules this skill routes to.

## MAY read for additional context before editing SKILL.md

- [Markdown authoring syntax](../../docs/AuthoringSyntax.md) - Read when changing frontmatter, invocation placeholders or document references.
- [Marketplace local compilation](workflows/compile/do.md) - Read when changing the Compile route or its description.
- [Marketplace repository configuration](workflows/sys/configure/do.md) - Read when changing the Configure route or its description.
- [Marketplace source synchronization](workflows/sync/do.md) - Read when changing the Sync route or its description.

## SKILL.md typical use context

### 💡 Distinct usage patterns for SKILL.md

#### Selected for marketplace development, compilation or configuration

User asks to develop a marketplace, compile its current working tree or configure its delivery -> the agent selects this skill -> SKILL.md routes to the relevant guidance or workflow.

#### Selected for source synchronization

Developer or domain expert asks to inspect, integrate, save or share marketplace source changes -> the agent selects Sync directly or through source-repository instructions -> SKILL.md loads the synchronization workflow.

### Role SKILL.md serves during use

- Discovery surface for marketplace developers and source maintainers.
- Intent router to development guidance, local compilation, repository configuration and source synchronization.
