# AiDoc Documentation Guide

Welcome to AiDoc — a system for writing documentation that AI agents actually use well. This guide helps you create, improve, and manage AiDocs through a structured workflow with AI assistance.

## The Documentation System

The framework uses three document layers:

**AiDocFormatDoc** (`.format.md`) — Format blueprints. Defines HOW to write a type of document: template, structure rules, validation. Formats already exist for common types — you rarely need to create new ones.

**AiDocMetaDoc** (`.meta.md`) — Additional authoring context: purpose, constraints, required reading, and usage patterns. Optional when the format and task provide enough context.

**AiDoc** (`.md`) — The actual document AI agents read during tasks. Concise, actionable, optimized for the chosen format.

### Why this separation?

Without it, you either re-explain a document's purpose every editing session, or pollute the working doc with meta-information that confuses agents during normal use. The AiDocMetaDoc preserves editing context between sessions without bloating the AiDoc itself.

### Available Formats

**BaseDoc** — General documentation with clear structure.

**CodeDoc** — Code patterns with comprehensive examples and inline comments. Use when the document is primarily about how to write code.

**WorkflowDoc** — Multi-step procedures with context gathering and verification.

**SkillDoc** — Agent skill definitions (SKILL.md files). Skills containing a procedure also use WorkflowDoc.

**FormatDoc** — Format specifications that define AiDocFormat structure and rules. You'll rarely need this unless creating a new document format.

**HumanDoc** — Human-facing guides like this one. Conversational tone, emojis, visual aids.

---

## 🔄 Overall Workflow

A typical documentation workflow:

1. **Define** → `${AGENT_SKILL(ai-doc)} meta` captures additional authoring context when useful
2. **Build** → `${AGENT_SKILL(ai-doc)} build` creates or improves the AiDoc using its format and any meta
3. **Test** → `${AGENT_SKILL(ai-doc)} debug` reflects on documentation quality after real use
4. **Iterate** → `${AGENT_SKILL(ai-doc)} build` again to improve based on findings

Everything runs through `${AGENT_SKILL(ai-doc)}`, followed by what you want: `meta`, `build`, `refine`, `compact`, `stress-test`, `debug`, or `move`.

---

## 📋 `${AGENT_SKILL(ai-doc)} meta` — Define What You Want

Creates or improves an **AiDocMetaDoc** — additional context that helps future authors preserve your document's purpose and important boundaries.

**When to use:**
- Creating document-specific editing context before building an AiDoc
- Adding a meta to an existing document

**Example prompt:**

```
${AGENT_SKILL(ai-doc)} meta Create meta file for docs/Code/Core/Ai/Mcp/McpTests.md with these considerations:
- It describes how to write proper MCP test classes
- Has CodeDoc format
- tests/Services/Ai/Mcp/Redmine/RedmineMcpServerSchemaTest.php is a good example
```

**What you get:**

An AiDocMetaDoc (`.meta.md`) with:
- **Goals and principles** — what the document achieves
- **AiDocFormat** — which format blueprint to follow
- **MUST read / MAY read** — required and optional context for editing
- **Typical use context** — how the document gets loaded and used

### What to mention in your prompt

Your considerations directly shape every section of the generated meta file. Here's what drives the best results:

**Purpose and constraints** — Always the most useful starting point. What should this doc achieve? "Describes how to write proper MCP test classes", "Guides entity migration step-by-step", etc.

**Usage patterns** — Always valuable. How will this doc be loaded?
- Directly: "User loads when writing repository code"
- Indirectly: "Called from BuildMcp workflow step 2, not used directly"
- This shapes the "typical use context" section, which helps future editing sessions understand how the doc is actually consumed.

**Format** — Specify it when you want a particular format, especially HumanDoc or a custom project format. Otherwise, the meta workflow retains the existing format or selects one based on the document's role.

**Special terms** — Mention any of these named terms to trigger specialized reading by the meta-building skill:
- HubDoc — loads [HubDoc meta-document guidance](Formats/MetaDoc/HubDocMeta.md), adds structural guidance for entry-point/routing docs
- ChildDoc — loads [ChildDoc meta-document guidance](Formats/MetaDoc/ChildDocMeta.md), adds guidance for docs extending another doc
- HubSkill — loads the [HubSkill format](Formats/SkillDoc/Types/HubSkill.format.md) alongside SKILL for a skill that dispatches to multiple handlers
- StartSimple — loads the [StartSimple methodology](Theory/StartSimple.md), adds the methodology of minimal initial content expanded only when real usage reveals gaps
- WriteFinal — loads [WriteFinal principles](Theory/WriteFinal.md), guides referencing during ecosystem build-out: treat planned stubs as if they exist, skip transitional docs that will be absorbed

