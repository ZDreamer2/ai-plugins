# SKILL.meta.md

Specification for editing [ai-doc hub skill](SKILL.md). Defines purpose, usage patterns, and constraints.

## SKILL.md goals and principles

- Primary entry point to ai-doc documentation ecosystem — single user-facing skill for all documentation workflows
- MUST be self-sufficient for routing users to the correct handler without requiring knowledge of internal skill names
- Delegates actual work to specialized workflows; keep their procedures out of the hub
- Keep descriptions only as detailed as needed to distinguish workflows and route requests; editing rules belong in the handlers
- Omit the Commands section as a deliberate exception to the [HubSkill format](../../Formats/SkillDoc/Types/HubSkill.format.md): argument-hint and handler descriptions already provide the routing information
- User-invocable only — agents SHOULD NOT auto-load this hub

## AiDocFormat

[SKILL format](../../Formats/SkillDoc/SKILL.format.md)
[HubSkill format](../../Formats/SkillDoc/Types/HubSkill.format.md)

## MUST read before editing SKILL.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Keep hub routing minimal; add dispatch entries only when evidence shows users need them
- [HubSkill format](../../Formats/SkillDoc/Types/HubSkill.format.md) - Apply the hub dispatch structure with Follow pointers, subject to the Commands-section exception above

## MAY read for additional context before editing SKILL.md

- [AiDoc creation workflow](../../workflows/build/do.md) - Read when adding or modifying the doc-build dispatch entry
- [Documentation refinement workflow](../../workflows/refine/do.md) - Read when adding or modifying the refine dispatch entry or distinguishing it from broader doc improvement
- [AiDocMetaDoc creation workflow](../../workflows/meta/do.md) - Read when adding or modifying the doc-build-meta dispatch entry
- [Documentation move workflow](../../workflows/move/do.md) - Read when adding or modifying the move dispatch entry
- [Documentation debugging workflow](../../workflows/debug/do.md) - Read when adding or modifying the debug dispatch entry
- [AiDoc stress-test workflow](../../workflows/stress-test/do.md) - Read when adding or modifying the stress-test dispatch entry or distinguishing it from refinement and session debugging
- [AiDoc compaction workflow](../../workflows/compact/do.md) - Read when modifying the compact dispatch entry or distinguishing purpose-aware compaction from refinement of user edits

## SKILL.md typical use context

### 💡 Distinct usage patterns for SKILL.md

#### Direct user invocation as the single ai-doc entry point

`${AGENT_SKILL(ai-doc)} build meta for src/Domain/Order/Docs/BuildOrder.md`

`${AGENT_SKILL(ai-doc)} debug — the workflow missed a validation rule`

`${AGENT_SKILL(ai-doc)} move src/old/path/Doc.md to src/new/path/`

### Role SKILL.md serves during use

- Single user-facing entry point for all ai-doc documentation workflows
- Intent classifier routing requests to the appropriate handler skill
- Decision tree for when to consult which specialized skill
