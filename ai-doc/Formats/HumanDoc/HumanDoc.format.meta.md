# HumanDoc.format.meta.md

Specification for editing [HumanDoc format](HumanDoc.format.md). Defines purpose, usage patterns, and constraints.

## HumanDoc.format.md goals and principles

- Format specification for human-facing documentation that prioritizes readability over token efficiency
- MUST clearly override BaseDoc.md restrictions while maintaining structural standards
- Enables creation of engaging, accessible documentation for human readers
- Primary format for guides, tutorials, and learning materials
- MUST be concise since the core message is simple: "write naturally for humans"

## AiDocFormat

[BaseDoc format](../BaseDoc/BaseDoc.format.md)

## MUST read before editing HumanDoc.format.md

- [AiDocMetaDoc format](../MetaDoc/AiDocMetaDoc.format.md) - To understand how HumanDoc.format.md fits into the format specification system

## MAY read for additional context before editing HumanDoc.format.md

- [CodeDoc format](../CodeDoc/CodeDoc.format.md) - Read when comparing human-facing guidance with a specialized format for AI code guidance
- [Ai-doc usage guide](../../HowToUse.md) - Read when checking how human-facing format choices work in a plugin usage guide

## HumanDoc.format.md typical use context

### 💡 Distinct usage patterns for HumanDoc.format.md

- Create `docs/GettingStarted.md` meta file following the [AiDocMetaDoc creation workflow](../../workflows/meta/do.md) with consideration that `GettingStarted.md` follows [HumanDoc format](HumanDoc.format.md).
  - Establishing, that some AiDoc must follow this format
- Create `docs/GettingStarted.md` following the [AiDoc creation workflow](../../workflows/build/do.md).
  - If `GettingStarted.meta.md` states that this is human-facing documentation

### Role HumanDoc.format.md serves during use

- Provides format guidelines when creating documentation for human consumption
- Explicitly permits formatting choices that would violate BaseDoc.md rules
- Ensures human-facing docs are engaging and accessible
- Bridges the gap between strict AI documentation and human learning needs