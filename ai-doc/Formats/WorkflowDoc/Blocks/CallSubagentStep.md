# CallSubagentStep Block Format

## CallSubagentStep template

Steps that delegate work to subagents. Two modes:

- Fork, written as `$${AGENT_FORK}`: inherits parent context — all loaded documents, dialogue history visible to the subagent
- Fresh, written as `$${AGENT_SUBAGENT_TOOL}` with the subagent kind: independent context — subagent starts clean, prompt MUST be self-contained

```markdown
### Step [N]: [Active verb + what is delegated]

Launch [mode description] subagent via [call]:

```
[exact prompt for subagent]
```

[Post-launch guidance: wait for result, what to extract, etc.]
```

Template notes:
- `[mode description]`: "fork" or "fresh-context" with brief rationale why this mode
- `[call]`: how the chosen mode above is called, so that the step names a tool and not only a mode
- `[exact prompt]`: the literal prompt passed to the subagent
- Step may vary: multiple subagents in parallel, described prompt instead of exact, conditional delegation

## CallSubagentStep example

### Step 2: Launch separate review

Launch fresh-context subagent via ${AGENT_SUBAGENT_TOOL} tool (independent perspective on code changes):

```
Read and follow [external review workflow](../on-external-review/do.md)
```

MUST wait for the subagent to return before Step 3 — read the returned path to get findings.

## Validation Rules

- MUST specify subagent mode (fork or fresh) with rationale
- MUST include exact prompt in code block when prompt is known ahead of time
- MUST include post-launch guidance when the parent workflow depends on subagent output
