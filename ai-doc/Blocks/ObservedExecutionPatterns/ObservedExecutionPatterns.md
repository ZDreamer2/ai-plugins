# Observed Execution Patterns Block Format

## Why Observed Execution Patterns

Workflow steps describe intended execution, but they do not carry knowledge of how previous executions actually went. That knowledge disappears with each session unless the workflow preserves it.

This block transfers decision-relevant experience between executions. It helps future agents exercise judgment with knowledge of recurring behavior, effective adaptations and failure patterns, rather than relying on the procedure alone.

## Observed Execution Patterns template

```markdown
## Observed Execution Patterns

[Observed execution patterns]
```

## Template Notes

### [Observed execution patterns]

Convey recurring behavior, effective adaptations, failure patterns or other observations when they would improve future decisions. Choose prose, bullets or named subsections suited to the owning workflow, and record reusable experience rather than incident chronology. The section has no required entry anatomy.

Use present tense for recurring patterns as current execution tendencies, and imperative or present tense for the response. Reserve past tense for historical conditions; "Observed" already establishes that the pattern comes from actual use.

## Observed Execution Patterns example

```markdown
## Observed Execution Patterns

AiDoc builds tend to carry too much gathered context into the first draft. Individually correct caveats, generic good practice and exhaustive detail accumulate, making the draft appear complete and defensible. Format, meta and reference checks can miss the weak fit for the intended reader.

The final review can then be glossed over: the agent loads [on-build-done.md](workflows/on-build-done.md) but finishes without applying its criteria to concrete passages, leaving the draft substantively unchanged.

Treat the first draft as provisional. Reconsider its overall usefulness to the intended reader, and execute the final review against the actual document rather than merely loading or reading its criteria.
```

## Validation Rules

- MUST describe patterns observed during actual workflow use
- MUST convey decision-relevant knowledge that the procedure alone does not supply
- MUST NOT contain hypothetical patterns or generic good practice
- SHOULD use a concise form suited to the owning workflow without duplicating its steps
