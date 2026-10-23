# AiDocTerminology.meta.md

Specification for editing [AiDoc terminology](AiDocTerminology.md). Defines purpose, usage patterns, and constraints.

## AiDocTerminology.md goals and principles

- Establishes foundational terminology for the AiDoc system used across all documentation workflows
- Defines core elements: AiDoc, AiDocFormat, AiDocFormatDoc, AiDocMetaDoc and their relationships
- MUST provide minimal essential definitions without over-specification per StartSimple methodology
- Serves as internal context foundation for workflows, not as directly-referenced instruction document

## AiDocFormat

[BaseDoc format](../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing AiDocTerminology.md

- [StartSimple methodology](StartSimple.md) - Apply its iterative minimal approach to documentation development
- [AiDoc creation workflow](../workflows/build/do.md) - Understand how AiDocTerminology.md will be used as base context
- [AiDocMetaDoc creation workflow](../workflows/meta/do.md) - Understand how AiDocTerminology.md will be used as base context

## MAY read for additional context before editing AiDocTerminology.md

- [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md) - Read when checking how the meta-document definition translates into editing-context requirements
- Other theory documents in `./` - Read when checking pattern consistency across theory documentation

## AiDocTerminology.md typical use context

### 💡 Distinct usage patterns for AiDocTerminology.md

#### Loaded automatically by workflows for base terminology

Workflows like the [AiDoc creation workflow](../workflows/build/do.md) and [AiDocMetaDoc creation workflow](../workflows/meta/do.md) read this document internally to establish shared vocabulary before executing their steps. Not referenced in user prompts.

### Role AiDocTerminology.md serves during use

- Establishes consistent terminology across all AiDoc workflows
- Provides authoritative definitions for core system elements
- Prevents terminology confusion by defining relationships between AiDoc, AiDocFormat, AiDocFormatDoc, and AiDocMetaDoc
- Serves as foundation for understanding workflow instructions
