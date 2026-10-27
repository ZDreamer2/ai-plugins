# AiDocMetaDoc Theory and Context

## Purpose and Function of AiDocMetaDocs

AiDocMetaDocs can precede the target document: they provide additional context for authorship and later editing. They leave document-level decisions to the target rather than recording a complete specification in advance. Their content boundary is defined by the [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md).

AiDocMetaDocs serve multiple critical functions:
- Helpful documentation to simplify editing AiDoc by providing examples and references
- Anchor that prevents AiDoc "drift" during multiple edits
- Explicit statement of AiDoc's relationship to other documentation
- Preservation of underlying theory too complex for practical guide

Key insight: AiDocMetaDocs are both helpful (providing examples, references) and protective (preventing drift, maintaining boundaries)

## AiDocUse vs AiDocEdit: The Two Scenarios

1. AiDocUse - AI Agent reads AiDoc during practical coding tasks
	- AiDoc appears in context through various mechanisms
	- AiDoc provides actionable guidance for immediate task
	- Token efficiency critical due to frequent loading

2. AiDocEdit - AI Agent creates or modifies AiDoc as a specific documentation task
	- AiDocMetaDoc loaded to provide editing context
	- AiDocMetaDoc explains AiDocUse patterns
	- AiDocMetaDoc prevents scope creep and maintains focus

## Why AiDocMetaDocs Matter

Without AiDocMetaDocs:
- AiDocs drift from original purpose over multiple edits
- Related AiDocs develop overlapping content
- Important context gets lost between editing sessions
- AiDocs become inconsistent with each other

With AiDocMetaDocs:
- Each AiDoc maintains clear boundaries and purpose
- Related AiDocs complement rather than duplicate
- Editing decisions informed by AiDocUse patterns
- Documentation ecosystem remains coherent

## When AiDocMetaDocs Are Used

CRITICAL: AiDocMetaDocs are ONLY loaded during AiDocEdit scenarios, NEVER during AiDocUse.

This separation is essential:
- AiDocUse requires token efficiency and immediate actionability
- AiDocEdit requires full context and theoretical understanding
- Mixing these scenarios would burden practical tasks with editing context

## AiDocMetaDoc as Contract

AiDocMetaDoc serves as contract between:
- AiDoc creator's original intent
- Future editors' modifications during AiDocEdit
- End users' needs during AiDocUse

This context helps editors judge changes in light of the document's purpose and use. It does not freeze the original contents or require the meta to retain decisions already expressed in the document.

## Format Requirements for AiDocs

Every AiDoc follows an AiDocFormat that defines its structure and documentation standards. Formats may come from this plugin's `../Formats/` directory or the project.

### Format selection

The [meta creation workflow](../workflows/meta/do.md) selects the format from explicit requirements or the intended document role. The meta records that choice so future authors apply the same structural contract.

### Format in AiDocMetaDocs

The dedicated `## AiDocFormat` section links to the applicable format specification. Reading that format is required; the section heading carries the obligation without an `@` marker or duplicate reading-list entry.

For structure and link conventions, follow the [AiDocMetaDoc format](../Formats/MetaDoc/AiDocMetaDoc.format.md).

### Why Format Matters

Format requirements ensure:
- Consistent structure across documentation ecosystem
- Appropriate token efficiency for each documentation type
- Clear expectations for documentation creators and editors
- Predictable documentation patterns for AI Agent during AiDocUse

Without explicit format designation, AiDocs risk:
- Inconsistent structure making them harder to maintain
- Inappropriate verbosity or terseness for their purpose
- Confusion about which standards apply

## HubDoc and ChildDoc Theory

The HubDoc-ChildDoc pattern enables efficient, maintainable documentation for complex domains with both simple and specialized use cases.

### Conceptual Model

HubDocs and ChildDocs form a hub-and-spoke documentation pattern:
- HubDoc sits at the center as the primary entry point
- ChildDocs extend outward as specialized spokes for complex scenarios
- This pattern prevents documentation sprawl while maintaining completeness

### When to Designate an AiDoc as HubDoc

An AiDoc becomes a HubDoc when:
- It serves as the primary entry point for a domain
- Multiple specialized scenarios exist that would bloat a single document
- Basic use cases need immediate, self-contained guidance
- Decision-making logic can route to appropriate specializations

Examples:
- `Build.md` - HubDoc for repository creation, routes to plugin-specific ChildDocs
- Main configuration guides that have environment-specific variations

### When to Create ChildDocs

Create a ChildDoc when:
- A specific scenario requires extensive specialized guidance
- Including the content in HubDoc would obscure basic use cases
- The specialization is only needed for a subset of users
- The content naturally extends rather than replaces HubDoc guidance

Examples:
- `EntityLink.md` - ChildDoc extending `Build.md` for entity relationship scenarios
- Plugin-specific implementations extending base functionality guides

### Loading Patterns

The loading relationship is asymmetric:
- HubDocs are loaded directly from user prompts or task context
- ChildDocs are NEVER loaded directly, only through HubDoc routing
- HubDoc contains explicit logic: "For X scenario, see ChildDoc Y"
- When ChildDoc loads, its HubDoc is always loaded alongside for context

This pattern ensures:
- Users always enter through the appropriate entry point
- Context is preserved through the HubDoc
- ChildDocs can assume HubDoc knowledge

### Boundary Management

Clear boundaries prevent documentation decay:
- HubDoc MUST be self-sufficient for basic cases
- ChildDocs MUST NOT duplicate HubDoc content
- Each ChildDoc has a specific, non-overlapping specialization
- HubDoc explicitly states what each ChildDoc covers

Anti-patterns to avoid:
- ChildDoc that could stand alone (should be independent AiDoc)
- HubDoc that requires ChildDoc for basic cases (violates self-sufficiency)
- Multiple ChildDocs with overlapping scope (creates confusion)
- ChildDoc referenced directly without HubDoc context