**Relations to other documents** — Mention how the doc relates to other documents in the project. These become MUST read / MAY read entries with actionable descriptions. Common patterns from the project:
- Boundaries: "Should not duplicate content from TestsClass.md"
- Source of knowledge: "Use McpCode.md as main source" or "Extract patterns from X.md"
- Methodology: "Follow StartSimple.md approach"
- Terminology: "Must use terminology consistently with AiDocTerminology.md"
- Examples: "RedmineMcpServerSchemaTest.php is a good example of MCP tests"
- Predecessor: "Replaces outdated HowToWriteDocs.md"
- Hub-spoke: "Primary entry point that routes to A.md, B.md, C.md"
- Extension: "Extends X.md with [specific aspect]"

---

## 🔨 `${AGENT_SKILL(ai-doc)} build` — Create or Improve Documentation

Creates or improves an AiDoc using its AiDocFormatDoc and, when present, its AiDocMetaDoc.

**When to use:**
- After AiDocMetaDoc exists and you're ready to write the AiDoc
- When an existing AiDoc needs improvements

AI uses the document's available editing context and your request. If neither specifies a format, it asks you to choose one.

**Example prompts:**

Create new:
```
${AGENT_SKILL(ai-doc)} build Create docs/Code/Core/Ai/Mcp/McpTests.md
- Let's use docs/Code/Core/Ai/Mcp/McpCode.md as main source of knowledge
- We want to move all test related knowledge from there
```

Improve existing:
```
${AGENT_SKILL(ai-doc)} build Improve docs/Feature/MyFeature.md
- The examples section needs updating for the new API
```

Create without a meta:
```
${AGENT_SKILL(ai-doc)} build Create docs/Code/McpTests.md without a meta
- Follow AI_DOC_PLUGIN/Formats/CodeDoc/CodeDoc.format.md
- Describe the MCP test patterns in tests/Services/Ai/Mcp/
```

Without a companion or referenced meta, AI records the format in the document's `edit-only-context` frontmatter.

---

## ✏️ `${AGENT_SKILL(ai-doc)} refine` — Refine Your Edits

After you edit a document, AI improves the wording and repairs related inconsistencies while preserving your intended meaning, organization, and level of detail. Definitions, descriptions, specifications, and instructions keep their roles.

**When to use:**

- You have made the substantive edits and want clearer language
- Your edits may have left stale references or conflicting statements elsewhere

**Example prompt:**

```text
${AGENT_SKILL(ai-doc)} refine docs/Feature/MyFeature.md
```

Use the edited document's path. This works in a fresh session: AI reads the document and its git diff. By default, it uses staged and unstaged changes against HEAD; specify a commit or range when those are the edits you want refined. Add an explanation when the reason for a change would help AI interpret it. An AiDocMetaDoc is useful but not required.

**How it works:**

1. AI reads your edits and the relevant context. If materially different meanings remain plausible, it groups clarification questions and offers alternatives with a recommendation.
2. AI refines the text and aligns directly affected references and meta guidance. Your intended changes, including deletions and simplifications, guide the edit.
3. You receive the revised files and a brief report of meaningful interpretations and concerns beyond refinement, such as a proposed structural change.

Review the reported calls to check that AI understood your intent. This is the first version of the workflow; feedback from actual use will shape it.

---

## 📉 `${AGENT_SKILL(ai-doc)} compact` — Reduce Reading Effort

Improves an entire document's usefulness and reading cost while preserving what its intended reader needs. Unlike `refine`, it can reconsider organization and move detail into satellites when that improves combined reading and navigation effort.

**When to use:**

- A document has become repetitive or costly to read
- Specialized detail obscures the main guidance

**Example prompt:**

```text
${AGENT_SKILL(ai-doc)} compact docs/Feature/MyFeature.md
- Keep the common case self-contained
```

---

## 🧪 `${AGENT_SKILL(ai-doc)} stress-test` — Challenge Uncommitted Changes

Critically reviews the AiDoc changes sitting in your working copy — whoever made them, you or AI — and applies the improvements it can justify.

**When to use:**

- After `${AGENT_SKILL(ai-doc)} build` or a batch of edits, before you commit
- Several documents changed together and you want their boundaries and repetition checked

**Example prompts:**

Review everything uncommitted:
```text
${AGENT_SKILL(ai-doc)} stress-test
```

Narrow the scope:
```text
${AGENT_SKILL(ai-doc)} stress-test only the docs under docs/Code/Core/Ai/Mcp
```

