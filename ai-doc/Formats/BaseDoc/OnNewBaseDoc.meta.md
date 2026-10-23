# OnNewBaseDoc.meta.md

Specification for editing [New BaseDoc guidance](OnNewBaseDoc.md). Defines purpose, usage patterns, and constraints.

## OnNewBaseDoc.md goals and principles

- Supplementary guidance loaded ONLY when creating a brand-new BaseDoc (not when editing an existing BaseDoc)
- Captures considerations unique to bootstrapping a BaseDoc from scratch — structuring free-form content, deciding scope, choosing what to defer
- MUST complement the [BaseDoc format](BaseDoc.format.md), NEVER duplicate its content or [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- MUST reinforce that drafting header structure first is the key first step for free-form documents
- MUST stay short — overflow guidance discourages the from-scratch reader who needs it most

## AiDocFormat

[BaseDoc format](BaseDoc.format.md)

## MUST read before editing OnNewBaseDoc.md

- [BaseDoc format](BaseDoc.format.md) - Parent format spec; OnNewBaseDoc.md MUST extend it without duplicating its content
- [StartSimple methodology](../../Theory/StartSimple.md) - Core methodology this doc reinforces; quote/apply rather than restate

## MAY read for additional context before editing OnNewBaseDoc.md

- [New format guidance](../FormatDoc/OnNewFormatDoc.md) - Read when checking parallel patterns with FormatDoc's from-scratch guidance
- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Read when reviewing formatting/style choices in OnNewBaseDoc.md itself

## OnNewBaseDoc.md typical use context

### 💡 Distinct usage patterns for OnNewBaseDoc.md

#### Loaded indirectly via BaseDoc.format.md when creating a new BaseDoc

User asks to create a new BaseDoc -> BaseDoc.format.md is loaded as the format spec -> BaseDoc.format.md's reading-context section directs the reader to OnNewBaseDoc.md for from-scratch guidance

### Role OnNewBaseDoc.md serves during use

- Adds creation-time considerations on top of the minimal rules in BaseDoc.format.md
- Guides the agent to draft header structure first before writing content
- Not consulted when editing an already-established BaseDoc — its scope is strictly the first version
