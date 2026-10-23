# docs-usefulness.meta.md

Specification for creating and editing the [documentation usefulness guidance](docs-usefulness.md). Defines purpose, usage context and authoring constraints.

## docs-usefulness.md goals and principles

- The document provides editorial guidance for revising documentation to help its intended reader understand what matters and proceed with reasonable effort, given the document's purpose and usage context.
- Its underlying concern is the cumulative cost of reading. Agents often load multiple documents together; even accurate content consumes context and competes for attention. Editorial effort improves repeated use by preserving information that supports decisions and prevents likely mistakes. Reading frequency is part of that cost, so the guidance scales editorial effort by how often the text is loaded and by which reader.
- Usefulness includes appropriate abstraction, sufficient context and clear ownership of explanations. The value of implementation detail depends on the document's purpose and what its reader needs beyond the source code and other available documents.
- Concision serves usefulness. Removing repetition or incidental detail and adding missing context can both improve a document; shorter text alone is not the measure of success, but growth is a cost that a change has to justify, more so the more tasks load the document. Readers still need the intent, contracts and constraints that guide their work. Leaving text unchanged is a stated outcome, because the other directives push toward editing and rewording without a reader benefit costs review attention.
- Ownership follows purpose and altitude: needing a compact explanation does not make a document the owner of its full reasoning. The main document can retain the picture its reader needs while a satellite owns the detail; useful overlap preserves understanding without creating competing explanations. Session evidence (2026-09-23, protocol refinement): a first pass restated new facts three times within one high-altitude protocol and had to be asked to cut them; a stricter "one mention per fact" formulation was tried and rejected as unrealistic for lower documents.
- The document supplies shared editorial judgment for AiDoc workflows and other callers, during both planning and editing. The compact workflow uses it to judge what earns its reading cost and whether satellite extraction improves usefulness. Document selection, context gathering, satellite meta creation and editing coordination belong to the invoking workflows, not this guidance.
- Its origin in a specific documentation review workflow does not restrict its scope or carry that workflow's file exclusions into its principles.

## AiDocFormat

[BaseDoc format](../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing docs-usefulness.md

- [StartSimple methodology](StartSimple.md) - Explains why this guidance focuses on established editorial needs rather than a catalog of document types or mandatory checks.

## docs-usefulness.md typical use context

### 💡 Distinct usage patterns for docs-usefulness.md

#### Loaded through the compact workflow

User requests compaction -> ai-doc skill dispatches to the compact workflow -> workflow loads this guidance with the target's authoring context -> agent assesses content and document boundaries against reader needs and combined reading effort.

#### Reuse by documentation planners and editors

Caller selects documentation and gathers its purpose and usage context -> loads this guidance -> agent applies its editorial judgment to planned or actual changes, including documents used together.

### Role docs-usefulness.md serves during use

- Shared editorial perspective on how well documentation serves its reader's task relative to the attention it requires.
- Foundation for compaction and satellite decisions without prescribing workflow mechanics.
