# Validation Rules Section Format Specification

## Validation Rules template

```markdown
## Validation Rules

- [MUST/SHOULD/MAY requirement]
```

## Template Notes

Validation Rules section serves as a validation checkpoint after document creation or editing. Unlike sections that introduce new information, this section highlights the most critical points that warrant verification.

The section conveys "among all considerations, THESE are critical" rather than "everything is critical." Duplicating content from earlier sections is natural and expected when those points warrant reinforcement during validation.

### [MUST/SHOULD/MAY requirement]

- Write requirements with deliberate restraint. Include only requirements that are:
  - Non-negotiable for document correctness
  - High-priority validation points
  - Would cause significant issues if violated

- Format using RFC 2119 directive terms (MUST/SHOULD/MAY) as defined in [AiDoc directive-language rules](../../Theory/AiDocBaseFormat.md#directive-language-rfc-2119):
  - Use only directive types matching actual requirements - not all types need to be present
  - Order requirements from most to least critical

- When several requirements share the same condition, factor it out using IF/THEN:

```markdown
## Validation Rules
- IF entity has relationships THEN:
  - MUST define inverse relationship
  - MUST handle cascade deletion
  - SHOULD add relationship validation
```

For single requirements, write them directly without IF/THEN ceremony.

## Validation Rules example

This document's own Validation Rules section (below) demonstrates the pattern: it focuses on the most critical validation points rather than exhaustively listing all formatting details from Template Notes.

## Validation Rules

- MUST use RFC 2119 terms as defined in [AiDoc directive-language rules](../../Theory/AiDocBaseFormat.md#directive-language-rfc-2119)
- MUST use bullet list format for all requirements
- MUST order requirements from most to least critical
- SHOULD include only truly essential validation points (demonstrate restraint over exhaustiveness)
