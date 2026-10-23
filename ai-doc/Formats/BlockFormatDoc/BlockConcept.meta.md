# BlockConcept.meta.md

Specification for editing [Block concept](BlockConcept.md). Defines purpose, usage patterns, and constraints.

## BlockConcept.md goals and principles

- Explains foundational concept of blocks as reusable content components within AiDocs
- Provides essential context for creating block specification documents
- Distinguishes blocks from complete documents (component vs standalone)
- MUST focus on WHAT blocks are, not WHEN/WHERE to use specific blocks

## AiDocFormat

[BaseDoc format](../BaseDoc/BaseDoc.format.md)

## MUST read before editing BlockConcept.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its iterative methodology
- [AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md) - Compare whole-document format structure with reusable block specifications
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Extract block instance example

## MAY read for additional context before editing BlockConcept.md

- [Document template block](../../Blocks/DocTemplate/DocTemplate.md) - Read when comparing reusable block structures beyond validation rules

## BlockConcept.md typical use context

### 💡 Distinct usage patterns for BlockConcept.md

#### Referenced from block spec meta files

```markdown
Create `path/to/SummaryBlock.md` following [AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md)

Meta file creation follows the [AiDocMetaDoc creation workflow](../../workflows/meta/do.md) which references [Block concept](BlockConcept.md)
```

This is the primary usage - BlockConcept.md gets loaded when creating or editing block specification documents because block spec meta files reference it in MUST read section.

#### Direct reference when needing block concept understanding

Read [Block concept](BlockConcept.md) to understand difference between blocks and documents.

### Role BlockConcept.md serves during use

- Foundational reference explaining block nature for block spec creators
- Clarifies terminology hierarchy used throughout block documentation
- Distinguishes blocks from documents to prevent conceptual confusion
- Explains composability principle that justifies block existence
