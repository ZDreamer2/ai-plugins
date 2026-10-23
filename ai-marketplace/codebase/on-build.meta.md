# on-build.meta.md

Authoring context for [marketplace build guidance](on-build.md).

## on-build.md goals and principles

- Give builders reusable implementation conventions and verification responsibilities without depending on planning context.
- Ai-doc authoring is required for every Markdown edit, including minor changes. Keeping verification proportional does not make that authoring process optional.
- Keep additional checks tied to affected contracts; avoid prescribing recurring work solely because it might be useful.
- Serve any marketplace adopting this CodebaseType; concrete SDKs, host support and tool commands belong to that marketplace.

## AiDocFormat

[BaseDoc format](AI_DOC_PLUGIN/Formats/BaseDoc/BaseDoc.format.md) - This is a phase guidance entry, rather than a guide to one code unit or API.

## MUST read before editing on-build.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Limit instructions to established needs and evaluate the recurring cost of mandatory work.

## on-build.md typical use context

### 💡 Distinct usage patterns for on-build.md

#### Loaded during implementation

Caller selects marketplace codebase guidance -> the build workflow loads `on-build.md` alongside the task's implementation references.

### Role on-build.md serves during use

Supplies implementation and verification obligations to a builder who may not have read `on-plan.md`.
