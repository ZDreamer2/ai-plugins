# do.meta.md

Specification for creating and editing the [marketplace source synchronization workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables developers and domain experts to collaborate on an authoritative marketplace source checkout without requiring routine Git expertise.
- Provides an opinionated, low-friction synchronization path while treating preservation of local and incoming work as a safety invariant.
- Remains reusable across marketplaces rather than encoding tender-specialist or other repository-specific domain rules.
- Focuses on one source checkout and complements developer workspace Git tooling rather than supporting arbitrary Git operations.
- Uses ordinary source-repository instructions as the lightweight override for commit and integration conventions instead of introducing a Sync-specific configuration system.
- Keeps source synchronization distinct from generated-distribution publication; repository instructions own additional boundaries around protected configuration and infrastructure.
- Surfaces Git decisions only when user intent is needed, especially for ambiguous content conflicts, and explains changes and outcomes in plain language.

## AiDocFormat

[WorkflowDoc format](AI_DOC_PLUGIN/Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps the workflow focused on the established collaboration loop rather than anticipated Git variations or configuration features.
- [Constraint theory](AI_DOC_PLUGIN/Theory/GuideVsGiveFreedom.md) - Helps constrain coordination and work-preservation safeguards while leaving inspection and conflict investigation flexible.
- [Marketplace planning guidance](../../../../codebase/on-plan.md) - Defines the source, plugin and generated-distribution ownership boundaries that synchronization must preserve.

## MAY read for additional context before editing do.md

- [Marketplace repository configuration](../sys/configure-central/do.md) - Read when changing the boundary between source synchronization and repository hosting, CI or generated-distribution publication.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Loaded through the ai-marketplace hub

User asks to retrieve colleagues' source changes, save and publish local edits, or recover from a rejected push -> ai-marketplace selects Sync -> loads this workflow with the current source checkout and repository instructions.

#### Referenced by marketplace source instructions

Agent maintains a specialist-owned marketplace -> source-root instructions refer to the reusable synchronization workflow -> this workflow supplies the collaboration procedure while repository instructions supply domain ownership and local conventions.

### Role do.md serves during use

- Coordinates safe routine synchronization of one authoritative marketplace source checkout.
- Preserves both contributors' work and escalates only decisions whose intended content cannot be determined safely.
- Gives source maintainers a plain-language account of changes and Git outcomes without requiring them to operate Git manually.
