# ChildDocMeta.meta.md

Specification for editing [ChildDoc meta guidance](ChildDocMeta.md). Internal plugin document, loaded only by ai-doc skills during AiDocMetaDoc creation.

## ChildDocMeta.md goals and principles

- Extends [AiDocMetaDoc format](AiDocMetaDoc.format.md) for AiDocMetaDocs of ChildDoc documents
- MUST NOT duplicate general AiDocMetaDoc writing guidance from [AiDocMetaDoc format](AiDocMetaDoc.format.md)
- Shows only template modifications needed for ChildDoc documents
- Focuses exclusively on unique requirements: parent references, non-duplication, indirect loading patterns

## AiDocFormat

[BaseDoc format](../BaseDoc/BaseDoc.format.md)

## 💡 Distinct usage patterns for ChildDocMeta.md

- `Create meta doc for EntityLink.md which is ChildDoc for Creation.md`
  - Creating AiDocMetaDoc for a document that extends a HubDoc for specialized scenarios


## Role ChildDocMeta.md serves during use

- Shows required AiDocMetaDoc modifications for ChildDocs when AiDocMetaDoc.format.md identifies need
- Anti-patterns to avoid (duplication, independence, scope creep)
- Examples of proper parent-extension boundary management
- Guidance on documenting indirect loading patterns
- Key principles specific to extending documents

## MUST read before editing ChildDocMeta.md

- [AiDocMetaDoc format editing context](AiDocMetaDoc.format.meta.md) - Preserve the parent format’s scope when defining child-specific guidance
- [HubDoc meta guidance](HubDocMeta.md) - Understand the parent’s routing role when describing the child’s loading and boundaries
