# Why We Omit `name` From Plugin SKILL.md Files

## The Bug

When a Claude Code plugin ships a skill with a `name` field in its SKILL.md frontmatter, the skill is registered **without the plugin namespace prefix**. The `name` value is used directly as the slash command, bypassing the `{plugin}:` prefix entirely.

**What happens:**

- Skill WITH `name` in frontmatter → `/my-skill` (no prefix — **wrong**)
- Skill WITHOUT `name` in frontmatter → `/my-plugin:my-skill` (correct prefix)

This means plugin skills with a `name` field leak into the global slash command namespace, potentially colliding with other plugins' skills or with project/personal skills.

**Upstream issue:** [anthropics/claude-code#22063](https://github.com/anthropics/claude-code/issues/22063) — filed January 2026, confirmed with reproduction steps, marked as bug. Still open as of March 2026.

## Why This Matters

When the bug is eventually fixed, all skills currently registered at the wrong path (`/my-skill`) will silently move to the correct path (`/my-plugin:my-skill`). Any references to these skills — in CLAUDE.md, in other skills' instructions, in muscle memory — will break without warning.

By omitting `name` now, our skills register at the correct namespaced path from day one. No migration needed when the fix lands.

## The Trade-off

The [Agent Skills specification](https://agentskills.io/specification) requires the `name` field. The spec states:

> The `name` field: Must be 1-64 characters [...] Must match the parent directory name.

Some implementations enforce this strictly — VS Code Copilot will not load a skill if `name` doesn't match the folder name. Others (Claude Code, Pi) are lenient and fall back to the folder name when `name` is absent.

We are knowingly violating the spec to get correct runtime behavior in Claude Code plugins. If Anthropic adds strict validation that rejects skills without `name`, we will need to add it back. The expectation is that the namespace prefix bug will be fixed before or alongside any such validation change.

## What To Do

- **Plugin skills:** Omit `name` from frontmatter. Use only `description`. Let the folder name serve as the skill identity.
- **Non-plugin skills** (project `.claude/skills/`, personal `~/.claude/skills/`): Include `name` per the spec. The bug only affects plugin-shipped skills.
- **Pi packages:** Include `name` per the spec. Pi uses its own `skill:name` namespacing which is not affected by this bug.

## Example

```yaml
# ✅ What we do for plugin skills
---
description: Analyze and fix database migration issues. Use when the user mentions migrations, schema changes, ALTER TABLE, or database versioning.
---
```

```yaml
# ❌ What the spec says to do (but triggers the bug in plugins)
---
name: db-migrations
description: Analyze and fix database migration issues. Use when the user mentions migrations, schema changes, ALTER TABLE, or database versioning.
---
```

## References

- [Agent Skills Specification](https://agentskills.io/specification) — `name` field requirements
- [anthropics/claude-code#22063](https://github.com/anthropics/claude-code/issues/22063) — the namespace prefix bug
- [anthropics/claude-code#29360](https://github.com/anthropics/claude-code/issues/29360) — related issue: plugin `allowed-tools` also fails to apply namespace prefix