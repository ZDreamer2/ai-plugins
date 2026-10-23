# AiDocBaseFormat

## Purpose

Foundation for writing AiDocs optimized for AI processing and task execution rather than visual aesthetics or casual reading.

## How You Process Documentation

### Sequential Processing

You read token by token, from start to finish. No skimming or visual scanning occurs.

### Perfect Recall

You maintain complete access to all content in your context window. Information doesn't need repetition for retention or summaries for recall.

### Attention Weighting

Nearby and semantically-related tokens receive higher attention weight during processing. Position and proximity affect how strongly different parts of context influence your decisions, even with perfect recall.

### Token-Level Processing

Text is processed as discrete tokens. ASCII text tokenizes more consistently than Unicode symbols. Distinctive token patterns may receive different attention treatment than common patterns.

## Core Philosophy

Minimal documentation is correct, not incomplete. You excel at investigation, pattern recognition, and leveraging full context visibility - comprehensive upfront guidance often constrains these capabilities while addressing problems that don't exist in practice.

Write only what is clearly understood and proven necessary right now. When genuine gaps surface through actual usage, the user will explicitly request additions. Until then, the current version is sufficient. Respond to evidence-based feedback, not theoretical completeness.

Warning signs of premature complexity:
- Instructions for scenarios that haven't occurred in practice
- Prescribing HOW to investigate rather than WHAT to achieve
- Multiple examples for unvalidated patterns
- Detailed guidance for "edge cases" without proven base cases

Add detail when documenting:
- Proven patterns that consistently work
- Coordination where order matters for correctness
- Non-obvious requirements or counterintuitive needs
- Safety boundaries and critical restrictions

Light documentation that trusts your capabilities outperforms heavy prescription. Constrain coordination and proven patterns, not investigation and problem-solving.

## Writing Principles

### Directive Language (RFC 2119)

Use RFC 2119 terms consistently for precise requirement levels:

MUST/MUST NOT - Absolute requirements with no exceptions
SHOULD/SHOULD NOT - Strong recommendations with rare, justified exceptions
MAY/OPTIONAL - Genuinely optional actions

Reserve these terms for actual requirement levels. Lowercase "must" creates ambiguity - use different phrasing for non-requirement contexts.

### Clarity and Precision

- Eliminate ambiguity through explicit references and consistent terminology
- Frame instructions positively - State what TO do rather than what to avoid

## Formatting Principles

### Bold

MUST NOT use bold except for critical safety constraints where mistakes are costly.

Target: Zero bold in most documents.

Instead use: Whitespace, lists, or sentence restructuring.

### ASCII Over Unicode

Text indicators tokenize more consistently than symbols. Use "Warning:" not ⚠️, "CORRECT/INCORRECT" not ✓/✗, "->" not "→".

### Lists vs Prose

- Use bullet lists for multiple distinct points. Lists provide clear boundaries for each idea, reducing parsing overhead.

- For nested lists with sub-bullets:
  - Use two-level structure when top-level items have supporting details
  - Separate multi-line units (bullet + sub-bullets) with blank lines
  - Keep simple single-line lists compact without blank lines

- Use prose for conceptual explanations that flow together.

### References to Other Documents

Use Markdown links for references to Markdown documents and backticks for other file references or literal paths and syntax. Choose each link's label to convey the target's subject or role in context. Use a filename as the label when the file's identity is relevant. Let the surrounding sentence or section establish why or when to read the target.

Paths are relative to the containing document by default. References to project code files use project-root paths. Meta documents outside ai-doc use `AI_DOC_PLUGIN/...` when referencing ai-doc content.

### Conciseness Without Sacrificing Clarity

Remove redundant words, use active voice. Never sacrifice necessary context for token reduction.
