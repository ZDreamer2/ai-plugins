# HowToUse.meta.md

Specification for editing [AiDoc documentation guide](HowToUse.md). Defines purpose, usage patterns, and constraints.

## HowToUse.md goals and principles

- Primary human entry point to AiDoc documentation framework
- MUST be self-sufficient for quick-start guidance without requiring deep documentation reading
- Directs humans on supported agent hosts to appropriate workflows and rendered skill commands based on their current documentation task
- Maintains conversational, accessible tone suitable for human readers

## HowToUse.md structure conventions

The guide has two types of content:

- Core process sections (workflow descriptions, "When to use", "How it works") - these document the actual documentation workflow steps
- "Recipe" subsections - optional tips and techniques that developers MAY find useful. Recipes are recommendations, not prescribed steps. They suggest ways to handle common situations but the developer decides their own approach. Use `### Recipe: {title}` heading format.

## AiDocFormat

[Human-facing documentation format](Formats/HumanDoc/HumanDoc.format.md)

## MUST read before editing HowToUse.md

- [AiDoc terminology](Theory/AiDocTerminology.md) - Use its definitions consistently when explaining the documentation layers
- [AiDocMetaDoc creation workflow](workflows/meta/do.md) - Understand the AiDocMetaDoc creation workflow that HowToUse.md explains to humans
- [AiDoc creation workflow](workflows/build/do.md) - Understand the AiDoc creation/improvement workflow that HowToUse.md explains to humans

## MAY read for additional context before editing HowToUse.md

- [Documentation refinement workflow](workflows/refine/do.md) - Read when explaining refinement of user edits, its inputs, clarification points, and outputs
- [AiDoc compaction workflow](workflows/compact/do.md) - Read when explaining whole-document reading-cost improvements and satellite extraction
- [AiDoc stress-test workflow](workflows/stress-test/do.md) - Read when explaining review of uncommitted changes and how it differs from refinement
- [AiDocMetaDoc format](Formats/MetaDoc/AiDocMetaDoc.format.md) - When explaining AiDocMetaDoc creation in more detail
- [HubDoc meta-document guidance](Formats/MetaDoc/HubDocMeta.md) - When explaining specialized document patterns (HubDoc/ChildDoc)
- [ChildDoc meta-document guidance](Formats/MetaDoc/ChildDocMeta.md) - When explaining specialized document patterns (HubDoc/ChildDoc)

## HowToUse.md typical use context

### 💡 Distinct usage patterns for HowToUse.md

#### Direct reference by humans seeking guidance

Human developer opens [the AiDoc documentation guide](HowToUse.md) to understand how to create and manage AiDoc documentation and find the right workflow for their current documentation task.

### Role HowToUse.md serves during use

- Quick-start guide for humans unfamiliar with AiDoc documentation framework
- Multi-host router to the appropriate rendered skill invocation based on the current documentation task
- Overview of the documentation process from AiDocMetaDoc creation to AiDoc development
