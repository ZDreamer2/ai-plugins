# WriteFinal

## Core Principle

When a doc ecosystem is being built incrementally, each AiDoc MUST be authored as if the planned architecture is already complete. References, relationships, and routing reflect the target state — not the current build progress.

## Rules That Flow From the Principle

### Reference planned docs normally

When a doc SHOULD exist in the target architecture but is currently an empty stub or not yet created, reference it the same way as any existing doc. No "when available", "once created", or "placeholder" qualifiers.

### Do not reference transitional artifacts

A transitional artifact is a doc that carries relevant knowledge now but will be absorbed into another doc or deleted as the ecosystem matures. Referencing it creates a dead link in the target state. Instead, reference the doc that will carry that knowledge in the finished architecture.

### Do not persist WriteFinal in meta docs

WriteFinal is session-scoped guidance for the current building session, not a permanent editing constraint. Once the ecosystem is fully built, its rules become irrelevant — every planned doc exists, so there are no stubs to qualify or transitional artifacts to avoid. Persisting it in a MUST read section makes WriteFinal itself a transitional artifact in the meta doc.

When a building session needs WriteFinal, the user provides it directly (e.g. as a session argument). Meta docs MUST NOT reference WriteFinal.

## Relationship to StartSimple

StartSimple governs what content to include — start minimal, expand on evidence.

WriteFinal governs how to frame references and relationships — write for the planned architecture, not the current build progress.
