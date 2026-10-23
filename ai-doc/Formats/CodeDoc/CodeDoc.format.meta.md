# CodeDoc.format.meta.md

Specification for editing the [CodeDoc format](CodeDoc.format.md). Defines purpose, usage patterns, and constraints.

## CodeDoc.format.md goals and principles

- Defines how to create AiDocs that guide AI when writing specific types of code files
- Each CodeDoc document describes one "program unit" - a distinct file type in the system (Controller, Repository, Enum, Interface, Test, Blade template, JS widget, etc.)
- MUST follow StartSimple methodology - start minimal, expand based on usage evidence
- Format enables consistent creation of code guidance across different file types

## AiDocFormat

[AiDocFormatDoc format](../FormatDoc/AiDocFormatDoc.format.md)

## MUST read before editing CodeDoc.format.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Keep the format minimal and expand only when usage reveals gaps
- The codebase's convention docs in its guidance folder (e.g. `docs/code/CONVENTIONS.md`) - Understand project conventions that should NOT be duplicated in CodeDoc documents

## MAY read for additional context before editing CodeDoc.format.md

- [Blade template example](Examples/BladeTemplate.md) - Read when shaping a concise document around a comprehensive example and a small set of rules
- [Migration class example](Examples/MigrationClass.md) - Read when supplementing a comprehensive example with sections on execution, schema selection, and helper methods
- [PHPUnit test example](Examples/TestsClass.md) - Read when a larger document needs to combine examples with testing philosophy, shared setup, and assertion guidance
- [Reading context sections](../../Blocks/ReadingContext/ReadingContext.md) - Read when adding or editing MUST read or MAY read sections

## CodeDoc.format.md typical use context

### 💡 Distinct usage patterns for CodeDoc.format.md

#### Direct reference when creating new code file type documentation

```markdown
Create CodeDoc document for Repository classes following [CodeDoc format](CodeDoc.format.md)
```

#### Loaded via BuildDoc workflow for code documentation

User requests code documentation creation -> BuildDoc workflow loads format specification -> CodeDoc.format.md guides document structure

### Role CodeDoc.format.md serves during use

- Template and rules for creating consistent code file type documentation
- Ensures each file type document follows the same structure
- Bridge between AiDocFormatDoc meta-format and practical code guidance documents
