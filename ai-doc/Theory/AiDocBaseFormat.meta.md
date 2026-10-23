# AiDocBaseFormat.meta.md

Specification for editing [AiDoc writing principles](AiDocBaseFormat.md). Defines purpose, usage patterns, and constraints.

## AiDocBaseFormat.md goals and principles

- Foundational guidance for writing AiDocs that effectively guide AI Agent during practical tasks
- MUST follow StartSimple methodology - start minimal, expand only based on proven needs from actual usage
- MUST be optimized for AI consumption, not human reading (sequential processing, perfect recall, no visual scanning)

## Critical editing guidance

### Document Scope

This document teaches writing and formatting principles applicable within any document structure. Document structure (section organization, templates) is the domain of AiDocFormatDoc files, not this document.

### Foundational Context

Core Philosophy sections establish the mental model that makes all subsequent principles coherent. Each AI conversation starts fresh - foundational sections provide essential context for every editing session.

## Tone and voice

How You Process Documentation and Core Philosophy sections:
- Direct address to AI model using "you" - establishes self-awareness about AI processing characteristics
- Personal and immediate tone helps internalize facts about how AI works
- Example: "You read sequentially", "You maintain perfect recall", "You excel at investigation"

Writing and Formatting Principles sections:
- Imperative instructions for actionable guidance
- Clear, direct commands about what to do
- Example: "Reserve capitals for the RFC 2119 terms", "Place critical information early"

Avoid throughout:
- Meta self-description: "This document will teach you..."
- Abstract third-person theory that requires translation to practice

## Section-specific editing guidance

### Purpose section

Single sentence per StartSimple - expand only on proven confusion. Focus on practical optimization goal: enabling effective task execution during AI agent work.

### How You Process Documentation section

Foundational context establishing AI self-awareness about processing patterns. Understanding YOUR processing model (sequential, perfect recall, attention weighting) enables writing AiDocs that work WITH these characteristics. Provides the "why" that makes formatting and structure choices practical, not arbitrary.

### Core Philosophy section

Unified principle integrating StartSimple and GuideVsGiveFreedom. Essence: Minimal documentation is correct. Trust AI capabilities. Expand based on evidence from actual usage, not anticipation of theoretical needs.

Key elements to convey:
- Permission (minimal is correct, not incomplete)
- Trust (AI excels at investigation and pattern recognition)
- Evidence-based expansion (respond to proven gaps, not theoretical ones)
- Warning signs (premature complexity, over-prescription, instructions for scenarios that haven't occurred)
- When to add detail (proven patterns, coordination where order matters, safety boundaries)

Self-contained and actionable.

## AiDocFormat

[Base document format](../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing AiDocBaseFormat.md

## MAY read for additional context before editing AiDocBaseFormat.md

- [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md) - Read when checking how writing principles apply to editing-context documentation
- [Validation rules block](../Blocks/ValidationRules/ValidationRules.md) - Read when refining directive-language guidance to check its application in validation rules
- [Attention and inference strategy](Research/ModelAttentionInInference.md) - Read when revising guidance on attention distribution and sequential processing
- [StartSimple methodology](StartSimple.md) - Read when refining the criteria for minimal documentation and evidence-based expansion
- [Constraint theory](GuideVsGiveFreedom.md) - Read when refining the distinction between necessary coordination and excessive prescription

## AiDocBaseFormat.md typical use context

### 💡 Distinct usage patterns for AiDocBaseFormat.md

#### Automatically loaded during AiDoc workflows

Loaded by the [ai-doc skill](../skills/ai-doc/SKILL.md) before it dispatches to a handler, providing foundational context for all AiDoc creation and editing tasks.

### Role AiDocBaseFormat.md serves during use

- Practical guidance enabling effective AiDoc writing by understanding AI consumption patterns
- Comprehensive standards for formatting, emphasis, structure, and token efficiency that demonstrably improve AI task execution
- Source of truth for proven documentation patterns (RFC 2119 terms, consequence-based emphasis, working WITH sequential processing)
