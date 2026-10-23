# ReadingContext.meta.md

Specification for editing [reading context sections](ReadingContext.md). Defines purpose, usage patterns, and constraints.

## ReadingContext.md goals and principles

- Unify MUST read and MAY read patterns via single "description frame" concept:
  - Actionable frame ("why/how to use this") -> MUST read section
  - Relevance frame ("when is this useful") -> MAY read section
- Guide format authors to embed self-contained reading context sections directly into format templates
- Guide adding validation rules about reading context sections to format files
- Guide adding ReadingContext.md reference to meta files of FormatDocs that use reading context sections
- Result: actual doc creation requires ONLY the format file - no block docs needed

## AiDocFormat

[BaseDoc format](../../Formats/BaseDoc/BaseDoc.format.md)

Future consideration: May evolve to [block format specification](../../Formats/BlockFormatDoc/AiDocBlockFormatDoc.format.md) when block structure matures.

## MUST read before editing ReadingContext.md

- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply formatting and writing principles

## MAY read for additional context before editing ReadingContext.md

- [CodeDoc format](../../Formats/CodeDoc/CodeDoc.format.md) - Read when seeing target pattern: self-contained format with no block doc references
- [CodeDoc editing context](../../Formats/CodeDoc/CodeDoc.format.meta.md) - Read alongside CodeDoc.format.md: meta doc that references ReadingContext.md, showing the pattern in use
- [block format specification](../../Formats/BlockFormatDoc/AiDocBlockFormatDoc.format.md) - Read when considering evolution to formal block format

## ReadingContext.md typical use context

### 💡 Distinct usage patterns for ReadingContext.md

#### Loaded indirectly when editing any FormatDoc with reading context sections

User edits FormatDoc (e.g. IssueSpec.format.md, AiDocBlockFormatDoc.format.md) -> FormatDoc's meta lists ReadingContext.md -> loaded when working on MUST/MAY read sections

#### Direct reference when simplifying existing format files

Refactor `some/format.format.md` to use the [reading context sections](ReadingContext.md) pattern instead of separate MustRead/MayRead references.

### Role ReadingContext.md serves during use

- Teaches format authors HOW to write self-contained reading context sections
- Format files then contain everything needed - doc authors work from format file alone
