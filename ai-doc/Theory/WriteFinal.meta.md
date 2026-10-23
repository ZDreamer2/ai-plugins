# WriteFinal.meta.md

Specification for editing [WriteFinal principles](WriteFinal.md). Defines purpose, usage patterns, and constraints.

## WriteFinal.md goals and principles

- Establishes the principle that AiDocs MUST be authored for the planned final architecture of the doc ecosystem, not its current build state
- Addresses the transitional period when the doc ecosystem is being built incrementally — some docs exist, some are planned stubs, some are about to be absorbed or deleted
- MUST convey the core mindset shift: each doc should read as if it already lives in the finished ecosystem
- MUST provide practical rules that flow from the core principle (referencing planned docs normally, not referencing transitional artifacts)
- Complements StartSimple: StartSimple governs what content to include, WriteFinal governs how to frame references and relationships given an incomplete ecosystem

## AiDocFormat

[BaseDoc format](../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing WriteFinal.md

- [StartSimple methodology](StartSimple.md) - Sibling principle: understand how StartSimple governs content scope so WriteFinal can focus on its distinct concern — reference framing, not content volume
- [AiDoc writing principles](AiDocBaseFormat.md) - Writing foundation; WriteFinal.md MUST comply with its principles

## MAY read for additional context before editing WriteFinal.md

- [Constraint theory](GuideVsGiveFreedom.md) - Related constraint theory; read when calibrating how prescriptive the practical rules should be
- [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md) - Meta docs are where WriteFinal most visibly applies (MUST read / MAY read sections reference other docs); read when writing examples

## WriteFinal.md typical use context

### 💡 Distinct usage patterns for WriteFinal.md

#### Referenced in meta docs as MUST read during ecosystem build-out phases

Meta doc author is writing references for a doc whose sibling/parent docs are not all built yet -> WriteFinal.md guides whether and how to reference planned or transitional docs

#### Direct reference when planning doc ecosystem structure

Plan the domain knowledge docs for the rm plugin; consider the [WriteFinal principles](WriteFinal.md) for how to handle references across docs at different stages of readiness

### Role WriteFinal.md serves during use

- Mindset guide: shifts authoring perspective from "what exists now" to "what the finished ecosystem looks like"
- Practical decision framework for handling references to docs in various states (planned, stub, transitional, about to be absorbed)
