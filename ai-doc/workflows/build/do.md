# BuildDoc Workflow Documentation

## Overview

Create or improve an AiDoc using its authoring context and format requirements.

### Input
- Target AiDoc path to create or improve
- Optional: User considerations about AiDoc, what to add/improve

### Output
- New or improved AiDoc that complies with its format and any AiDocMetaDoc context

## Workflow

### Step 1: Gather context

Review foundational documents:
- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Use its definitions and meta-document naming convention
- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its directive language, formatting, and conciseness rules

Substeps MUST be executed sequentially due to path dependencies.

Read files in this specific order to build context from general to specific:

#### 1.1: Determine editing context

Read the target if it exists and locate its AiDocMetaDoc using the [naming convention](../../Theory/AiDocTerminology.md#aidocmetadoc-files).

- IF AiDocMetaDoc exists THEN read it, understand its goals and constraints, and extract the format reference from `## AiDocFormat`.
- Otherwise, use the AiDocFormatDoc specified in the target or supplied by the user when requesting work without a meta. Ask for the format location if needed.
- IF neither a meta nor a format is specified THEN stop and request the missing input.

Resolve references using the [reference path rules](../../Theory/References/ReferencePathManagement.md). Resolve `AI_DOC_PLUGIN/...` from this plugin's root (`../../` relative to this workflow); other document paths are relative to their containing document. Resolve a format supplied in the request from the location the user specifies.

#### 1.2: Read AiDocFormatDoc

- Read the AiDocFormatDoc determined in step 1.1
- Understand format structure, template, and validation rules

#### 1.3: Read format foundation documents

- Read all documents from "MUST read before planning" section of the AiDocFormatDoc
- Read applicable "SHOULD read" and relevant optional context from the AiDocFormatDoc

#### 1.4: Read AiDoc-specific requirements

- IF an AiDocMetaDoc exists and contains "MUST read before editing" section THEN
	- Read all documents listed in that section
	- These provide AiDoc-specific context and requirements

#### 1.5: Read additional context

- When a meta exists, consider reading documents from its "MAY read for additional context" section
- Trust your judgment about what additional context might help

### Step 2: Analyze and clarify

Ensure all context from Step 1 is gathered BEFORE this step — incomplete context leads to flawed analysis.

- Analyze complexity, structure, and requirements based on gathered context
- IF ambiguities, missing information, or assumptions need validation THEN
	- Clarify with user before proceeding
	- Consider ${AGENT_QUESTION_TOOL} for structured clarification

### Step 3: Plan and execute

- Create or improve AiDoc based on analysis
- For a target without a meta, record its format in `edit-only-context`, preserving other frontmatter fields
- Write document references as Markdown links following [reference path rules](../../Theory/References/ReferencePathManagement.md); required reading is carried by the section or sentence

### Step 4: Validate

Run each check sequentially in a separate inference:

- Verify against the selected AiDocFormat using its Validation Rules section
- When a meta exists, verify its goals and principles are met and evaluate whether its editing context needs updating
- Verify document references resolve
- Follow the [final documentation review](workflows/on-build-done.md) and apply any relevant considerations

## Key Principles

- Do not duplicate general formatting rules - reference format documents
- Preserve the document's purpose using the request, target and available editing context
