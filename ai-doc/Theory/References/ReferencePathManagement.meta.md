# ReferencePathManagement.meta.md

Specification for editing [reference path management](ReferencePathManagement.md). Defines purpose, usage patterns, and constraints.

## ReferencePathManagement.md goals and principles

- Source of truth for how doc references are written within the ai-doc system
- Covers reference path bases, syntax by target type, and where required reading is signalled
- Defines the supported project/plugin boundaries without duplicating equivalent cases
- Provides mechanical rules (section-based) and judgment rules (body prose) for signalling required vs optional reading
- MUST prohibit `@path` context injection, including in skills, and explain the risk of repeated document injection when skills are reused
- MUST establish document-relative paths as the default within a project or plugin, including meta documents, with project-root paths for project code references
- MUST distinguish installed-plugin isolation from source-only marketplace meta documents: metas may reference sibling plugins, using document-relative links and directory paths, and marketplace-root paths for code and other non-Markdown files
- MUST preserve the required base of literal checkout paths in build commands, configuration and examples
- MUST use Markdown links for references to Markdown documents and backticks for other file references
- MUST reserve `AI_DOC_PLUGIN` for meta documents outside ai-doc referencing ai-doc content
- MUST keep host-specific variables and executable path handling outside these authoring rules
- MUST consider documents in different locations: project, ai-doc plugin, other plugins
- MUST cover both normal docs and AiDocMetaDocs as reference sources
- MUST distinguish links to follow from literal paths or syntax examples; preserve the separation between reference syntax and path-base policy

## AiDocFormat

[Base document format](../../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing ReferencePathManagement.md

- [AiDoc terminology](../AiDocTerminology.md) - Understand AI_DOC_PLUGIN definition and its resolution to plugin root

## MAY read for additional context before editing ReferencePathManagement.md

- [AiDoc base format](../AiDocBaseFormat.md) - Contains the brief actionable summary of link conventions; review to keep the two in sync

## ReferencePathManagement.md typical use context

### Distinct usage patterns for ReferencePathManagement.md

#### Consulted by plugin creators when designing path conventions

Loaded when making decisions about how references should work in skills, meta files, or new plugin scenarios.

#### Consulted when writing or reviewing any doc reference

Loaded when an agent needs to write a reference in any ai-doc: its destination base, its link syntax, and explicit reading obligations without context injection.

### Role ReferencePathManagement.md serves during use

- Design reference clarifying which destination convention applies within and across project/plugin boundaries
- Source of truth for how references are linked and how required reading is signalled
- Judgment guide for ambiguous body-prose references
- Decision guide when extending path handling in ai-doc skills
