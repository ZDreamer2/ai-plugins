# Refine Documentation Workflow

## Overview

Refine user edits into clear, concise, consistent documentation while preserving their intended meaning, organization, and communicative role.

### Input

- Target AiDoc and relevant git changes, uncommitted or identified by a commit or range
- Optional: User explanations of the intended changes

### Output

- Refined AiDoc and directly affected meta guidance or references aligned with the edits
- Brief report of meaningful calls, unresolved questions, and concerns beyond refinement

## Workflow

### Step 1: Understand the intended changes

Read the complete current document and the relevant git diff, including deletions. Use the changes identified by the user; otherwise, use the target's staged and unstaged changes against HEAD. If the intended comparison cannot be determined from context, ask before relying on it.

Read the target's AiDocMetaDoc if present and relevant formatting or editing context it references. A missing meta does not block refinement. Consult related documentation as needed to understand changed references or shared concepts.

Treat the user's edits and explanations as the intended direction, including removals and relaxed requirements. The previous version and meta provide context that may now be outdated; disagreement with them alone is not an error. Identify contradictions or unclear intent without silently restoring earlier decisions.

### Step 2: Resolve unclear intent

Assess the edits together using the gathered context. Apply clear corrections and well-supported interpretations without approval. Reserve questions for unresolved intent where plausible readings would produce materially different documentation; a concern about the user's design alone does not block refinement.

If clarification is needed, group independent questions into one exchange. Prefer ${AGENT_QUESTION_TOOL} when available to present the choices. For each, identify the passage and ambiguity, offer concise plausible readings, and put your recommended reading first with a brief reason. Ask for the missing intent, not approval of an editing plan. Resolve answers before applying dependent changes; if no clarification is needed, proceed directly.

Keep nonblocking structural problems and independent design proposals for the finish report. Preserve intended edits even when you would have made a different design choice.

### Step 3: Refine the edits and their consequences

- Improve wording in edited passages while preserving meaning, requirement strength, and the document's organization. Keep definitions, descriptions, specifications, and instructions in their intended roles; making declarative content actionable can introduce new responsibilities.
- Make the smallest local change that expresses the intended meaning clearly. Split sentences or adjust adjacent wording when useful. Keep the level of detail and roughly the same length or shorter; additions need a concrete clarity or consistency purpose.
- Repair clear consequences elsewhere, such as stale step references, inconsistent terminology, and directly affected meta guidance. Align outdated meta with the user's intended changes while preserving its role as editing context. Keep related edits tied to these consequences.

Retain meaningful interpretive calls and concerns for the finish report without implementing an independent redesign. If new uncertainty requires user intent, inspect the remaining affected content to consolidate further questions, then return to Step 2 before applying dependent changes.

### Step 4: Validate the result

Read the complete revised document and inspect your own changes against its pre-refinement state. Check that:

- The user's intended changes survive, including deletions and simplifications.
- The document is coherent, with directly affected references and meta aligned.
- Refinement preserves statement types and introduces no unintended responsibilities, requirements, detail, or restructuring.

Correct issues within scope. Return to Step 2 if unresolved intent affects correctness; keep concerns requiring broader changes for the finish report.

### Step 5: Report meaningful calls and concerns

Briefly state what changed, including related files. Report interpretive calls worth reviewing and concerns beyond refinement scope, with a concise recommendation where useful. Identify any unresolved questions and passages left unchanged because of them. Omit empty categories and routine grammar details.

The report supports review and further discussion; completed refinements need no general approval gate. Questions needed to determine the meaning of applied changes belong in Step 2, not in this report.
