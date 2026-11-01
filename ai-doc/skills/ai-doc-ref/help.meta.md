# help.meta.md

Specification for editing [reference lookup help](help.md). Defines purpose, usage patterns, and constraints.

## help.md goals and principles

- Fallback output when `print-ai-doc-by-ref.py` receives an unknown or missing argument
- MUST list all available short names and what ai-doc documents they map to
- Should be self-sufficient — an agent reading this output must understand what arguments are valid without further exploration

## AiDocFormat

[BaseDoc format](../../Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing help.md

- `ai-doc/skills/ai-doc-ref/Tools/print-ai-doc-by-ref.py` - Understand how help.md is printed and what arguments the script already handles
- [Reference lookup skill](SKILL.md) - Understand how the skill invokes the script

## help.md typical use context

### Distinct usage patterns for help.md

#### Printed as fallback by print-ai-doc-by-ref.py

Agent calls `${AGENT_SKILL(ai-doc:ai-doc-ref)} UnknownName` — script does not recognize the argument, prints help.md content instead

### Role help.md serves during use

- Error recovery: tells the agent what valid arguments exist so it can retry with a correct one
