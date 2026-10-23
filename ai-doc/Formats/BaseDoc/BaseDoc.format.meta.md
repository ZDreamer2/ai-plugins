# BaseDoc.format.meta.md

Specification for editing [BaseDoc format](BaseDoc.format.md). Defines purpose, usage patterns, and constraints.

## BaseDoc.format.md goals and principles

- Defines default AiDocFormat used when no specific format is specified
- MUST be light specification that references actual guidance in [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- MUST NOT duplicate actual guidance (that belongs in AiDocBaseFormat.md)

## AiDocFormat

[AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md)

## MUST read before editing BaseDoc.format.md

- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Extract comprehensive theory and standards for BaseDoc format
- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its iterative methodology
- [AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md) - MUST comply with its structure and standards
- [Reading context sections](../../Blocks/ReadingContext/ReadingContext.md) - Apply when writing MUST read section
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Apply when writing Validation Rules section

## MAY read for additional context before editing BaseDoc.format.md

- [WorkflowDoc format](../WorkflowDoc/WorkflowDoc.format.md) - Read when comparing the default format with a format for sequential procedures
- [CodeDoc format](../CodeDoc/CodeDoc.format.md) - Read when comparing the default format with a format for code guidance
- [AiDocMetaDoc format](../MetaDoc/AiDocMetaDoc.format.md) - Read when checking how meta documents declare their target document's format

## BaseDoc.format.md typical use context

### 💡 Distinct usage patterns for BaseDoc.format.md

##### Referenced in AiDocMetaDocs to declare format

Used in AiDocFormat section of AiDocMetaDocs for documents using default BaseDoc format.

### Role BaseDoc.format.md serves during use

- Default format specification when no specialized format applies
- Bridge to foundation guide in AiDocBaseFormat.md
