# AiDocMetaDoc Format Specification

## What is document in AiDocMetaDoc format

An AiDocMetaDoc explains what its target document contributes, who relies on it and why its important boundaries exist. It gives future editors the context needed to preserve that purpose as the document changes. It can precede the target and remains useful during later editing.

AiDocMetaDocs are ONLY loaded during AiDoc creation or editing, NEVER during normal use of the target. They describe the target's role and the reasons behind its constraints; the target owns its instructions, structure and operational decisions. This preserves intent without freezing the current contents or turning the meta into a procedure for the editor.

Useful context includes audience assumptions, relationships to other documents and rationale a future editor could not recover from the target alone. Existing sources remain authoritative for domain knowledge and mechanics. Limited overlap can help explain a boundary; recording every current decision adds no protection against losing the underlying purpose.

## MUST read before planning AiDocMetaDoc document

- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its directive language, formatting, and conciseness rules
- [Typical use context block](Blocks/TypicalUseContext.md) - Distinguish direct and indirect loading when writing the distinct usage patterns subsection

## AiDocMetaDoc template

```markdown
# [AiDocName].meta.md

Specification for creating and editing [AiDocName](path/to/AiDoc.md). Defines purpose, usage patterns, and constraints.

## [AiDocName].md goals and principles

- [What the target enables for its reader]
- [Key principle or constraint]
- [Additional principles as needed]

## AiDocFormat

[FormatName](path/to/format.format.md)

## MUST read before editing [AiDocName].md

- [Subject or role](path/to/document.md) - [what editing context this source contributes and why it matters] (one or more)

## MAY read for additional context before editing [AiDocName].md (optional)

- [Subject or role](path/to/document.md) - [when is this relevant for editing target AiDoc] (one or more)

## [AiDocName].md typical use context

[TypicalUseContext.md: distinct usage patterns subsection]

### Role [AiDocName].md serves during use

- [Primary function during practical tasks]
- [Additional roles as needed]

## [AiDocName].md underlying theory (optional)

[Essential theoretical context necessary for AiDoc creation but too complex for the practical guide]
```

## Template Notes

### "[AiDocName].md goals and principles" section

Describe the target's purpose and responsibilities, with the target as the subject: "Preserves the rationale future maintainers need," rather than "Preserve the rationale," which instructs the editor. Goals explain what makes the document useful; important constraints include the reasons they matter.

The test is whether this context helps an editor recognize what a plausible rewrite could lose that matters. Current wording, steps or file layout are not enduring goals merely because they already exist.

### "MUST read before editing [AiDocName].md" section

- Documents required during creation and every editing session — without them, edits risk being incorrect
- List only AiDoc-specific context documents
- Format specification from AiDocFormat section is already required
- Descriptions explain the source's contribution to editing this target and why it matters, beyond repeating its title
- The source owns the knowledge; its description explains the relevance rather than copying that knowledge or assigning generic editing actions
- New AiDocMetaDocs MUST link to the [StartSimple methodology](../../Theory/StartSimple.md) in this section. Outside ai-doc, use `[StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md)`; inside ai-doc, use a document-relative destination, following the path rules below

### "MAY read for additional context before editing [AiDocName].md" section

- Documents relevant only in specific editing scenarios — reader decides based on current task
- Descriptions answer "when is this relevant" - enable reader to decide if needed for current task

### Path references in meta docs

Use Markdown links in the specification statement, AiDocFormat section, and required or optional reading lists. Templates use `Subject or role` and `path/to/document.md` as placeholders for the label and destination.

Follow [reference path rules](../../Theory/References/ReferencePathManagement.md) for destination prefixes. Use the same syntax in all reading sections; their headings establish the obligation. Meta documents MUST NOT use `@` for auto-loading.

## AiDocMetaDoc example

Example meta document in `src/Core/Domain/Repository/Docs/Build/`:

```markdown
# Build.meta.md

Specification for creating and editing [BuildRepository.md](BuildRepository.md). Defines purpose, usage patterns, and constraints.

## BuildRepository.md goals and principles

- Enables rapid creation of basic Repository implementations with standard patterns
- Keeps basic repository creation self-contained so common tasks do not require unrelated specialization context
- Connects specialized cases to their owning guides, keeping those details out of the common path

## AiDocFormat

[CodeDoc format](AI_DOC_PLUGIN/Formats/CodeDoc/CodeDoc.format.md)

## MUST read before editing BuildRepository.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Explains the focus on established repository-building needs
- [Entity documentation](../../../Entity/Docs/Entity.md) - Owns the entity model this guide assumes; that boundary keeps repository guidance focused on persistence

## MAY read for additional context before editing BuildRepository.md

- `src/Core/Domain/Repository/Repository.php` - Defines the base architecture; relevant when its assumptions change
- `src/Modules/Analytics/Domain/Report/Report/ReportRepository.php` - Provides plugin-specific behavior when that guidance changes
- `src/Domain/Redmine/Issue/IssueRepository.php` - Provides retrieval-event behavior when that section changes
- `src/Modules/Analytics/Domain/DataQuery/DataQueryRepository.php` - Provides persistence-event behavior when that section changes

## BuildRepository.md typical use context

### 💡 Distinct usage patterns for BuildRepository.md

#### Loaded indirectly via workflow when building entity classes

Entity-building workflow selects repository creation -> loads this guide with the entity context already available.

#### Direct reference for repository modifications

`Edit src/Modules/Analytics/Domain/Report/Report/ReportRepository.php using the repository creation guide.`

### Role BuildRepository.md serves during use

- Primary guide enabling immediate repository code generation for basic cases
- Decision tree for when to consult specialized documentation
- Bridge between Entity theory and practical Repository implementation
```

## Validation Rules

- MUST comply with [AiDoc writing principles](../../Theory/AiDocBaseFormat.md)
- MUST open with clear specification statement
- MUST describe the target's purpose and responsibilities in the goals section, rather than give instructions to its editor
- MUST include AiDocFormat section with path to format specification
- MUST explain what required sources contribute to editing the target and why they matter
- MUST include typical use context section with both subsections
- MUST clearly state role during use
- MUST NOT duplicate general documentation standards
- MUST provide context that helps an editor judge whether a rewrite preserves the target's purpose and important boundaries, without freezing its current contents
- MUST distinguish settled authoring constraints from unresolved choices when recording them
- SHOULD leave document-level decisions and detailed guidance to the target; overlap is justified by explanatory value, not completeness
- MUST use Markdown links for document references, with required or optional reading expressed by the section or sentence
- SHOULD include underlying theory ONLY if necessary
