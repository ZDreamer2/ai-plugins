# do.meta.md

Specification for editing [AiDoc creation workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables creation and improvement grounded in the target's authoring context and format
- MUST ensure the target's AiDocMetaDoc is loaded and understood before modification when present
- Working without a meta is the user's choice, not a suitability judgment made by this workflow
- Primary workflow for all AiDoc creation and editing tasks
- MUST produce AiDocs that comply with their specified format requirements

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Keep terminology consistent with the definitions available during workflow use
- [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md) - Use its structure and purpose to preserve how the workflow consumes AiDocMetaDocs
- [AiDocMetaDoc creation workflow](../meta/do.md) - Check how AiDocMetaDocs are created to preserve the expected workflow inputs

## MAY read for additional context before editing do.md

- [Reference path rules](../../Theory/References/ReferencePathManagement.md) - When editing how the workflow handles path references in meta files
- [HubDoc meta-document guidance](../../Formats/MetaDoc/HubDocMeta.md) - Read when editing support for hub-document specifications
- [ChildDoc meta-document guidance](../../Formats/MetaDoc/ChildDocMeta.md) - Read when editing support for child-document specifications
- [CodeDoc format](../../Formats/CodeDoc/CodeDoc.format.md) - Read when checking how the workflow applies specialized format requirements

## do.md typical use context

### 💡 Distinct usage patterns for do.md

- Create `docs/Code/Core/Feature/NewFeature.md` following the [AiDoc creation workflow](do.md)
  - Direct reference for creating new AiDoc from scratch
- Improve `docs/Existing/Document.md` following the [AiDoc creation workflow](do.md) with these considerations:
  - Direct reference for improving existing AiDoc
  - Other than this line should contain some considerations, what and why we want to improve
- Improve the [AiDocMetaDoc creation workflow](../meta/do.md) following the [AiDoc creation workflow](do.md)
  - Improve workflow document, using special WorkflowDoc.md format for it

### Role do.md serves during use

- Standard workflow reading the target's meta when present, its format and required sources before AiDoc changes
- Quality assurance mechanism through format compliance verification
- Bridge between authoring context, format requirements and practical AiDoc content
