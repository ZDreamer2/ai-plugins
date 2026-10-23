# on-build-done.meta.md

Specification for editing [final documentation review](on-build-done.md). Defines purpose, usage patterns, and constraints.

## on-build-done.md goals and principles

- Provides a final review lens for recurring, cross-cutting documentation pains after an AiDoc build
- MUST remain compact and include only considerations proven relevant across AiDocs
- MUST complement rather than duplicate AiDocFormat validation and AiDocMetaDoc checks
- Assumes the Agent already has the full build context and trusts it to determine situation-specific action

## AiDocFormat

[BaseDoc format](../../../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing on-build-done.md

- [StartSimple methodology](../../../Theory/StartSimple.md) - Use evidence from recurring build pain to decide whether a consideration belongs in this shared final review
- [Constraint theory](../../../Theory/GuideVsGiveFreedom.md) - Apply its constraint boundary so considerations preserve Agent judgment in the specific build context
- [AiDoc creation workflow](../do.md) - Identify the invocation point and checks already completed before this final review

## on-build-done.md typical use context

### 💡 Distinct usage patterns for on-build-done.md

#### Loaded after standard build validation

AiDoc build -> BuildDoc workflow completes its format and meta checks -> on-build-done.md reviews the resulting changes

### Role on-build-done.md serves during use

- Shared final review for recurring documentation concerns not owned by a specific AiDocFormat or AiDocMetaDoc
- Evidence-based extension point for considerations that should apply to every AiDoc build
