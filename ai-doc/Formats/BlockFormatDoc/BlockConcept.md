# Block Concept

## What is a Block

A block is a reusable content component that appears as a section within multiple AiDocs.

Blocks define:
- Structure pattern for that component type
- Writing standards for content within that pattern
- Examples demonstrating the pattern in practice

Blocks do NOT define:
- When to use the block
- Where to place the block in documents
- Workflow for gathering block content

## Blocks vs Documents

### Block
- Reusable component appearing within documents
- Defines a section type that appears in multiple documents
- Instances exist as sections within other documents
- Example: ValidationRules block appears in many format specs

### Document
- Complete standalone specification
- Defines structure for entire document type
- Instances exist as separate files
- Example: IssueInfo.format.md exists as its own file

## Terminology Hierarchy

### Block Specifications

**AiDocBlockFormatSpec** - Specification document that defines a block format
- File: [ValidationRules.md](../../Blocks/ValidationRules/ValidationRules.md)
- Defines: How to write ValidationRules sections

**AiDocBlockFormat** - Block format defined by the spec
- Format: ValidationRules Block
- Applied: In multiple documents as Rules/Validation Rules sections

**AiDocBlock** - Specific instance following the format
- Instance: [Validation Rules section in the BaseDoc format](../BaseDoc/BaseDoc.format.md#validation-rules)
- Instance: [Validation Rules section in the AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md#validation-rules)
- Instance: [Validation Rules section in the block specification itself](../../Blocks/ValidationRules/ValidationRules.md#validation-rules)

## Composability Principle

Blocks exist to avoid duplication and ensure consistency across AiDoc system.

Same block definition applied across many document types:

```
ValidationRules.md (block specification)
  ├─ Used in AiDocFormatDoc.format.md (as Validation Rules section)
  ├─ Used in IssueInfo.format.md (as Validation Rules section)
  └─ Used in EntitySpec.format.md (as Validation Rules section)
```

Without blocks: Each document would define its own rules format, creating inconsistency and maintenance burden.

With blocks: Single definition maintains consistency across all uses.

## Block Instance Location

### Block Instances
- Appear as sections WITHIN other documents
- You do NOT create separate files per instance
- Example: You write "Rules section" in the [AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md) following the [Validation Rules block specification](../../Blocks/ValidationRules/ValidationRules.md)

### Document Instances
- Exist as separate standalone files
- You DO create separate files per instance
- Example: You create IssueInfo.md for issue #123 following IssueInfo.format.md specification

This distinction is fundamental: blocks are building blocks composed into documents, not documents themselves.
