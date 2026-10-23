# HubSkill Format Specification

## What is document in HubSkill format

A HubSkill is a SKILL.md that serves as a single entry point to a domain. It does not perform the work itself — it classifies the user's intent and dispatches to focused handlers (workflows, sub-skills, scripts).

HubSkill is a sub-format of SKILL: frontmatter and general SKILL.md rules come from the [SKILL format](../SKILL.format.md); this spec defines only the body shape. A hub SKILL's AiDocMetaDoc lists both in `## AiDocFormat` — `SKILL.format.md` primary, `HubSkill.format.md` secondary.

## MUST read before planning HubSkill document

- [SKILL format](../SKILL.format.md) - Apply its frontmatter and general skill-writing rules before refining the hub body

## HubSkill template

```markdown
## Goal

Classify the user's intent and dispatch to the right handler.

## Context (optional)

[Cross-cutting context]

## Commands

- `/[skill-name] [verb] <args>` - Dispatch to `[Handler name]` (one or more)

## [Dispatch section]

### [Handler name]

[Handler description]

Follow [Handler workflow](path/to/handler-doc.md)

(one or more)

## [Fallback section] (optional)

[Fallback description]

Follow [Fallback workflow](path/to/fallback-handler.md)
```

## Template Notes

Template covers the SKILL.md body only. Frontmatter follows the [SKILL format](../SKILL.format.md). Handler paths are relative to the hub's SKILL.md.

### Frontmatter `argument-hint`

For hub skills `argument-hint` SHOULD list the available verbs (e.g. `docs <request>`, `workshop|explore|change <request>`). The verb is the routing key, so surfacing it in autocomplete is especially load-bearing for hubs.

### "Goal" section

The template sentence is the default — keep it as-is unless the hub has a more precise verb than "dispatch" for what it does. Resist re-adding a "single entry point for [domain]" preamble; the frontmatter `description` already carries that framing.

### "Context" section

Use only when there are facts or constraints that genuinely apply across all handlers (e.g. "all handlers assume a git working copy", "issue IDs are Redmine numbers without `#`"). Skip the section entirely when nothing of this kind needs stating — an empty Context section is worse than no section.

### [Cross-cutting context]

Facts, constraints, or conventions that apply across all handlers and would otherwise be duplicated into each handler doc or get lost.

### "Commands" section

Each entry SHOULD reference its handler by name (`Dispatch to \`[Handler name]\``). The handler section below carries the fuller description.

### [Handler description]

1-2 sentences covering what kind of request this handler takes.

### [Fallback description]

1-2 sentences covering when this escape hatch applies and why named handlers are preferred when they fit.

### Dispatch section preamble

A `When the request does not use an explicit command, classify the intent and act accordingly.` preamble MAY be added at the top of the dispatch section when handler labels diverge from command verbs and intent-based routing needs explicit framing. Omit when the Goal sentence already covers it (typical case).

## HubSkill example

Body of the `rm` hub skill (frontmatter omitted; paths are relative to `skills/rm/SKILL.md` in the rm plugin):

```markdown
## Goal

Classify the user's intent and dispatch to the right internal workflow.

## Commands

- `$${AGENT_SKILL(rm)} workshop <request>` - Dispatch to `Workshop`
- `$${AGENT_SKILL(rm)} explore <request>` - Dispatch to `Discover`
- `$${AGENT_SKILL(rm)} change <request>` - Dispatch to `Shallow changes`

## Workflows

When the request does not use an explicit command, classify the intent and act accordingly.

### Workshop

Single-issue focused work: read, analyze, craft, or edit one Redmine issue in depth. The issue is pulled into a local RmIssueDir; the agent works there and saves changes back (or no-ops).

Follow [Single-issue workshop](../../workflows/on-workshop-start/do.md)

### Discover

Multi-issue or criteria-based work: search, list, explore, aggregate across issues (queries, reports, counts).

Follow [Issue discovery](../../workflows/on-discover-start/do.md)

### Shallow changes

Quick metadata changes — status, assignment, priority, time tracking, short comments. Applies to one or many issues. Does not justify a local working copy.

Follow [Quick issue changes](../../workflows/on-edits-start/do.md)

## Direct Redmine API work

Fallback for requests that no workflow handles well — write ad-hoc Python that calls the Redmine API directly via a dedicated API handler. Most flexible path.

Use when:

- The request is genuinely outside the workflows above
- The user explicitly asks for a direct API approach

Prefer named workflows when they fit — they encode Bico practices the raw API does not.

Follow [Direct API handler](../../workflows/on-api-direct/do.md)
```

## Validation Rules

- MUST comply with the [SKILL format](../SKILL.format.md)
- MUST include Goal, Commands, and a dispatch section
- Hub MUST NOT carry the work itself — each handler entry MUST end with a `Follow` pointer to a separate handler doc
- Each command in Commands MUST map to exactly one handler section
- SHOULD include a fallback section only when a real request shape does not fit any named handler
