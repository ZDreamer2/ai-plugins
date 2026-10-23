# Document Template Block Format

## Basic Template

```markdown
## Basic Template

[Template structure]

## Template Notes (optional)

[Template context]

### [Placeholder name]

[Placeholder explanation]

### "[Section name]" section

[Section explanation]
```

## Template Notes

### Placeholders

Placeholders use square brackets and are named like class or method names - concise identifiers, not explanations. Template Notes section provides detailed explanations for each placeholder.

- Good: `[Chunk goal]`, `[Purpose point]`, `[File entry]`
- Bad: `[What success looks like for this chunk]`, `[Brief explanation of why this file changes]`

When placeholder references content defined by a block specification, start with block filename:
- Format: `[BlockDoc.md: brief context]`
- Example: `[CodeExample.md: complete example of this program unit]`

### Modifiers

Modifiers are parenthetical markers placed after headers or placeholders to indicate structural constraints. They use parentheses and lowercase text to be clearly distinct from `[Placeholders]` and `ACTION` keywords.

Available modifiers:
- `(optional)` - section or element may be omitted
- `(one or more)` - element repeats, at least one required

### [Template structure]

Complete document structure with all headers, sections, and content placeholders

### "Template Notes" section

- Template-wide context and conventions as bullets or prose
- Subsections for individual template parts that need explanation

Subsection header conventions:
- For placeholders: `### [Placeholder name]`
- For sections: `### "Section name" section`

## Basic Example

```markdown
# Some Doc Specification

## Purpose

[Doc purpose]

## Context (optional)

[Doc context]

## Basic Template

[DocTemplate.md: template structure]

## Basic Example

[Doc example]

## Rules

[ValidationRules.md: validation rules]
```

## Rules

- MUST use markdown code blocks with `markdown` language identifier for templates
- MUST use placeholders in square brackets for variable content
- MUST use modifiers in parentheses with lowercase text
- MAY include Template Notes section with subsections for individual template parts
