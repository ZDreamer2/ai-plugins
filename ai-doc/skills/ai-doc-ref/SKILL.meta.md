# SKILL.meta.md

Specification for editing [ai-doc-ref skill](SKILL.md). Defines purpose, usage patterns, and constraints.

## SKILL.md goals and principles

- Exposes ai-doc plugin documents by short name to external project files without requiring knowledge of the installed plugin path
- MUST be a thin agent-executed invocation: run the Python script with the caller’s reference name as one argument, or no argument when no name is supplied, and read its output
- MUST use explicit agent execution without an argument-substitution variable
- For unknown arguments, MUST output [reference registry](help.md) listing available argument names
- Agent-facing skill, not user-facing — consumed by other skills and docs, not invoked directly by users

## AiDocFormat

[SKILL format](../../Formats/SkillDoc/SKILL.format.md)

## MUST read before editing SKILL.md

- [SKILL format](../../Formats/SkillDoc/SKILL.format.md) - Follow SKILL format for frontmatter and body structure
- [reference registry](help.md) - Understand the argument registry this skill exposes
- `ai-doc/skills/ai-doc-ref/Tools/print-ai-doc-by-ref.py` - The python script that does the actual work; SKILL.md delegates to it

## MAY read for additional context before editing SKILL.md

- [Reference path management](../../Theory/References/ReferencePathManagement.md) - Read when checking supported ways for external documents to reference ai-doc content
- [AiDoc terminology](../../Theory/AiDocTerminology.md) - When understanding `AI_DOC_PLUGIN` convention that this skill complements

## SKILL.md typical use context

### Distinct usage patterns for SKILL.md

#### External doc references ai-doc content by short name

`${AGENT_SKILL(ai-doc:ai-doc-ref)} StartSimple` — agent reads the output to get content of [StartSimple methodology](../../Theory/StartSimple.md)

#### External doc discovers available references

`${AGENT_SKILL(ai-doc:ai-doc-ref)}` or `${AGENT_SKILL(ai-doc:ai-doc-ref)} help` — agent gets the list of available short names and what they point to

### Role SKILL.md serves during use

- Bridge between external project files and ai-doc plugin content without requiring direct path knowledge
