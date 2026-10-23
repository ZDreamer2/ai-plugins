# HowToUse Document Guide

Principles and patterns for writing effective HowToUse documents — human-facing guides that help developers navigate a system's workflow through its commands.

## Core Qualities

A good HowToUse document is:

- **Self-sufficient** — a developer understands the system and starts using it without reading anything else
- **Progressive** — overview first, then per-command details
- **Practical** — real examples over abstract descriptions
- **Conversational** — natural tone, like explaining to a colleague

## Document Structure

### 1. Welcome + System Overview

Open with a welcome line and brief system description:

```
Welcome to [SystemName] — a system that helps you [purpose through outcome].
```

If the system has concepts the reader needs before diving into commands, add a brief conceptual overview after the welcome. Keep it minimal — just enough to make the rest comprehensible.

### 2. 🔄 Overall Workflow

Show the high-level flow as a numbered list. This gives the reader a mental map before details:

```markdown
## 🔄 Overall Workflow

The process takes [input] and produces [output]:

1. **Step** → Brief description
2. **Step** → Brief description
3. **Step** → Brief description
```

### 3. Per-Command Sections

Each command gets its own section with the structure described in the next major section below. Separate command sections with horizontal rules (`---`).

### 4. Summary Section

End with either:

- **📋 Typical Workflow** — condensed step-by-step for quick reference
- **📖 Complete Scenarios** — worked examples showing end-to-end usage with real prompts

Complete Scenarios tend to be more useful — they show real prompts and outcomes developers can follow directly.

---

## Per-Command Structure

### Always include

**Header** with emoji + command + short description:

```markdown
## 📥 `/command:name` — Short Description
```

**Opening paragraph** — one paragraph explaining what this command does and produces.

**"When to use:"** — bullet list of situations. This is the routing mechanism — helps readers find the right command for their current step.

**"Example prompts:"** — code blocks with real, copy-pasteable prompts. At least one per command. Add brief context between examples when showing different usage styles.

### Include when relevant

**"What you get:"** — describe the output structure when it has sections or parts worth knowing about. Skip for simple commands where the opening paragraph already covers it.

**"How it works:"** — numbered steps describing the **interactive flow**: user's role, decision points, back-and-forth. Use when the command involves dialogue or multi-step interaction. Skip when it would just list AI's internal processing steps the user can't control.

**"What to mention in your prompt:"** — guidance on what prompt content shapes output quality. Use for commands where the user's input significantly affects results.

**"Reviewing the [Output]:"** — practical guidance on what to check in the output. Use when output needs human judgment before proceeding to the next step.

### 💡 Recipe subsections

Recipes capture non-obvious techniques within command sections:

```markdown
### 💡 Recipe: Descriptive title

[Show the technique, explain when it's useful]
```

Recipes are recommendations, not requirements. They suggest approaches for common situations but the developer decides.

---

## Formatting Conventions

- **Emoji** in section headers for visual scanning (📥 📋 🔨 ✅ 🔄 📖 ⚡)
- **Horizontal rules** (`---`) between major command sections
- **Code blocks** for all command examples and output samples
- **Bold** for key terms and subsection labels within command sections
- **Conversational tone** throughout — write like explaining to a colleague
