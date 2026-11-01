# Reference Path Management

Rules for authoring and following document references in the ai-doc system. Covers link destinations, labels, and reading obligations. Executable paths and host-specific expansion belong to runtime and packaging guidance.

## Reference paths

### Within the same project or plugin

Use paths relative to the directory containing the referencing document by default. This applies to skills, workflows, supporting documents, formats, and meta documents. A meta document uses its own directory as the base.

For example, from `skills/ai-doc/SKILL.md`, write `[AiDoc terminology](../../Theory/AiDocTerminology.md)`. From a document in `Theory/`, write `[AiDoc terminology](AiDocTerminology.md)`.

### Project code files

References to code files in the same project use paths from the project root, such as `src/Core/Domain/Repository/Repository.php`, regardless of the referencing document's directory. References to Markdown documents in the project follow the document-relative default.

### Directory references

Use backticked paths relative to the containing document for directory references. Literal checkout paths in build commands, configuration, or examples retain the base required by that context.

### Marketplace source meta documents

Meta documents used to edit marketplace sources may reference files across the entire marketplace repository, including sibling plugins. Their scope is the source repository, not an installed plugin.

Use document-relative Markdown links for documents and document-relative paths for directories. Code and other non-Markdown file references within the marketplace use paths from its repository root, such as `pm/rm/scripts/load_issue.py` or `@common/scripts/do.py`. References outside the marketplace retain the owning project's path convention. The ai-doc prefix convention below still applies.

### Editing-only references to ai-doc

MUST use `AI_DOC_PLUGIN/...` for references to ai-doc content from meta documents or `edit-only-context` properties in a project or another plugin. For example: `[CodeDoc format](AI_DOC_PLUGIN/Formats/CodeDoc/CodeDoc.format.md)` in a meta.

Ai-doc editing workflows resolve this prefix to the ai-doc plugin root, as defined in [AiDoc terminology](../AiDocTerminology.md#plugin-reference-convention). It is a resolver convention, not a filesystem directory. Inside ai-doc, use document-relative paths instead.

### Other cross-boundary references

Bundled dependencies of documents used from installed plugins stay within that plugin, including its shared content. Direct references into another plugin's installation or a particular project's checkout are unsupported. The source-meta and ai-doc prefix conventions above are separate editing-time cases.

## Reference syntax

Use `[label](destination)` for references to Markdown documents and backticks for references to other files. Choose the path using the rules above. The [editing-only frontmatter reference](../AiDocTerminology.md#aidocformatdoc-files) uses a YAML string path instead of Markdown link syntax.

- Choose a concise label that identifies the target's subject or role in the current context. Use wording that helps the reader understand what the reference contributes. A document title is often sufficient; use a filename when the file's identity matters. Apply this guidance when revising existing Markdown links too.
- Keep Markdown link destinations out of backticks. Use backticks for literal filenames, paths, commands, and syntax examples, including Markdown filenames being discussed rather than referenced for reading.
- Apply these syntax rules in required and optional reading sections, including `## AiDocFormat` and all meta files.

## Reading obligations

The section or sentence states when to read a referenced file:

- `## MUST read before editing`, `## MUST read before planning`, and a meta document's `## AiDocFormat` require reading.
- `## MAY read for additional context` makes reading optional.
- In body prose, use an explicit instruction such as "Read X before planning" or optional wording such as "See also X".
- A reference in an `IF ... THEN` branch is required only when that condition applies.

Reference syntax neither loads the target nor establishes a reading obligation by itself.

## Path resolution when reading

Retain the containing document's full path alongside its content. Resolve paths using the bases defined above, regardless of the shell working directory or previously read documents.

Pass the resolved full path to file tools. Link syntax alone does not perform this resolution.

## Explicit reading instead of context injection

MUST NOT use `@path` context injection, including in `SKILL.md` files and their supporting documents. Repeated skill use can inject the same documents again, consuming context even when their content is already available.

Use the reference syntax above and state reading obligations in the section or sentence. Read referenced context explicitly when needed; reuse content already available in the session when it is sufficient and current. MUST NOT use `@` to mark required reading or prepend it to reference paths, including `AI_DOC_PLUGIN` references.
