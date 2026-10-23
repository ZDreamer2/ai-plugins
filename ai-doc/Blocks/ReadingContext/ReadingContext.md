# Reading Context Block for Format Documents

Guides adding file reference sections to AiDocFormatDoc documents. Used in two scenarios:
- MUST read sections - required references, always needed when document is loaded
- MAY read sections - optional references, useful for some tasks but not all

## Context

User provides ReadingSectionName and ReadingSectionFrame for the new section.

You add content to these FormatDoc locations:
- Template - the markdown structure
- Template Notes - explanations for placeholders
- Validation Rules - compliance rules

And to FormatDoc's meta file (separate file with editing context).

## Definitions

### ReadingSectionName

The section header name. Examples: "MUST read before planning", "MAY read for additional context", "Relevant code files".

### ReadingSectionFrame

Framing question that descriptions should answer. Determines what each file's description communicates:
- Actionable frame -> MUST read pattern (e.g., "how to use this file")
- Relevance frame -> MAY read pattern (e.g., "when is this file useful")

## Template addition

```markdown
## [ReadingSectionName] (optional)

- [Subject or role](path/to/document.md) - [ReadingSectionFrame] (one or more)
```

Use document-relative paths for Markdown references. For project code files, use backticked paths from the project root.

## Template Notes addition

Add section explanation if needed - when to include this section, what files to focus on.

The link label identifies the target's subject or role in context.
The description answers ReadingSectionFrame, adding information beyond the label.

Add entry-level template notes only when the section's framing question needs explanation.

## Validation Rules addition

Add rule ensuring descriptions answer the ReadingSectionFrame:

```markdown
- [ReadingSectionName] file descriptions MUST answer "[ReadingSectionFrame]" with section-specific guidance.
```

## Meta file addition

Add a reference to this block in the FormatDoc's meta file MAY read section:

```markdown
- [Reading context sections](AI_DOC_PLUGIN/Blocks/ReadingContext/ReadingContext.md) - Read when adding or editing "[ReadingSectionName]" section
```

Inside ai-doc, use a document-relative destination instead.

## Example

User provides:
- ReadingSectionName: "Relevant code files"
- ReadingSectionFrame: "role in the issue"

Template addition:
```markdown
## Relevant code files (optional)

- `path/to/code-file.php` - [role in the issue] (one or more)
```

Template Notes addition:
```markdown
### "Relevant code files" section

Code files directly relevant to understanding or implementing the issue. Optional - include when issue touches specific known parts of codebase.
```

Validation Rules addition:
```markdown
- "Relevant code files" descriptions MUST answer "role in the issue" with issue-specific guidance.
```

Meta file addition (for a format outside ai-doc):
```markdown
- [Reading context sections](AI_DOC_PLUGIN/Blocks/ReadingContext/ReadingContext.md) - Read when adding or editing "Relevant code files" section
```
