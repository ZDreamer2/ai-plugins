# TypicalUseContext.meta.md

Specification for editing [Typical use context block](TypicalUseContext.md). Defines purpose, usage patterns, and constraints.

## TypicalUseContext.md goals and principles

- Define block format for documenting distinct usage patterns of AiDocs
- Focus on UNIQUE patterns only, rejecting redundant variations
- Provide clear template for structuring usage pattern documentation
- Demonstrate distinction between genuinely different patterns vs superficial variations

## AiDocFormat

[AiDocBlockFormatDoc format](../../BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing TypicalUseContext.md

- [StartSimple methodology](../../../Theory/StartSimple.md) - Apply iterative methodology when planning improvements
- [Block concept](../../BlockFormatDoc/BlockConcept.md) - Understand block nature for specification context
- [Document template block](../../../Blocks/DocTemplate/DocTemplate.md) - Apply when writing template section
- [Validation rules block](../../../Blocks/ValidationRules/ValidationRules.md) - Apply when writing Validation Rules section
- [AiDocMetaDoc format](../AiDocMetaDoc.format.md) - Use its template to preserve how distinct usage patterns fit in the typical use context section

## MAY read for additional context before editing TypicalUseContext.md

- [AiDocMetaDoc format](../AiDocMetaDoc.format.md) - Read when checking integration with the surrounding typical use context section
- [AiDoc creation workflow editing context](../../../workflows/build/do.meta.md) - Read when refining examples of distinct creation and editing patterns

## TypicalUseContext.md typical use context

### 💡 Distinct usage patterns for TypicalUseContext.md

#### Loaded when creating new AiDocMetaDoc following BuildDocMeta workflow

Follow the [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) to create a meta file for `docs/Code/Entity/Entity.md`

Workflow loads TypicalUseContext.md specification when building the "Typical Use Context" section of new AiDocMetaDoc.

#### Referenced when improving existing AiDocMetaDoc usage patterns section

`Improve usage patterns section in docs/Code/Repository/Repository.meta.md to better distinguish unique patterns`

Direct reference for clarifying what constitutes distinct vs redundant usage patterns.

### Role TypicalUseContext.md serves during use

- Template for structuring usage pattern documentation in AiDocMetaDocs
- Criteria for distinguishing genuinely unique patterns from superficial variations
- Guidance on when to include explanatory text vs relying on self-explanatory prompts
