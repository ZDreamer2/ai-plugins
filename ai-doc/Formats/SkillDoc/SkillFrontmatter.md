# SKILL Frontmatter Reference

## Template

```yaml
name: [Skill name]
description: [Skill description]
user-invocable: [true|false]
disable-model-invocation: [true|false]
license: [License] (optional)
compatibility: [Compatibility] (optional)
metadata: (optional)
  [key]: [value]
allowed-tools: [Tools] (optional)
```

## Fields

Required:
- name - 1-64 chars. Lowercase letters, numbers, hyphens only. No leading/trailing/consecutive hyphens.
- description - 1-1024 chars. Third person. Capability and trigger conditions for agent discovery.

Optional:
- license - License name or reference to bundled license file.
- compatibility - 1-500 chars. Environment requirements (product, packages, network). Include only when skill has specific requirements.
- metadata - Key-value string map for additional properties.
- allowed-tools - Space-delimited list of pre-approved tools. Experimental.

### Name

Must match the parent directory name exactly. Uses lowercase with hyphens as word separators.

Valid: `code-review`, `pdf-processing`, `data-analysis`
Invalid: `Code-Review` (uppercase), `-pdf` (leading hyphen), `pdf--tool` (consecutive hyphens)

MUST NOT contain XML tags or reserved words ("anthropic", "claude").

### Description

Description is a routing signal, not instruction. Agents see all skill descriptions and decide which to load for the current task. Implementation details belong in the body.

Descriptions load on every inference - every token is paid on every API round-trip across the entire session. Goal: maximum routing precision with minimum tokens.

Compression test: if removing a word does not reduce routing precision, remove it. Avoid enumerating semantically overlapping triggers - one precise term beats three synonyms.

MUST NOT contain XML tags.

MUST write in third person. Include:
- Capability: what the skill does
- Trigger conditions: when to activate it

GOOD: `Runs SQL queries against project databases. Use when database queries or schema inspection is needed.`
GOOD: `Extracts text and tables from PDF files, fills forms, merges documents. Use when working with PDFs or document extraction.`
POOR: `Helps with PDFs.` (too vague - no capability, no trigger)
POOR: `I can help you query databases` (wrong point of view)
POOR: `Runs SQL queries against project MariaDB databases. Use when needing to query, inspect, or modify database data, explore table structures, or investigate data-related issues.` (overlapping triggers, technology name that adds no routing value)

## Claude Code Extensions

Claude Code adds these fields beyond the open format. `user-invocable` and `disable-model-invocation` MUST be set explicitly on every skill — relying on defaults hides invocation policy from anyone reading the frontmatter. The rest are optional.

- user-invocable - Set false to hide from / menu. Use for background knowledge Claude loads when relevant but users SHOULD NOT invoke directly.
- disable-model-invocation - Set true to prevent Claude from auto-loading this skill.
- argument-hint - Hint shown during autocomplete. Example: [issue-number], [filename] [format].
- model - Model override when this skill is active.
- context - Set to fork to run in an isolated subagent context.
- agent - Subagent type when context: fork. Options: Explore, Plan, general-purpose, or custom agents from .claude/agents/.
- hooks - Hooks scoped to this skill's lifecycle.
