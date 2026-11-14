# TypicalUseContext Block Format

## TypicalUseContext template

```markdown
### 💡 Distinct usage patterns for [AiDocName].md

#### [Descriptive title for pattern]

[Pattern description: direct reference, indirect loading, inherited usage, or unobserved usage]

[Optional explanation if adds value]
```

## Template Notes

NOTE: The 💡 emoji is a deliberate exception to [BaseDoc format](../../BaseDoc/BaseDoc.format.md) emoji restrictions. It serves as a human-detectability marker for quickly locating usage patterns, not for emphasis.

Purpose: Document distinct patterns of how the AiDoc gets loaded and used.

Include only unique usage patterns representing genuinely different mechanisms or contexts. Having only 1-2 patterns is preferable to listing redundant variations.

For a new document without observed usage, state that plainly and identify any known loading relationship, such as a parent document or workflow. MUST NOT invent prompts, triggers or patterns to fill the section.

### Pattern description formats

Choose format based on observed usage or a known loading relationship:

- Direct reference - User explicitly mentions the document in a prompt:
  - Multi-line prompts: code blocks (triple backticks)
  - Single-line prompts: inline backticks
  - Show the actual user prompt.

- Indirect loading - Document loaded through a workflow/chain:
  - Describe the known flow: trigger -> workflow -> document reference
  - Use `->` notation.

- Hybrid - Both direct and indirect usage:
  - Document both as separate #### sections.

- Inherited or unobserved usage - Document has no observed usage pattern:
  - Identify any known parent document or workflow whose usage it inherits.
  - State what has not yet been observed.

### [Pattern description: direct reference, indirect loading, inherited usage, or unobserved usage]

Use level 4 headers (`####`) for each pattern with descriptive title. Include explanatory text only when it adds value beyond the pattern itself.

## TypicalUseContext example

Example showing hybrid case with both direct and indirect patterns:

```markdown
### 💡 Distinct usage patterns for BuildRepository.md

#### Loaded indirectly via workflow when building entity classes

User asks to implement entity -> BuildEntity workflow loads E_C_BuildClasses.md -> E_C_BuildClasses.md references BuildRepository.md for repository implementation guidance

#### Direct reference for repository modifications

`Edit src/Modules/Analytics/Domain/Report/Report/ReportRepository.php to add support for the entity "meta" field according to src/Core/Domain/Repository/Docs/Build/BuildRepository.md`
```

Example for a new document without observed direct usage:

```markdown
### 💡 Distinct usage patterns for Satellite.md

#### Usage inherited from parent documentation

Inherits usage from [Parent guide](../Parent.md); direct usage has not yet been observed.
```

## Validation Rules

- MUST represent observed usage or a known loading relationship; MUST NOT invent prompts, triggers or usage patterns
- MUST include only unique usage patterns representing genuinely different mechanisms or contexts
- MUST use 💡 emoji in "Distinct usage patterns" subsection header
- MUST use level 4 headers (`####`) for each distinct pattern with descriptive title
- MUST choose the pattern format matching the evidence:
  - Direct reference: show the actual prompt, using code blocks for multi-line prompts and inline backticks for single-line prompts
  - Indirect loading: describe the known flow using `->` notation
  - Inherited or unobserved usage: identify known inheritance and state what has not been observed
- SHOULD include explanatory text only when it adds value beyond the pattern description
- SHOULD have 1-2 distinct patterns, preferring fewer over redundant variations
