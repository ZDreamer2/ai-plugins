# ValidationRules.meta.md

Specification for editing [Validation rules block](ValidationRules.md). Defines purpose, usage patterns, and constraints.

## ValidationRules.md goals and principles

- Defines structure and formatting patterns for Rules sections in AiDocs
- Explains how to write Rules sections, not when to include them
- Source of truth for project-wide Rules section patterns
- Consumed by AI agents creating AiDocs for other AI agents
- MUST NOT be self-sufficient - relies on BaseDoc.md for foundational guidance

## AiDocFormat

[AiDocBlockFormatDoc format](../../Formats/BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing ValidationRules.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its iterative methodology
- [Block concept](../../Formats/BlockFormatDoc/BlockConcept.md) - Understand block nature for specification context

## MAY read for additional context before editing ValidationRules.md

- [CodeDoc format](../../Formats/CodeDoc/CodeDoc.format.md) - Read when checking how Rules sections fit into code documentation
- [AiDoc creation workflow](../../workflows/build/do.md) - Read when choosing IF/THEN phrasing for conditional requirements

## ValidationRules.md typical use context

### 💡 Distinct usage patterns for ValidationRules.md

#### Referenced by format documents that require Rules sections

Edit the [CodeDoc format](../../Formats/CodeDoc/CodeDoc.format.md) to reference the [Validation rules block](ValidationRules.md) for standardized Rules section guidance.

#### Direct reference when creating or improving AiDocs with Rules sections

Add a Rules section to the example target `src/Core/Domain/Entity/Docs/Entity.md` following the [Validation rules block](ValidationRules.md).

### Role ValidationRules.md serves during use

- Provides format specification for Rules sections structure
- Explains constraint documentation patterns (RFC 2119 terms, bullet format, subsections)
- Shows examples of well-formed Rules sections
- Bridges BaseDoc.md general principles with specific Rules section formatting requirements
