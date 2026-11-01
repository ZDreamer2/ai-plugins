# AiDocMetaDocs for Documents that Extend Others

When writing a AiDocMetaDoc for ChildDoc document, use the standard template from [AiDocMetaDoc format](AiDocMetaDoc.format.md) with the modifications below.

A ChildDoc assumes its HubDoc's context and is read alongside it. A document that stands on its own is an independent AiDoc, not a ChildDoc.

## Required Template Modifications

### Goals and Principles Section

MUST include these elements to identify the extending nature:
```markdown
- Extends `HubDoc.md` for [specific scenarios]
- MUST NOT duplicate information from `HubDoc.md`
- Focuses exclusively on [specialization area]
- Loaded when `HubDoc.md` identifies need for [specialization]
```

### MUST Read Section

Always include parent's AiDocMetaDoc:
```markdown
- [Parent editing context](path/to/HubDoc.meta.md) - Understand when the parent is used and how it loads this child document
- ALWAYS include all documents from "MUST Read Section" of [Parent editing context](path/to/HubDoc.meta.md)
```

### Typical Use Context Section

#### 💡 Typical Prompts Subsection

Explain indirect loading pattern:
```markdown
- `Appears when HubDoc.md logic directs to this specialization`
- `Not typically loaded directly from user prompts`
```

#### Role During Use Subsection

Clarify specialization role:
```markdown
- Provides detailed guidance for [specific scenario] when `HubDoc.md` identifies need
```

## Editing Checklist

When editing ChildDoc document:
1. Load HubDoc document's AiDocMetaDoc first
2. Check parent's boundaries before adding content
3. Ensure no duplication with parent document
4. Maintain strict specialization focus
5. Verify loading pattern documentation is correct