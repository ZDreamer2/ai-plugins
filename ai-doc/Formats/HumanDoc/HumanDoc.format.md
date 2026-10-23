# Human-Facing Documentation Format

IMPORTANT: This format MUST NOT follow [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) since we are creating document for humans, not AI model.

## Core Philosophy

Write naturally for human readers while maintaining necessary conciseness. Every sentence should earn its place. Prioritize comprehension through clarity, not length.

## What's Different from BaseDoc

### ✅ Formatting Freedoms

**Emojis Welcome** 
- Use emojis for visual navigation and friendliness
- 📚 for documentation, ✅ for dos, ❌ for don'ts
- Makes scanning and finding sections easier for humans

**Bold for Emphasis**
- Use **bold** to highlight key concepts
- Unlike BaseDoc, bold helps human readers scan effectively
- Don't overuse - reserve for truly important points

**Visual Aids**
- Tables for comparisons and quick reference
- Diagrams and ASCII art when helpful
- Code blocks with syntax highlighting
- Screenshots and images when available

**Human-Friendly Structure**
- Longer explanations ONLY when necessary for understanding
- Progressive disclosure (overview → details)
- Summaries for complex topics
- FAQs when genuinely helpful
- "Quick Start" guides for getting started

## What Remains from BaseDoc

### Core Principles
- **Conciseness matters** - Don't confuse "human-friendly" with "verbose"
- Every paragraph should have a purpose
- Cut redundancy ruthlessly
- If you can say it in 5 words instead of 15, do so

### Structure and Organization
- Clear markdown headers for sections
- Logical flow of information
- Practical examples
- Consistent formatting within the document

### Quality Standards  
- Accurate, tested information
- Clear, unambiguous language
- Complete coverage without bloat
- Regular updates as needed

## Two Kinds of Human-Facing Documents

**Guides** — tutorials, how-tos, quick starts, command guides. The reader wants to get something done; instruction is the genre: "do this, then that", with the reasons where they help.

**Descriptions** — reference pages, articles about a tool, plugin or part of a system. The reader wants to know what exists and how it behaves, and draws their own conclusions. For descriptions:
- Narrate the present state. No futures and no "for now" — a doc is read at an unknown date; maturity is a present fact ("first version"), not a promise
- Describe, do not advise. What the reader should do with the thing belongs to a guide
- State positively. What it does, not what it does not do or is not — a contrast with an alternative the reader never raised reads as argument
- Write from the reader's side, not the implementer's. What the reader gives, gets and meets; file names, internal rules and the author's own instructions stay out unless the reader meets them

## When to Use HumanDoc Format

Use this format when:
- Primary audience is humans learning or reference
- Document is an entry point or guide
- Visual aids significantly improve comprehension
- You need to explain "why" extensively
- Creating tutorials or how-to guides

DO NOT use for:
- AI agent task instructions (use BaseDoc)
- Code implementation patterns (use CodeDoc)
- Tool documentation (use ToolDoc)
- Step-by-step workflows (use WorkflowDoc)

## Specialized Guides

- [HowToUse document guide](HowToUseDoc.md) - MUST read and follow when writing a HowToUse.md document (command guides, workflow navigation)

## Quick Guidelines

When writing HumanDoc:
1. **Stay concise** - Human-friendly doesn't mean wordy
2. **Plain, natural tone** - Not robotic, not a story
3. **Use visual hierarchy** - Emojis and bold for scanning, where the host's style guide allows
4. **Include examples** - But only necessary ones
5. **Explain the why** - When it adds value

Remember: Formatting freedom doesn't mean length freedom. The goal is comprehension through clarity and appropriate formatting, not through exhaustive explanation.