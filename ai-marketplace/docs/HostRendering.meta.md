# HostRendering.meta.md

Specification for creating and editing [host rendering reference](HostRendering.md). Defines purpose, usage patterns, and constraints.

## HostRendering.md goals and principles

- Human-facing English reference for authors deciding whether shared plugin content works under Claude Code, Codex and Pi
- Owns host output details and the rationale needed to interpret them; [authoring syntax](AuthoringSyntax.md) owns the shared writing rules, and [maintainer guide](../../docs/Maintaining.md) owns local build and test commands
- Distinguishes deliberate adaptations, literal host-specific constructs and enforced validation. A successful build or a report finding alone does not establish runtime compatibility
- Keeps literal syntax examples escaped where necessary so this reference retains its meaning in every rendered tree

## AiDocFormat

[Human-facing documentation format](AI_DOC_PLUGIN/Formats/HumanDoc/HumanDoc.format.md)

## MUST read before editing HostRendering.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps the reference focused on established cross-host behavior rather than speculative compatibility guidance
- [Maintainer guide](../../docs/Maintaining.md) - Defines the standalone extraction and local verification this reference supplements
- [Authoring syntax](AuthoringSyntax.md) - Owns the shared syntax contract; output explanations must agree without repeating its checklist
- `ai-marketplace/scripts/marketplace/build/rendering/__init__.py` - Defines the Python renderer's public contract and host metadata APIs

## MAY read for additional context before editing HostRendering.md

- `ai-marketplace/scripts/marketplace/build/rendering/_placeholders.py` and `ai-marketplace/scripts/marketplace/build/rendering/_includes.py` - When changing marker vocabulary, include behavior or diagnostics
- `ai-marketplace/scripts/marketplace/build/rendering/_links.py` - When changing included link rebasing or literal-code boundaries
- `ai-marketplace/scripts/marketplace/build/rendering/_claude.py`, `ai-marketplace/scripts/marketplace/build/rendering/_codex.py` and `ai-marketplace/scripts/marketplace/build/rendering/_pi.py` - When changing host metadata or skill adaptation
- `ai-marketplace/scripts/marketplace/source/_inventory.py` - When changing skill identity or Pi naming claims
- `ai-marketplace/scripts/marketplace/build/rendering/_constructs.py` - When changing report coverage
- [Maintainer guide](../../docs/Maintaining.md) - When changing local output verification; host acceptance remains a separate check

## HostRendering.md typical use context

### 💡 Distinct usage patterns for HostRendering.md

#### Referenced while authoring for several hosts

Marketplace overview, maintainer guide or authoring syntax -> author needs a rendered value or host limitation -> this reference

### Role HostRendering.md serves during use

- Cross-host output reference supporting authoring and adaptation decisions
