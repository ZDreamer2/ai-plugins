# AiDoc System Foundation

This document establishes foundational terminology for the AiDoc documentation system. These definitions provide consistent vocabulary across all documentation workflows and tools.

## Core Terms

**AiDoc** - Any document that guides AI Agent during practical tasks in the project. Purpose: Direct AI during actual work (coding, planning, analysis).

**AiDocFormat** - Format specification that defines AiDoc structure and standards. Purpose: Establish consistent structure and rules for specific document types.

**AiDocFormatDoc** - Specification document that defines an AiDocFormat. Establishes WHAT documents in that format are and HOW to write them. Purpose: Teach AI how to create documents following a specific format.

**AiDocMetaDoc** - Additional context for creating or editing an AiDoc reliably, alongside the target when present. Purpose: Explain intent, usage context, important authoring constraints and relevant sources; the target owns its content and document-level decisions. Loaded during creation and editing, not during AiDoc use in normal tasks.

## File Naming Conventions

### AiDocFormatDoc Files

AiDocFormatDoc files use `.format.md` extension pattern:
- `CodeDoc.format.md`
- `Workflow.format.md`
- `AiDocFormatDoc.format.md`

An AiDoc references its AiDocFormatDoc through its AiDocMetaDoc or through the `edit-only-context` YAML frontmatter property.

### AiDocMetaDoc Files

AiDocMetaDoc files insert `.meta` before the final `.md` extension:
- `doc.md` -> `doc.meta.md`
- `doc.format.md` -> `doc.format.meta.md`

## Editing context

When creating or editing an AiDoc, read its meta, format and their required sources. This context is for editing, not normal document use.

Editing context comes from the companion `.meta.md` file or a meta/format referenced by the `edit-only-context` YAML property. Property paths are document-relative or use `AI_DOC_PLUGIN/...`.

## Plugin Reference Convention

`AI_DOC_PLUGIN` - Path prefix resolved by ai-doc editing workflows to the ai-doc plugin root. Used in meta documents outside ai-doc and in `edit-only-context` references outside ai-doc to reference ai-doc content. Inside ai-doc, use document-relative paths.

## Practical Examples

Two examples showing the complete system in practice:

```
IssueInfo.format.md (AiDocFormatDoc)
  -> defines: IssueInfo (AiDocFormat)
       -> guides writing: IssueInfo.md for issue #123 (AiDoc)
            -> editing context: IssueInfo.meta.md (AiDocMetaDoc)

Workflow.format.md (AiDocFormatDoc)
  -> defines: Workflow (AiDocFormat)
       -> guides writing: BuildDoc.md (AiDoc)
            -> editing context: BuildDoc.meta.md (AiDocMetaDoc)
```
