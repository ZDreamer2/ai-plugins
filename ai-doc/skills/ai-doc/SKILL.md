---
name: ai-doc
description: AI documentation workflows. Use when user invokes ${AGENT_SKILL(ai-doc)}.
user-invocable: true
disable-model-invocation: false
argument-hint: meta|build|refine|compact|move|debug|stress-test <request>
---

## Goal

Read context, classify the user's intent and dispatch to the right handler.

## MUST READ Context

- [AiDoc terminology](../../Theory/AiDocTerminology.md) - Use its definitions and meta-document naming convention
- [AiDoc writing principles](../../Theory/AiDocBaseFormat.md) - Writing and formatting principles to follow during any AiDoc changes

## Handlers

### Build meta

Create or improve an AiDocMetaDoc that provides editing context for an AiDoc.

Follow the [AiDocMetaDoc creation workflow](../../workflows/meta/do.md)

### Build

Create or improve an AiDoc using its AiDocMetaDoc for context and requirements.

Follow the [AiDoc creation workflow](../../workflows/build/do.md)

### Refine

Improve wording and consistency of user edits using the git diff, preserving intent.

Follow the [documentation refinement workflow](../../workflows/refine/do.md)

### Compact

Reduce reading effort for an AiDoc while preserving its purpose, optionally moving detail into satellites.

Follow the [AiDoc compaction workflow](../../workflows/compact/do.md)

### Move

Move documentation files while maintaining reference integrity across the codebase.

Follow the [documentation relocation workflow](../../workflows/move/do.md)

### Debug

Evaluate documentation effectiveness using session evidence and propose improvements.

Follow the [documentation debugging workflow](../../workflows/debug/do.md)

### Stress-test

Critically review and improve uncommitted AiDoc changes in the working copy.

Follow the [AiDoc stress-test workflow](../../workflows/stress-test/do.md)
