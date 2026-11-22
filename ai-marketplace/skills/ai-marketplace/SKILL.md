---
name: ai-marketplace
description: Guides AI plugin marketplace development, local compilation, repository configuration and source collaboration. Use for marketplace sources, plugins, local distributions, delivery configuration, or source synchronization.
user-invocable: true
disable-model-invocation: false
argument-hint: build|compile|configure|sync <request>
---

# AI plugin marketplace

## Goal

Classify the user's intent and dispatch to the right handler.

## Commands

- `${AGENT_SKILL(ai-marketplace)} build <request>` - Dispatch to `Build`
- `${AGENT_SKILL(ai-marketplace)} compile <request>` - Dispatch to `Compile`
- `${AGENT_SKILL(ai-marketplace)} configure <request>` - Dispatch to `Configure`
- `${AGENT_SKILL(ai-marketplace)} sync <request>` - Dispatch to `Sync`

## Workflows

### Build

Plan or implement marketplace sources, plugins, builder behavior or generated distributions.

Follow the [marketplace planning guidance](../../codebase/on-plan.md) before planning and the [marketplace build guidance](../../codebase/on-build.md) before implementation.

### Compile

Compile Claude, Codex and Pi distributions from the current source working tree and validate the Pi result without committing, pushing or publishing.

Follow the [marketplace local compilation workflow](workflows/compile/do.md).

### Configure

Set up source hosting, automated builds and generated-distribution publication.

Follow the [marketplace repository configuration workflow](workflows/sys/configure/do.md).

### Sync

Synchronize one authoritative marketplace source checkout: inspect local and incoming changes, integrate colleagues' work, commit intended edits and push them while preserving work.

Follow the [marketplace source synchronization workflow](workflows/sync/do.md).
