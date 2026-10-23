# StartSimple.meta.md

Specification for editing [StartSimple methodology](StartSimple.md). Defines purpose, usage patterns, and constraints.

## StartSimple.md goals and principles

- Establishes iterative, usage-driven approach to documentation development as preferred method over comprehensive upfront planning
- Prevents premature optimization of documentation complexity before practical validation
- MUST provide concrete methodology for starting minimal and expanding based on real feedback
- Complements existing AI constraint theory with focus on documentation development process
- [AiDoc writing principles](AiDocBaseFormat.md#core-philosophy) state the principle and its warning signs and are loaded in the same sessions. StartSimple.md holds what they lack - the reasoning and how to apply it when creating and editing - and MUST NOT restate them
- Guidance MUST be actionable within a single editing session, where the available evidence is what the user and debug findings bring

## AiDocFormat

[BaseDoc format](../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing StartSimple.md

- [Constraint theory](GuideVsGiveFreedom.md) - Preserve the distinction between guiding AI execution and limiting documentation complexity
- [AiDoc writing principles](AiDocBaseFormat.md) - Check its Core Philosophy section to keep StartSimple.md from restating it

## MAY read for additional context before editing StartSimple.md

- [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md) - Read when using meta-documentation as an example of iterative refinement

## StartSimple.md typical use context

### 💡 Distinct usage patterns for StartSimple.md

#### Loaded as required reading when building format-governed docs and new metas

Format documents list it under MUST read, and the [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md) requires new AiDocMetaDocs to link it -> most build and meta sessions load it together with [AiDoc writing principles](AiDocBaseFormat.md)

#### Named in a user prompt as special direction

`Also, consider [StartSimple methodology](StartSimple.md) while planning AnalyseMr.md` - part of a bigger prompt, conveys direction during complex doc creation

### Role StartSimple.md serves during use

- Philosophical framework for making documentation complexity decisions
- Decision criteria for determining when to add detail vs when to maintain simplicity
- Methodology guide for iterative documentation development process
- Counterbalance to natural tendency toward comprehensive upfront planning