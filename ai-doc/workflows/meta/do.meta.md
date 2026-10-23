# do.meta.md

Specification for creating and editing [AiDocMetaDoc creation workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables creation of editing context that remains useful as the target evolves, whether or not the target exists yet.
- Establishes the target's purpose and use before its format. In the motivating session, metas generated from one template repeated document purposes without explaining what future edits needed to preserve.
- Owns the authoring process; the AiDocMetaDoc format owns the content standard. Keeping that distinction lets creation and review use the same definition of a useful meta.
- Remains independent of harness-specific orchestration tools and reuses sufficient current context. Its value comes from interpreting the particular target's intent and boundaries, rather than accumulating required reading or completing a template.

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Defines the creation and editing roles this workflow coordinates.
- [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md) - Owns the content boundary and validation requirements shared with review.
- [StartSimple methodology](../../Theory/StartSimple.md) - Explains why the procedure stays proportional to the authoring task.

## MAY read for additional context before editing do.md

- [Reference path rules](../../Theory/References/ReferencePathManagement.md) - Defines resolution conventions relevant to reference-handling changes.
- [AiDoc creation workflow](../build/do.md) - Shows how the resulting meta is consumed during target authorship.
- [HubDoc guidance](../../Formats/MetaDoc/HubDocMeta.md) and [ChildDoc guidance](../../Formats/MetaDoc/ChildDocMeta.md) - Defines specialized context relationships relevant to selection changes.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Dispatched by the ai-doc skill

User requests creation or improvement of a meta -> ai-doc selects the meta workflow -> this document guides production of the meta. The target may be absent, empty or already implemented.

### Role do.md serves during use

- Orchestrates context gathering and authorship of the meta.
- Checks the value of the additional context and leaves document-level choices to the target author.
