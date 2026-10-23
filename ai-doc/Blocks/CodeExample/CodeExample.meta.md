# CodeExample.meta.md

Specification for editing [Code example block](CodeExample.md). Defines purpose, usage patterns, and constraints.

## CodeExample.md goals and principles

- Defines the CodeExample Block format for use across AiDocs
- Consumed by AI agents creating AiDocs for other AI agents
- Provides minimal, essential guidance for creating effective code examples
- MUST follow StartSimple methodology - minimal guidance, expand based on proven gaps

## AiDocFormat

[AiDocBlockFormatDoc format](../../Formats/BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing CodeExample.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its iterative methodology
- [Block concept](../../Formats/BlockFormatDoc/BlockConcept.md) - Understand block nature for specification context
- [Validation rules block](../ValidationRules/ValidationRules.md) - Apply its format to Rules section
- [Document template block](../DocTemplate/DocTemplate.md) - Apply its format to Template section

## MAY read for additional context before editing CodeExample.md

- [Repository documentation example](../../Formats/CodeDoc/Examples/BuildRepository.md) - Read when refining guidance on dense examples with inline explanations
- Any AiDoc format specification from `../../Formats/` - Read when checking how consuming formats reference the code example block

## CodeExample.md typical use context

### 💡 Distinct usage patterns for CodeExample.md

#### Consulted directly when creating code examples in AiDocs

AI agent creating or editing AiDoc with code examples reads this for specific guidance beyond BaseDoc.md

### Role CodeExample.md serves during use

- Defines code example-specific quality standards (density, conciseness, self-sufficiency)
- Provides actionable rules for creating effective code examples
- Demonstrates proper code example format through working example
- Guides when to include "do not" examples for anti-pattern illustration
