# AuthoringSyntax.meta.md

Specification for editing [Markdown authoring syntax](AuthoringSyntax.md). Defines purpose, usage patterns, and constraints.

## AuthoringSyntax.md goals and principles

- The normative shared Markdown authoring contract for marketplaces adopting this CodebaseType: skill frontmatter, document references, agent-executed commands, agent placeholders and agent includes. Authors use the shared syntax without choosing a host except for intentionally agent-specific features
- Rules only: every statement is a rule an author applies or a fact the build enforces, with one example where the shape is not obvious. Host renderings, validation details and reports belong to [host rendering](HostRendering.md); marketplace-specific testing and publication status belong to the marketplace README. They are not prerequisites for applying these rules
- MUST agree with the rendering implementation. Consult the implementation references below when changing rendering claims; use neutral names for syntax examples
- MUST distinguish installed-plugin references from source meta references: metas can reach the whole marketplace, with document-relative Markdown links and directory paths and marketplace-root paths for code and other non-Markdown files
- MUST NOT cover marketplace-specific plugin lifecycle, report locations, build authorization or cleanup

## AiDocFormat

[BaseDoc format](AI_DOC_PLUGIN/Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing AuthoringSyntax.md

- [Start Simple](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keep the document to proven rules; add a rule when authors get it wrong, not when a case is imaginable

IMPORTANT: AuthoringSyntax.md is authored as the final reader-facing text, with literal variable names and placeholder examples. MUST NOT encode literal host variables as agent placeholders; the builder leaves them unchanged.

## MAY read for additional context before editing AuthoringSyntax.md

The following marketplace-root implementation paths support maintenance of the shared contract, not ordinary use of the guide.

- `ai-marketplace/scripts/marketplace/build/rendering/_placeholders.py` - When changing marker rules, verify vocabulary, argument syntax, host values, escaping and diagnostics
- `ai-marketplace/scripts/marketplace/build/rendering/_includes.py` - When changing include rules, verify placement, target validation, nesting and host selection
- `ai-marketplace/scripts/marketplace/build/rendering/_links.py` - When changing included link semantics, verify logical source bases, Markdown destination parsing and literal-code preservation
- `ai-marketplace/scripts/marketplace/build/rendering/_codex.py` and `ai-marketplace/scripts/marketplace/build/rendering/_pi.py` - When changing skill rules, verify host frontmatter adaptation, namespacing and validation
- `ai-marketplace/scripts/marketplace/build/rendering/_constructs.py` - When changing report coverage, verify which constructs remain literal

- [Reference path management](AI_DOC_PLUGIN/Theory/References/ReferencePathManagement.md) - When touching the reference rules: apply its document-relative paths, link syntax, reading obligations and prohibition on context injection
- [Host rendering](HostRendering.md) - When deciding whether a statement is a shared rule (here) or an output explanation (there)
- [Marketplace README](../../README.md) - When deciding whether a statement belongs to syntax or local marketplace operations
- `ai-marketplace/scripts/marketplace/build/rendering/tests/` - When verifying a rule, use the focused rendering fixtures for Claude, Codex and Pi

## AuthoringSyntax.md typical use context

### 💡 Distinct usage patterns for AuthoringSyntax.md

#### Direct reference when writing or editing plugin markdown

`Edit a plugin workflow following the marketplace Markdown authoring syntax.`

#### Loaded indirectly during plugin authoring

Codebase build guidance or a marketplace build guide -> this authoring contract -> rules relevant to the Markdown being edited

### Role AuthoringSyntax.md serves during use

- Checklist an author or agent applies to every markdown file before it enters the source: what to write and when to use an intentional agent-specific escape hatch
