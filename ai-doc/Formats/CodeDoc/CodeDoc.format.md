# CodeDoc Format Specification

## What is document in CodeDoc format

A CodeDoc document guides AI when working with code. Each document describes one "code concept" and teaches how to work with it correctly.

CodeDoc has two modes:

- CodeUnit - documents a file type: how to WRITE it (Controller, Repository, Enum, Blade template, etc.)
- CodeUsage - documents an API, pattern, or subsystem: how to USE it across different code (PdoExecutor, Events, Caching, etc.)

## MUST read before planning CodeDoc document

- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its formatting and writing principles
- [StartSimple methodology](../../Theory/StartSimple.md) - Start minimal and expand only when evidence shows gaps

## MAY read for additional context before planning CodeDoc document

- [Code example block](../../Blocks/CodeExample/CodeExample.md) - Read when working on Comprehensive Example section
- [Validation rules block](../../Blocks/ValidationRules/ValidationRules.md) - Read when working on Rules section

## CodeDoc template

```markdown
# [CodeConcept]

[Code concept definition]

## MUST read to understand [CodeConcept] (optional)

- [Subject or role](path/to/document.md) - [why essential for understanding this code concept] (one or more)

## Comprehensive Example

[CodeExample.md: complete example of this code concept]

[Zero or more topic sections for complex aspects]

## MAY read for additional context (optional)

- [Subject or role](path/to/document.md) - [when relevant for working with this code concept] (one or more)

## Rules

[ValidationRules.md: rules for this code concept]
```

## Template Notes

### [CodeConcept]

Name of the code concept being documented.

- CodeUnit mode: file type name (e.g., "Blade Template", "Repository Class", "PHPUnit Test")
- CodeUsage mode: API or pattern name (e.g., "PdoExecutor", "Repository Events", "Type Usage")

### [Code concept definition]

One to three sentences defining the code concept.

- CodeUnit mode: focus on WHAT the file type is, not WHEN to use it
- CodeUsage mode: focus on WHAT the API/pattern does and where it applies

### "MUST read to understand [CodeConcept]" section

Optional section for code concepts that depend on foundational concepts.

- Include when code concept only makes sense in context of broader domain concepts (e.g., Repository requires Entity + Collection understanding)
- Omit when code concept is self-contained and comprehensible from example alone
- Descriptions answer "why essential for understanding" - not just what document contains

### "Comprehensive Example" section

A single, dense code example demonstrating the code concept. Follow [code example rules](../../Blocks/CodeExample/CodeExample.md) for inline comments and self-sufficiency.

- CodeUnit mode: complete file showing the file type
- CodeUsage mode: usage patterns and snippets showing how to use the API/pattern

### [Zero or more topic sections for complex aspects]

Optional sections where one comprehensive example cannot cover all important aspects. Guidelines:

- Add when code concept has distinct subsystems, configuration options, or patterns needing dedicated explanation
- Each section addresses one topic with its own header (e.g., "Repository Options", "Helper Methods", "Common Patterns")
- May contain CodeExample blocks following [code example rules](../../Blocks/CodeExample/CodeExample.md) - these illustrate specific topics, not as parallel comprehensive examples
- The Comprehensive Example remains the primary teaching vehicle; topic sections supplement it
- Rules section MUST remain at the end

Examples: [Repository example](Examples/BuildRepository.md), [Migration class example](Examples/MigrationClass.md)

### "MAY read for additional context" section

Optional section for code concepts that may benefit from additional context files.

- Descriptions answer "when relevant for working with" - enable reader to decide if needed for current task

### "Rules" section

Critical rules specific to this code concept. Do not duplicate rules from the codebase's convention docs in its guidance folder (e.g. `docs/code/CONVENTIONS.md`).

## CodeDoc examples

- CodeUnit: [Blade template example](Examples/BladeTemplate.md)
- CodeUsage: [Database query interface example](Examples/PdoExecutor.md)

## Validation Rules

- MUST follow template structure
- MUST comply with [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- MUST NOT duplicate rules from the codebase's convention docs in its guidance folder (e.g. `docs/code/CONVENTIONS.md`)
- MUST include Comprehensive Example and Rules sections
- IF CodeUnit mode THEN MUST NOT include usage guidance (WHEN to use this file type)
