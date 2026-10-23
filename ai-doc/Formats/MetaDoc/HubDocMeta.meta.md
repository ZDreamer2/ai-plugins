# HubDocMeta.meta.md

Specification for editing [HubDoc meta guidance](HubDocMeta.md). Defines purpose, usage patterns, and constraints.

## HubDocMeta.md goals and principles

- Extends [AiDocMetaDoc format](AiDocMetaDoc.format.md) for how to create HubDoc AiDocMetaDocs
- MUST NOT duplicate general AiDocMetaDoc writing guidance from [AiDocMetaDoc format](AiDocMetaDoc.format.md)
- Shows only AiDocMetaDoc modifications needed for HubDoc documents

## AiDocFormat

[BaseDoc format](../BaseDoc/BaseDoc.format.md)

## 💡 Distinct usage patterns for HubDocMeta.md

- `Create DocMeta.md for HubDoc doc MainFile.md`
  - Creating AiDocMetaDoc for a document that serves as primary entry point with specialized ChildDocs


## Role HubDocMeta.md serves during use

- Shows required AiDocMetaDoc modifications for HubDocs when AiDocMetaDoc.format.md identifies need
- Key principles for HubDocs (self-sufficiency, routing, boundaries)
- Examples of proper boundary management with extending documents
- Guidance on documenting conditional loading of extending documents

## MUST read before editing HubDocMeta.md

- [AiDocMetaDoc format editing context](AiDocMetaDoc.format.meta.md) - Preserve the parent format’s scope when defining hub-specific guidance
- [ChildDoc meta guidance](ChildDocMeta.md) - Understand child loading and specialization when defining hub routing and boundaries