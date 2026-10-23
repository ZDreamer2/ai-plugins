# AiDocFormatDoc format Specification

## What is document in AiDocFormatDoc format

An AiDocFormatDoc defines an AiDocFormat (see [AiDoc terminology](../../Theory/AiDocTerminology.md) for definitions).

It defines:
- What documents in that format are (definition and purpose)
- How to structure them (required sections, template)
- How to write them (content standards, rules, examples)

## MUST read before planning AiDocFormatDoc document

- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its directive language, formatting, and conciseness rules to the format specification
- [StartSimple methodology](../../Theory/StartSimple.md) - Start minimal and expand only when evidence shows gaps

## SHOULD read for additional context before planning AiDocFormatDoc document

- [Creating a new AiDocFormat](OnNewFormatDoc.md) - Read when defining a format from scratch to establish its template before expanding the specification
- [Document template block](../../Blocks/DocTemplate/DocTemplate.md) - Read when working on the template section to structure placeholders, modifiers, and Template Notes
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Read when working on the Validation Rules section to select critical checks and express requirement levels
- [Reading context sections](../../Blocks/ReadingContext/ReadingContext.md) - Read when working on MUST read, MAY read, or similar sections to align descriptions with their reading purpose

## AiDocFormatDoc template

```markdown
# [AiDocFormat] Format Specification

## What is document in [AiDocFormat] format

[Format definition]

## MUST read before planning [AiDocFormat] document (optional)

- [Subject or role](path/to/document.md) - [why and how to use when creating documents in this format] (one or more)

## MAY read for additional context before planning [AiDocFormat] document (optional)

- [Subject or role](path/to/document.md) - [when is this relevant for creating documents in this format] (one or more)

## [AiDocFormat] Context (optional)

[Format context]

## [AiDocFormat] template

[DocTemplate.md: [AiDocFormat] template structure]

## [AiDocFormat] example (optional)

[Format example]

## Validation Rules

[ValidationRules.md: [AiDocFormat] validation rules]
```

## Template Notes

### [Format definition]

Define what a document in this format is - its purpose and what it contains.

### "MUST read before planning [AiDocFormat] document" section

- Include when additional documents beyond foundational docs are required
- Descriptions answer "why and how to use" - actionable, not just what document contains
- See this document's MUST read section for examples

### "MAY read for additional context before planning [AiDocFormat] document" section

- Include when format benefits from optional contextual references
- Descriptions answer "when is this relevant" - enable reader to decide if needed for current task
- For block document references, use pattern: "Read when working on [SectionName] section"
- See this document's MAY read section for examples

### "[AiDocFormat] format parameters" section

Optional section for formats designed for parameterized reuse across contexts.

### [Format context]

- Optional section for theoretical foundation, domain concepts, or background information
- Include when "What is document" section becomes too long (>3 paragraphs) OR when additional concepts must be established before presenting template
- Keep "What is document" section concise; overflow theoretical content goes here

### "[AiDocFormat] template" section

Structure for writing individual documents in this format.

### [Format example]

- One complete document following that structure
- Include when it conveys what the template and notes cannot
- A single example anchors length, shape and vocabulary; omit it when documents in the format vary widely

### "Validation Rules" section

Non-trivial constraints that counter natural behavior, not template structure repetition.

## AiDocFormatDoc example

This document ([AiDocFormatDoc format specification](AiDocFormatDoc.format.md)) exemplifies the standards it teaches. Use it as a reference when creating new format specifications.

## Validation Rules

- MUST follow template structure from template section
- MUST comply with [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- MUST focus strictly on format definition (WHAT documents are, HOW to write them)
- MUST NOT include workflow/usage guidance (WHEN to use format, HOW to gather content)
- MUST apply [StartSimple methodology](../../Theory/StartSimple.md) - start minimal, expand based on evidence
- MUST include template and Validation Rules sections
