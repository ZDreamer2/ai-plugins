# README.meta.md

Specification for creating and editing [marketplace README](README.md). Defines purpose, usage patterns and constraints.

## README.md goals and principles

- Orients maintainers working with the standalone two-plugin marketplace, distinguishing GitLab publication from unconfigured GitHub delivery and consumer migration.
- Keeps executable local verification reproducible without the original checkout, shared SDK or downloaded Python dependencies.
- Owns local verification and GitLab publication operations, including the shared-runner trust boundary, credential renewal and artifact verification. Extraction provenance and unimplemented delivery stages stay distinct; licensing remains an owner decision.

## AiDocFormat

[BaseDoc format](AI_DOC_PLUGIN/Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing README.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps the entry point focused on established local operations.
- [Host rendering](ai-marketplace/docs/HostRendering.md) - Defines the output contract the local commands exercise.

## README.md typical use context

### 💡 Distinct usage patterns for README.md

#### Direct checkout entry point

`Build and test this checkout using README.md.`

### Role README.md serves during use

- Local setup and verification entry point, with extraction provenance and deployment boundaries.
