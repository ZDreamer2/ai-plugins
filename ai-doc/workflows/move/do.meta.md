# do.meta.md

Specification for editing [documentation relocation workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Systematic workflow for moving documentation files while maintaining reference integrity
- MUST ensure all references are updated when files move
- MUST handle accompanying .meta.md files (move them together with main AiDocs)
- MUST verify no broken references remain after move
- Reference search MUST stay in find-doc.py rather than returning to prose instructions: search tools respect .gitignore by default, so nested sibling repositories - which hold the references most likely to break - are skipped without any signal, and describing the workaround would prescribe HOW to search

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Apply its AiDocMetaDoc naming convention when maintaining document pairs

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Dispatched by the ai-doc skill on a move request

`/ai-doc move docs/OldPath/doc.md to docs/NewPath/doc.md`

`/ai-doc move docs/OldFolder/ to docs/NewFolder/`

User invokes ai-doc move -> [ai-doc skill](../../skills/ai-doc/SKILL.md) classifies the request -> the skill loads do.md

### Role do.md serves during use

- Procedural orchestration of file movement with reference integrity
- Ensures .meta.md files are moved together with their main AiDocs
- Quality control through verification that no broken references remain
