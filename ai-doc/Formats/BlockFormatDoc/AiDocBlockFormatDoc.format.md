# AiDocBlockFormatDoc format Specification

## What is document in AiDocBlockFormatDoc format

An AiDocBlockFormatDoc defines an AiDocBlockFormat (see [AiDoc terminology](../../Theory/AiDocTerminology.md) for terminology).

It defines:
- What block specifications in that format are (definition and purpose)
- How to structure them (required sections, template)
- How to write them (content standards, rules, examples)

## MUST read before planning AiDocBlockFormatDoc document

- [Block concept](BlockConcept.md) - Understand block vs document distinction and composability principle
- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its directive language and formatting rules to the block specification
- [StartSimple methodology](../../Theory/StartSimple.md) - Start minimal and expand only when evidence shows gaps
- [Document template block](../../Blocks/DocTemplate/DocTemplate.md) - Apply when writing template section
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Apply when writing Validation Rules section
- [Reading context sections](../../Blocks/ReadingContext/ReadingContext.md) - Apply when writing MUST read section if included

## AiDocBlockFormatDoc template

```markdown
# [AiDocBlockFormat] Block Format

## [AiDocBlockFormat] template

[DocTemplate.md: [AiDocBlockFormat] template structure]

## [AiDocBlockFormat] example

[Block example]

## Validation Rules

[ValidationRules.md: [AiDocBlockFormat] validation rules]
```

## Template Notes

### "[AiDocBlockFormat] template" section

Structure for writing individual blocks in this block type.

### [Block example]

One complete block example following this block type.

### "Validation Rules" section

Critical validation points specific to this block type.

## AiDocBlockFormatDoc example

Examples of actual block types:

- [Document template block](../../Blocks/DocTemplate/DocTemplate.md) - Document template block format
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Validation rules block format

## Validation Rules

- MUST follow template structure from template section
- MUST comply with [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- MUST focus strictly on block format definition (WHAT block specifications are, HOW to write them)
- MUST NOT include workflow/usage guidance (WHEN to use block format, HOW to gather content)
- MUST apply [StartSimple methodology](../../Theory/StartSimple.md) - start minimal, expand based on evidence
- MUST include template, example, and Validation Rules sections
