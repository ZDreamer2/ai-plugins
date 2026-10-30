# TypicalUseContext Block Format

## TypicalUseContext template

```markdown
### 💡 Distinct usage patterns for [AiDocName].md

#### [Descriptive title for pattern]

[Pattern description: direct reference OR indirect loading]

[Optional explanation if adds value]
```

## Template Notes

NOTE: The 💡 emoji is a deliberate exception to [BaseDoc format](../../BaseDoc/BaseDoc.format.md) emoji restrictions. It serves as a human-detectability marker for quickly locating usage patterns, not for emphasis.

Purpose: Document distinct patterns of how the AiDoc gets loaded and used.

CRITICAL: Include only UNIQUE usage patterns representing genuinely different mechanisms or contexts. Having only 1-2 patterns is preferable to listing redundant variations.

### Pattern description formats

Choose format based on actual loading mechanism:

**Direct reference** - User explicitly mentions doc in prompt:
- Multi-line prompts: code blocks (triple backticks)
- Single-line prompts: inline backticks
- Shows actual user prompt

**Indirect loading** - Doc loaded through workflow/chain:
- Describe flow: trigger -> workflow -> doc reference
- Use `->` notation
- Shows loading mechanism, not user prompt

**Hybrid** - Both direct and indirect usage:
- Document both as separate #### sections

### [Pattern description: direct reference OR indirect loading]

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

## Validation Rules

- MUST include only UNIQUE usage patterns (each representing genuinely different mechanism or context)
- MUST use 💡 emoji in "Distinct usage patterns" subsection header
- MUST use level 4 headers (`####`) for each distinct pattern with descriptive title
- MUST choose pattern format based on actual loading mechanism:
  - Direct reference: use code blocks (triple backticks) for multi-line prompts OR inline backticks for single-line prompts
  - Indirect loading: describe the flow using `->` notation
- SHOULD include explanatory text only when it adds value beyond the pattern description
- SHOULD have 1-2 distinct patterns (preferable to listing redundant variations)
