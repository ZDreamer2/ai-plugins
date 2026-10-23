# DocTemplate.meta.md

Specification for editing [document template block](DocTemplate.md). Internal plugin document, used only by AiDocFormatDoc docs.

## DocTemplate.md goals and principles

- Defines how to write template blocks that provide reusable document structure patterns for AI agents
- Consumed by AI agents creating AiDocs for other AI agents

## AiDocFormat

[AiDocBlockFormatDoc format](../../Formats/BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing DocTemplate.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its iterative methodology
- [Block concept](../../Formats/BlockFormatDoc/BlockConcept.md) - Understand block nature for specification context

## MAY read for additional context before editing DocTemplate.md

- [Validation rules block](../ValidationRules/ValidationRules.md) - Read when checking how templates fit into a block specification

## DocTemplate.md typical use context

### 💡 Distinct usage patterns for DocTemplate.md

#### Referenced when creating block specification documents

Create `ChecklistBlock.md` following [AiDocFormatDoc format](../../Formats/FormatDoc/AiDocFormatDoc.format.md) with template section per [document template block](DocTemplate.md)

#### Referenced when standardizing template presentation in existing docs

Update [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md) to improve template formatting according to [document template block](DocTemplate.md)

### Role DocTemplate.md serves during use

- Ensures consistent template presentation across all AiDocs
- Provides standards for creating reusable document structure patterns
- Guides when and how to use markdown code blocks for templates
- Defines how to mark optional sections and placeholders in templates using `(optional)` marker
- Provides pattern for explaining template usage and sections via Template Notes
