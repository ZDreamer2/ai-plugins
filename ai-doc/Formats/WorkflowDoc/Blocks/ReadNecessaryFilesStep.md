# ReadNecessaryFilesStep Block Format

## Template

```markdown
### Step [N]: Read necessary files

[intro] (optional)

[reading content]
```

Or with substeps for complex reading logic:

```markdown
### Step [N]: Read necessary files

[intro] (optional)

#### [N.N]: Read [specific target]

[reading content]

#### [N.N]: Determine [what to read]

[path deduction logic]
[conditional reading]
```

## Template Notes

### [intro]

Optional introduction explaining what will be read, why, or noting dependencies between substeps.

### [substep title]

Action-oriented title pattern: "[Action verb] [specific target]"

Recommended patterns:
- "Read [specific file/type]" - Direct reading action
- "[N.N]: Read [specific target]" - Numbered when order matters
- "Determine [what to read]" - Path deduction logic
- "Check [condition]" - Conditional branching

Examples:
- "Read AiDocMetaDoc"
- "1.1: Read core specifications"
- "Determine AiDocFormat path"
- "Check existing files"

### [reading content]

Specifies WHAT to read and HOW to determine paths:

- Direct file references: `[DocumentName](path/to/file.md) - brief purpose`
- Path deduction: Rules for deriving file paths from context
- Conditional loading: `IF condition THEN read file/follow logic`
- Sequential dependencies: Explicit execution order
- State branching: Different paths based on workflow state

## Example

Demonstrates action-oriented substep titles and clear structure:

```markdown
### Step 1: Read necessary files

Substeps MUST be executed sequentially due to path dependencies.

#### 1.1: Determine editing context

- Locate the target's AiDocMetaDoc using the [naming convention](../../../Theory/AiDocTerminology.md#aidocmetadoc-files).
- IF a meta exists THEN read it and extract the format path from its `## AiDocFormat` section.
- Otherwise, obtain the AiDocFormatDoc path specified in the target or supplied by the user when requesting work without a meta.

#### 1.2: Read AiDocFormatDoc

- Read the AiDocFormatDoc from path extracted in step 1.1
- Understand format structure, template, and validation rules

#### 1.3: Read format requirements

- IF AiDocFormatDoc contains "MUST read before planning" section THEN
	- Read all documents listed in that section
```

Adapted from the [AiDoc creation workflow](../../../workflows/build/do.md). See also the [AiDocMetaDoc context-gathering steps](../../../workflows/meta/do.md#step-1-establish-the-intended-document) for complex conditional logic.

## Validation Rules

- Main step title MUST be "Step [N]: Read necessary files"
- Substep titles MUST use action-oriented pattern: "[Action verb] [specific target]"
- File purposes MUST be 5-10 words maximum
- Dependencies between file reads MUST be explicit (sequential order or IF/THEN logic)
- State conditions MUST be clear when using conditional loading
- Path deduction logic MUST specify transformation rules
- Direct file references MUST use Markdown links
