# ObservedExecutionPatterns.meta.md

Specification for creating and editing [Observed execution patterns block](ObservedExecutionPatterns.md). Defines purpose, usage patterns, and constraints.

## ObservedExecutionPatterns.md goals and principles

- Defines the reusable structure and writing standards for Observed Execution Patterns sections in WorkflowDocs; each instance remains embedded in its owning workflow rather than being collected in this specification
- Preserves decision-relevant experience from actual workflow executions so future agents can exercise judgment with knowledge of how the workflow has gone in practice
- Includes recurring behavior, effective adaptations and failure patterns when they would improve future decisions; cases where an agent formally followed the workflow but produced a weak result remain especially valuable
- Restricts content to evidence from actual workflow use. Hypothetical patterns, generic good practice and restatements of procedure would create the noise this block is meant to reduce
- Explains how to write the block, while WorkflowDoc owns its optional inclusion and placement; new workflows without observed evidence do not need to load this specification
- Remains a compact format specification rather than becoming a catalogue of execution patterns or a substitute for the owning workflow's steps and Key Principles

## AiDocFormat

[AiDocBlockFormatDoc format](../../Formats/BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing ObservedExecutionPatterns.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Keeps the block minimal and evidence-driven rather than expanding it into a general risk or review checklist
- [Block concept](../../Formats/BlockFormatDoc/BlockConcept.md) - Preserves the distinction between this reusable specification, its embedded instances and the document format that composes it

## MAY read for additional context before editing ObservedExecutionPatterns.md

- [WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md) - Read when checking the block's template integration, conditional loading or boundary with Workflow steps and Key Principles
- [Documentation debugging workflow](../../workflows/debug/do.md) - Read when refining how actual session observations become evidence for an execution-pattern entry
- [AiDoc creation workflow](../../workflows/build/do.md) - Read when revising the draft-preservation example or checking that it accurately represents the workflow's observed execution experience

## ObservedExecutionPatterns.md typical use context

### 💡 Distinct usage patterns for ObservedExecutionPatterns.md

#### Referenced conditionally by the WorkflowDoc format

An agent adds or revises an Observed Execution Patterns section after actual workflow use -> the WorkflowDoc template note references this block specification -> the agent loads it to shape the section

#### Direct reference for documenting observed execution experience

`Document this recurring execution pattern following ai/zd-plugins/ai-doc/Blocks/ObservedExecutionPatterns/ObservedExecutionPatterns.md.`

### Role ObservedExecutionPatterns.md serves during use

- Source of truth for the structure and writing standards of Observed Execution Patterns sections
- Editorial guide for turning session evidence into concise, durable, decision-relevant workflow experience
- Boundary anchor that keeps actual execution-pattern instances in their owning workflows and speculative patterns out of the block
