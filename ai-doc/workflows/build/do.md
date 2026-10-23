# BuildDoc Workflow Documentation

## Overview

Transforms a request into a new or improved AiDoc by leveraging its corresponding AiDocMetaDoc for context and requirements.

### Input
- Target AiDoc path to create or improve
- Optional: User considerations about AiDoc, what to add/improve

### Output
- New or improved AiDoc that complies with its AiDocMetaDoc specifications and format requirements

## Workflow

### Step 1: Gather context

Review foundational documents:
- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Use its definitions and meta-document naming convention
- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Apply its directive language, formatting, and conciseness rules

Substeps MUST be executed sequentially due to path dependencies.

Read files in this specific order to build context from general to specific:

#### 1.1: Read AiDocMetaDoc

Based on provided AiDoc path, locate and read its AiDocMetaDoc:
- Check for meta file using AiDocMetaDoc naming convention from [AiDoc terminology](../../Theory/AiDocTerminology.md#aidocmetadoc-files)
- IF AiDocMetaDoc does not exist THEN
	- Exit workflow - AiDocMetaDoc is required
- IF AiDocMetaDoc exists THEN
	- Understand its goals, principles, and requirements
	- Meta docs may use `AI_DOC_PLUGIN` in references — resolve its suffix from the ai-doc plugin root (`../../` relative to this workflow), then read the resolved absolute path
	- Extract AiDocFormat path from `## AiDocFormat` section

#### 1.2: Read AiDocFormatDoc

- Read the AiDocFormatDoc from path extracted in step 1.1
- Understand format structure, template, and validation rules

#### 1.3: Read format foundation documents

- Read all documents from "MUST read before planning" section of the AiDocFormatDoc
- Check "SHOULD read" sections of the AiDocFormatDoc and read those that apply to the current situation

#### 1.4: Read AiDoc-specific requirements

- IF AiDocMetaDoc contains "MUST read before editing" section THEN
	- Read all documents listed in that section
	- These provide AiDoc-specific context and requirements

#### 1.5: Read additional context

- Consider reading documents from AiDocMetaDoc "MAY read for additional context" section
- Trust your judgment about what additional context might help

### Step 2: Analyze and clarify

Ensure all context from Step 1 is gathered BEFORE this step — incomplete context leads to flawed analysis.

- Analyze complexity, structure, and requirements based on gathered context
- IF ambiguities, missing information, or assumptions need validation THEN
	- Clarify with user before proceeding
	- Consider ${AGENT_QUESTION_TOOL} for structured clarification

### Step 3: Plan and execute

- Create or improve AiDoc based on analysis
- Write document references as Markdown links following [reference path rules](../../Theory/References/ReferencePathManagement.md); required reading is carried by the section or sentence

### Step 4: Validate

Run each check sequentially in a separate inference:

- Verify against AiDocFormat specified in AiDocMetaDoc using its Validation Rules section
- Verify all AiDocMetaDoc goals and principles are met
- Evaluate if AiDocMetaDoc needs updating to reflect changes made to AiDoc
- Follow the [final documentation review](workflows/on-build-done.md) and apply any relevant considerations

## Key Principles

- AiDocMetaDoc is ALWAYS required - this workflow cannot proceed without it
- Do not duplicate general formatting rules - reference format documents
- Focus on the specific purpose and context defined in AiDocMetaDoc
- The AiDocMetaDoc defines success criteria for the AiDoc
