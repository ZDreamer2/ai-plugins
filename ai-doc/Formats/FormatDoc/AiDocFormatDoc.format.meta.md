# AiDocFormatDoc.format.meta.md

Specification for editing [AiDocFormatDoc format specification](AiDocFormatDoc.format.md). Defines purpose, usage patterns, and constraints.

## Key Terms

- AiDocFormatDoc - a specification document that defines a document format. It establishes WHAT documents in that format are and HOW to write them, including structure, required sections, content standards, and writing rules (e.g., IssueInfo.format.md, IssuePlan.format.md)
- AiDocFormat - a document format defined by an AiDocFormatDoc (e.g., IssueInfo, IssuePlan, EntitySpec)
- AiDoc - a specific document following an AiDocFormat (e.g., IssueInfo.md for issue #123, IssuePlan.md for issue #456)
- AiDocFormatDoc.format.md - this document, describes how to write AiDocFormatDoc documents

## AiDocFormatDoc.format.md goals and principles

- Guides creation of AiDocFormatDocs that define WHAT a document format is and HOW to write docs in that format
- MUST focus strictly on format definition and writing standards (WHAT and HOW), NOT on usage decisions (WHEN)
- MUST strongly emphasize StartSimple methodology - start minimal, expand based on evidence
- MUST guide effective use of doc blocks (ValidationRules, DocTemplate, etc.) in format docs
- Template defines structure - Rules MUST NOT duplicate what template already establishes
- Rules MUST NOT duplicate block specifications - reference blocks and follow their guidelines
- The example section is optional: agents copy an example's surface - length, file count, vocabulary - so a single example overfits formats whose documents vary widely, as with ChunkPlan. Include one only when it teaches what the template and notes cannot
- AiDocFormatDoc.format.md itself is an AiDocFormatDoc and MUST exemplify the standards it teaches

## AiDocFormat

[AiDocFormatDoc format specification](AiDocFormatDoc.format.md)

## MUST read before editing AiDocFormatDoc.format.md

- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Use its definitions to preserve the distinction between documents, formats, and format specifications
- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its iterative methodology to AiDocFormatDoc.format.md
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Apply its criteria for selecting critical checks and expressing requirement levels when guiding format authors
- [Document template block](../../Blocks/DocTemplate/DocTemplate.md) - Apply its placeholder, modifier, and Template Notes conventions when guiding format authors
- [Reading context sections](../../Blocks/ReadingContext/ReadingContext.md) - Apply its label and description principles when guiding required and optional reading sections

## MAY read for additional context before editing AiDocFormatDoc.format.md

- [CodeDoc format](../CodeDoc/CodeDoc.format.md) - Read when checking how format guidance applies to code documentation
- [WorkflowDoc format](../WorkflowDoc/WorkflowDoc.format.md) - Read when checking how format guidance applies to procedural documentation

## AiDocFormatDoc.format.md typical use context

### 💡 Distinct usage patterns for AiDocFormatDoc.format.md

#### Creating new document format specification

```
Create `docs/Code/Domain/EntitySpec.format.md` based on [AiDocFormatDoc format specification](AiDocFormatDoc.format.md) to define entity specification documents
```

### Role AiDocFormatDoc.format.md serves during use

- Primary guide for creating consistent, minimal AiDocFormatDocs
- Establishes critical WHAT/HOW vs WHEN boundary for format documentation
- Ensures format docs apply StartSimple methodology from inception
- Provides standards for incorporating doc blocks into format specifications
