# HowToUseDoc.meta.md

Specification for editing [HowToUse document guide](HowToUseDoc.md). Defines purpose, usage patterns, and constraints.

## HowToUseDoc.md goals and principles

- Captures proven patterns and principles for writing effective HowToUse documents
- Extracts structural and tonal conventions from the best existing HowToUse docs in the project
- Guides AI in creating HowToUse documents that are clear, self-sufficient, and useful for human developers
- Supplements HumanDoc.format.md with HowToUse-specific guidance

## AiDocFormat

[Human-facing documentation format](HumanDoc.format.md)

## MUST read before editing HowToUseDoc.md

- [AiDoc documentation guide](../../HowToUse.md) - Primary example of a HowToUse document; source for extracting structural patterns, tone, complete scenarios section, and "What to mention" guidance

## MAY read for additional context before editing HowToUseDoc.md

- [AiDoc guide editing specification](../../HowToUse.meta.md) - Read when describing how meta documents capture guide goals, structure conventions, and usage patterns

## HowToUseDoc.md typical use context

### 💡 Distinct usage patterns for HowToUseDoc.md

#### Loaded indirectly when building a HowToUse document

User asks to create/edit a HowToUse document -> BuildDoc workflow loads the document's .meta.md -> .meta.md references HowToUseDoc.md as MUST read -> AI loads HowToUseDoc.md for HowToUse-specific patterns

#### Direct reference when planning HowToUse document structure

`${AGENT_SKILL(ai-doc)} meta Create meta for docs/NewSystem/HowToUse.md - follow HowToUseDoc patterns`

### Role HowToUseDoc.md serves during use

- Pattern reference ensuring consistent HowToUse documents across the project
- Supplementary guide to HumanDoc format for the specific HowToUse document type
