# AiDocMetaDocs for Primary Entry Point Documents

When writing a AiDocMetaDoc for a document that serves as HubDoc and routes to specialized documentation, use the standard template from [AiDocMetaDoc format](AiDocMetaDoc.format.md) with the modifications below.

## Required Template Modifications

### Goals and Principles Section

MUST include these elements to identify the primary entry point nature:
```markdown
- Primary entry point to [domain] documentation ecosystem
- MUST be self-sufficient for basic [use case]
- Directs to specialized documentation for complex scenarios
```

### MAY Read Section

Include extending documents for boundary understanding:
```markdown
- Extending documents - To understand what NOT to include in primary document
- Implementation examples showing basic vs complex patterns
```

### Typical Use Context Section

#### Role During Use Subsection

Emphasize decision-making and routing:
```markdown
- Primary guide for [basic cases]
- Decision tree for when to consult specialized documentation
- Router to appropriate extending document for [complex scenarios]
```

## Editing Checklist

When editing a primary entry point document:
1. Ensure self-sufficiency for basic cases
2. Include clear decision trees for extending documents
3. Verify no duplication with extending documents
4. Check routing logic is explicit and complete
5. Confirm boundaries are well-defined