# do.meta.md

Specification for editing [refine workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables refinement of user-edited AiDocs into clear, concise, consistent documentation while preserving the user's intended changes.
- Preserve the document's communicative role: definitions, descriptions, specifications, and instructions need different forms of expression. Do not turn declarative content into procedural guidance merely to make it more actionable.
- Combines the user's operational experience and editorial direction with AI language precision, consistency checking, and critical reading. Preserve organization by default without assuming that either user edits or previous AI writing are always correct.
- Prevent refinement from becoming a rebuild: local clarity and consequences of the user's edits are in scope; independent redesign belongs in reported concerns. Structural preservation does not mean concealing structural problems.
- Treat the user's edits and explanations as the intended direction, including deletions and relaxed requirements. Previous versions and meta documents provide context, not grounds to silently reverse a change. Clearly erroneous or self-contradictory edits still need resolution.
- Include consistency beyond changed sentences: stale references and directly affected meta guidance were observed weaknesses in manual editing. Keep this scope tied to the edit rather than inviting an unrelated documentation cleanup.
- Avoid a rigid one-sentence limit or word budget: splitting a tangled sentence or adjusting adjacent wording can preserve meaning better. Preserve the level of detail and favor stable or shorter length; additions need a concrete clarity or consistency purpose.
- Balance autonomy with uncertainty. Routine corrections need no approval; well-supported interpretations can be made and reported. Materially different plausible meanings need clarification, with concise alternatives and the AI's recommended reading first. Reporting a call does not replace resolving uncertain intent.
- Keep the final report useful for calibrating AI judgment: meaningful interpretive calls, unresolved questions, and concerns beyond refinement matter; an inventory of grammar fixes does not.

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Apply its criteria for necessary guidance; resist adding speculative safeguards or elaborate review machinery.
- [Constraint theory](../../Theory/GuideVsGiveFreedom.md) - Use its distinction between coordination and investigation to set editorial boundaries without prescribing every correction.

## MAY read for additional context before editing do.md

- [Ai-doc skill entry point](../../skills/ai-doc/SKILL.md) - Read when aligning workflow dispatch and invocation with the skill entry point.
- [Build workflow](../build/do.md) - Read when distinguishing refinement of user edits from broader document creation or improvement.
- [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md) - Read when defining how refinement keeps editing context aligned without duplicating runtime instructions.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Intended dispatch after manual documentation edits

User edits an AiDoc -> invokes ai-doc refine with the target and relevant git changes -> the skill loads this workflow.

The user supplies editorial direction through the edits and may explain their intent in the conversation. Git changes may be uncommitted or identified by a commit, as in the motivating review.

### Role do.md serves during use

- Guides an editing pass that makes the user's changes clear and internally coherent, including their direct effects on related documentation.
- Separates corrections and supported interpretations from unresolved intent and independent design proposals.

## do.md underlying theory

### Evidence behind the boundaries

The motivating review examined commit `7d5513e6` in `ai/bc-plugins`, file `dev/forge/skills/drive/workflows/build-chunk.md`. Grouping build and fix rounds improved the workflow's organization, while stale step references and meta guidance showed the need for consistency repair. An awkward builder-context sentence showed why refinement sometimes requires interpreting a tradeoff rather than correcting grammar alone.

The user confirmed that deleting the rare scope-explosion branch and selecting which driver decisions to report were intentional simplifications. Restoring the old rules would therefore defeat the edit. Conversely, making acceptance wording precise could preserve the intended gate without adding defensive instructions. These observations justify a refinement boundary; they do not establish that every user edit improves agent behavior. Actual runs remain the evidence for policy effectiveness.
