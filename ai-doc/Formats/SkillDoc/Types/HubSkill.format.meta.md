# HubSkill.format.meta.md

Specification for editing [HubSkill format](HubSkill.format.md). Defines purpose, usage patterns, and constraints.

## HubSkill.format.md goals and principles

- Defines HubSkill as a sub-format of SKILL: a SKILL.md that serves as a single entry point to a domain, classifying user intent and dispatching to focused handlers (workflows, sub-skills, scripts)
- Conveys what a hub skill IS — its anatomy and constituent elements
- Companion to [SKILL format](../SKILL.format.md): SKILL.format.md governs SKILL.md writing in general; HubSkill.format.md narrows the shape for the hub case
- NOT a how-to-write guide and NOT a when-to-choose decision aid — both are out of scope
- MUST NOT duplicate general SKILL writing guidance from [SKILL format](../SKILL.format.md)
- MUST apply StartSimple — hub skill pattern is still emerging in this codebase, describe only elements observed in real hub skills

## AiDocFormat

[AiDocFormatDoc format](../../FormatDoc/AiDocFormatDoc.format.md)

## MUST read before editing HubSkill.format.md

- [SKILL format](../SKILL.format.md) - Parent format; HubSkill.format.md MUST NOT restate anything already covered there
- [StartSimple methodology](../../../Theory/StartSimple.md) - Apply minimal approach; expand only when real usage reveals gaps

## HubSkill.format.md typical use context

### 💡 Distinct usage patterns for HubSkill.format.md

#### Loaded during BuildDoc workflow when creating a hub-style SKILL.md

User asks to create or improve a SKILL.md and signals hub-skill kind -> [BuildDoc workflow](../../../workflows/build/do.md) loads [SKILL editing context](../SKILL.format.meta.md) -> [SKILL format](../SKILL.format.md) routes to [HubSkill format](HubSkill.format.md) for the hub sub-format spec

### Role HubSkill.format.md serves during use

- Format reference: defines what artifact the term "hub skill" denotes and its template
- Anatomy reference: enumerates the constituent elements of a hub skill (single entry point, explicit commands, classification, dispatch targets, fallback)
- NOT consulted for deciding whether a SKILL should be a hub, NOT a step-by-step writing process
