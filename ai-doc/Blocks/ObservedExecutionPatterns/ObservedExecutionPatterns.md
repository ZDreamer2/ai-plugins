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

## Observed Execution Patterns example

```markdown
## Observed Execution Patterns

### Draft preservation

Initial AiDoc builds have carried too much gathered context into the first draft. Individually correct caveats, generic good practice and exhaustive detail accumulated, making the draft appear complete and defensible. Format and reference checks then reinforced acceptance instead of prompting reconsideration.

Reconsider the draft's overall usefulness to the intended reader before treating mechanical validation as completion.
```

## Validation Rules

- MUST describe patterns observed during actual workflow use
- MUST convey decision-relevant knowledge that the procedure alone does not supply
- MUST NOT contain hypothetical patterns or generic good practice
- SHOULD use a concise form suited to the owning workflow without duplicating its steps
