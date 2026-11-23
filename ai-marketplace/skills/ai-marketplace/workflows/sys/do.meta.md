# do.meta.md

Specification for creating and editing the [marketplace system configuration workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Provides a shared configuration entry point with named branches for central marketplace delivery and local source editing.
- Keeps central hosting and publication separate from workstation setup while exposing both through the `sys` command.
- Leaves target-specific authorization, safety and verification boundaries to the selected scenario.

## AiDocFormat

[BaseDoc format](AI_DOC_PLUGIN/Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps the dispatcher limited to established configuration targets.
- [ai-marketplace hub](../../SKILL.md) - Defines the `sys` invocation boundary this workflow receives.
- [Central repository configuration](configure/do.md) and [local editing configuration](local/do.md) - Own the scenarios and boundaries that the dispatcher must preserve.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Loaded through the ai-marketplace hub

User invokes `sys configure-central` or `sys configure-local` -> the hub loads this workflow -> the workflow selects the scenario that owns the requested target.

### Role do.md serves during use

- Shared system-configuration entry point and scenario dispatcher.
