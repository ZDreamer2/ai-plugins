# BuildDocMeta Workflow Documentation

## Overview

Create or improve an AiDocMetaDoc with the additional context needed to create or edit its target reliably.

### Input

- Target AiDoc path; the target may be absent, empty or already written
- User's intent, requirements and relevant dialogue context

### Output

- New or improved AiDocMetaDoc following the [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md)

## Workflow

### Step 1: Establish the intended document

Reuse sufficient, current context already available; read what is missing.

- Read [AiDoc terminology](../../Theory/AiDocTerminology.md), [writing principles](../../Theory/AiDocBaseFormat.md) and the [AiDocMetaDoc format](../../Formats/MetaDoc/AiDocMetaDoc.format.md), including its required context.
- Locate the target and its meta using the naming convention. Read each that exists. An absent or empty target is normal: establish its purpose from the request and surrounding documentation instead.
- Establish what the target enables, who relies on it and why its boundaries matter before selecting its format or drafting sections. Consider what a plausible rewrite could lose that matters, and what context would help a future editor judge that change. Read the surrounding entry points and contracts needed to answer this for the particular target.
- For an existing meta, read its required editing references and relevant optional references. Resolve `AI_DOC_PLUGIN/...` from this plugin's root before reading; other document references are relative to their containing document.

Choose and read the target's AiDocFormatDoc. Use the user's explicit format when supplied; otherwise retain the format specified in the existing meta or target. If no format is recorded, select by the target's role:

- `SKILL.md`: [SKILL format](../../Formats/SkillDoc/SKILL.format.md); add [WorkflowDoc](../../Formats/WorkflowDoc/WorkflowDoc.format.md) when it also contains a procedure.
- Step-by-step procedure: [WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md).
- Code guidance: [CodeDoc format](../../Formats/CodeDoc/CodeDoc.format.md).
- Format specification: [AiDocFormatDoc format](../../Formats/FormatDoc/AiDocFormatDoc.format.md).
- Otherwise: [BaseDoc format](../../Formats/BaseDoc/BaseDoc.format.md).

Resolve a named custom format in the project; ask for its location if it cannot be found.

Read specialized guidance only IF the user mentions the corresponding term:

- HubDoc: [HubDoc guidance](../../Formats/MetaDoc/HubDocMeta.md).
- ChildDoc: [ChildDoc guidance](../../Formats/MetaDoc/ChildDocMeta.md).
- StartSimple: [StartSimple methodology](../../Theory/StartSimple.md).
- WriteFinal: [WriteFinal principles](../../Theory/WriteFinal.md).

### Step 2: Identify additional authoring context

Identify the overall intent, usage context and important constraints that help an author beyond what the target and existing sources provide. For an absent target, distinguish this context from the content and decisions the future document should own.

Apply the [meta's content boundary](../../Formats/MetaDoc/AiDocMetaDoc.format.md#what-is-document-in-aidocmetadoc-format):

- Keep intent, rationale and constraints when they add value to future authorship.
- Reference existing authorities for domain knowledge and mechanics.
- Leave the actual content, including workflow steps, to the target. Include overlap only when it helps explain the context, not to retain every decision from the dialogue.

Ask when an unresolved choice materially affects the target's purpose, scope or constraints and cannot be settled from the available context. Continue independent work while that question is pending.

### Step 3: Write the meta

Create or revise the meta as a complement to the target, giving its author the context needed to make good editing decisions. Follow the format's structure and [reference rules](../../Formats/MetaDoc/AiDocMetaDoc.format.md#path-references-in-meta-docs). Keep required reading limited to context needed for every authoring session; make conditional references optional.

When adding a meta to a format-only target, record its format in the meta and remove the target's `edit-only-context` property, preserving other frontmatter fields.

### Step 4: Reread and validate

Reread the resulting meta after writing it. For an existing target, consider the two documents together; for a new target, assess whether the meta orients its author while leaving document-level decisions open to authorship.

- Check the [format's validation rules](../../Formats/MetaDoc/AiDocMetaDoc.format.md#validation-rules) and resolve the references. The planned target may not exist yet; required source references should resolve to available context.
- Assess the result against the [goals and principles criterion](../../Formats/MetaDoc/AiDocMetaDoc.format.md#aidocnamemd-goals-and-principles-section): what useful editing context does each passage add beyond the target and required sources? An absent target is not a reason to store its prospective contents in the meta.
- Remove passages whose only purpose is to retain document-level decisions. Keep limited overlap when it improves explanation, and check that recorded constraints agree with the referenced contracts.
- Apply the [shared editorial criteria](../build/workflows/on-build-done.md). Reread any revised passages before finishing.