**How it works:**

1. AI finds the changed AiDocs from Git status, including new untracked files
2. Each document gets its own focused review pass, using its AiDocMetaDoc when one exists (a missing one doesn't block the review)
3. AI reviews the documents together — boundaries, repetition, reading dependencies
4. You receive a brief report of what improved and any questions that need your decision

How is this different from `refine`? Refine polishes *your* edits while protecting your intent. Stress-test questions whether each changed passage earns its place at all.

---

## 🔍 `${AGENT_SKILL(ai-doc)} debug` — Test Documentation Quality

Reflects on documentation effectiveness using actual session evidence. Documentation is accountable for AI guidance quality — if AI performed poorly, documentation failed to guide properly.

**When to use:**
- After a session where AI behavior didn't match expectations
- End of any session, to get AI feedback on documentation quality

**Two modes:**

Investigate specific anomaly:
```
${AGENT_SKILL(ai-doc)} debug AI created entity files in wrong directory structure, didn't follow CodeUnit patterns
```

General session reflection (no arguments):
```
${AGENT_SKILL(ai-doc)} debug
```

**What you get:**
- Identified documentation gaps framed as practical data points (not AI errors)
- Specific improvement direction for the documentation that was insufficient

---

## 📦 `${AGENT_SKILL(ai-doc)} move` — Relocate Documentation

Moves documentation files while keeping all references intact across the codebase.

**When to use:**
- Reorganizing documentation structure
- Renaming or relocating AiDoc files

**Example prompts:**

```
${AGENT_SKILL(ai-doc)} move docs/Old/Feature.md to docs/New/Feature.md
```

```
${AGENT_SKILL(ai-doc)} move docs/Old/FeatureFolder to docs/New/FeatureFolder
```

**What happens:**
1. AI identifies all files to move (including `.meta.md` companions)
2. AI searches for all references to these files
3. Files are moved with `git mv` to preserve history
4. All references are updated
5. AI verifies no broken references remain

---

## 🔗 `${AGENT_SKILL(ai-doc:ai-doc-ref)}` — Reference Plugin Content from External Docs

Agent-facing skill that prints ai-doc plugin documents by short name. Used in external project files (workflows, commands, format specs) without knowing the installed plugin path.

**Example usage in an external doc:** `- Call '${AGENT_SKILL(ai-doc:ai-doc-ref)} HumanDoc' skill - format for human-facing documentation`

See the [available short-name references](skills/ai-doc-ref/help.md).

---

## 📖 Complete Scenarios

### Scenario 1: Creating New Documentation

**Context:** You need to document MCP test patterns.

**Step 1: Create AiDocMetaDoc**
```
${AGENT_SKILL(ai-doc)} meta Create meta for docs/Code/Core/Ai/Mcp/McpTests.md with these considerations:
- Describes proper MCP test class patterns
- Has CodeDoc format
- tests/Services/Ai/Mcp/Redmine/RedmineMcpServerSchemaTest.php is a good example
```

Review the generated `.meta.md` — check that goals, required reading, and format look right.

**Step 2: Create AiDoc**
```
${AGENT_SKILL(ai-doc)} build Create docs/Code/Core/Ai/Mcp/McpTests.md
- Use docs/Code/Core/Ai/Mcp/McpCode.md as main source of knowledge
```

The AI reads your AiDocMetaDoc, loads all required context, and builds the document.

### Scenario 2: Improving Existing Documentation

**Context:** A workflow document needs restructuring after a process change.

**Single step:**
```
${AGENT_SKILL(ai-doc)} build Improve docs/code/on-build.md
- Clarify which verification the workspace check already performs
- Keep the builder's additional verification responsibilities explicit
```

The AI reads the document's meta when present, its format and required sources, then applies improvements while maintaining format compliance.

### Scenario 3: Reorganizing Documentation

**Context:** A directory was restructured and docs need to follow.

```
${AGENT_SKILL(ai-doc)} move docs/Code/Domain/OldModule to docs/Code/Domain/NewModule
```

The AI moves all files (including `.meta.md` companions), updates every reference across the codebase, and verifies nothing is broken.

---

## 🎯 Start Simple, Iterate

Every line in your documentation competes for AI attention. More isn't better — it's worse.

1. Start with minimal documentation
2. Use it in practice
3. Add only what's clearly missing
4. Remove what isn't used

**Recognizing bloat:** repeated information across sections, examples that don't add new patterns, explanations of obvious concepts. If you can't immediately explain why a line is essential, it probably isn't.
