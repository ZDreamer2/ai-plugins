# OnNewFormatDoc.meta.md

Specification for editing [New format creation guidance](OnNewFormatDoc.md). Defines purpose, usage patterns, and constraints.

## OnNewFormatDoc.md goals and principles

- Supplementary guidance loaded ONLY when creating a brand-new AiDocFormat (not when editing an existing AiDocFormatDoc)
- Captures decisions and considerations unique to bootstrapping a format from scratch — naming, scope, format-vs-block boundary, choosing what to defer
- MUST complement AiDocFormatDoc.format.md, NEVER duplicate its template, sections, or validation rules
- MUST strongly reinforce StartSimple methodology — new formats are the primary site where premature complexity creeps in
- MUST stay short — overflow guidance discourages the from-scratch reader who needs it most

## AiDocFormat

[BaseDoc format](../BaseDoc/BaseDoc.format.md)

## MUST read before editing OnNewFormatDoc.md

- [AiDocFormatDoc format](AiDocFormatDoc.format.md) - Parent format spec; OnNewFormatDoc.md MUST extend it without duplicating its content
- [StartSimple methodology](../../Theory/StartSimple.md) - Core methodology this doc reinforces; quote/apply rather than restate
- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Use its definitions of AiDoc, AiDocFormat, and AiDocFormatDoc consistently throughout

## MAY read for additional context before editing OnNewFormatDoc.md

- [CodeDoc format](../CodeDoc/CodeDoc.format.md) - Read when verifying advice still applies to a concrete existing AiDocFormatDoc
- [WorkflowDoc format](../WorkflowDoc/WorkflowDoc.format.md) - Read when verifying advice still applies to a concrete existing AiDocFormatDoc
- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Read when reviewing formatting/style choices in OnNewFormatDoc.md itself

## OnNewFormatDoc.md typical use context

### 💡 Distinct usage patterns for OnNewFormatDoc.md

#### Loaded indirectly via AiDocFormatDoc.format.md when creating a new AiDocFormat

User asks to create a new AiDocFormat -> AiDocFormatDoc.format.md is loaded as the format spec -> AiDocFormatDoc.format.md's reading-context section directs the reader to OnNewFormatDoc.md for from-scratch guidance

### Role OnNewFormatDoc.md serves during use

- Adds creation-time considerations on top of the structural rules in AiDocFormatDoc.format.md
- Acts as a guardrail against over-specifying a format before real usage proves the need
- Not consulted when editing an already-established AiDocFormatDoc — its scope is strictly the first version
