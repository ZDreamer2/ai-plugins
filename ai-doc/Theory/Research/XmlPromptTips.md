# XML Prompt Formatting Guide for Claude 4

## Basic Structure and Tag Naming

Use **semantic, descriptive tag names** that clearly indicate content purpose. Claude 4 interprets tag meanings, so `<customer_feedback>` outperforms generic tags like `<data>`. Keep tag names lowercase with underscores for multi-word tags.

```xml
<!-- Good -->
<analysis_request>
	<data_source>Q4 financial records</data_source>
	<output_format>executive summary</output_format>
</analysis_request>

<!-- Avoid -->
<req>
	<src>Q4 financial records</src>
	<fmt>executive summary</fmt>
</req>
```

## Optimal Nesting Depth

Maintain **2-3 levels of nesting** for best performance. Deeper structures remain functional but offer diminishing returns.

```xml
<!-- Optimal depth -->
<task>
	<requirements>
		<priority>high</priority>
		<deadline>2024-12-01</deadline>
	</requirements>
	<deliverables>
		<report>financial analysis</report>
		<presentation>stakeholder deck</presentation>
	</deliverables>
</task>

<!-- Too deep - avoid unless necessary -->
<task>
	<requirements>
		<scheduling>
			<timeline>
				<start>
					<date>2024-11-01</date>
				</start>
			</timeline>
		</scheduling>
	</requirements>
</task>
```

## Attribute Usage

Use attributes for **simple metadata only**. Keep semantic content in element bodies, not attributes.

```xml
<!-- Good attribute usage -->
<requirement priority="high" id="REQ-001">
	<description>Implement authentication system</description>
	<acceptance_criteria>Support OAuth 2.0 and SAML</acceptance_criteria>
</requirement>

<!-- Avoid content in attributes -->
<requirement description="Implement authentication system" criteria="Support OAuth 2.0">
</requirement>
```

## Indentation and Whitespace

While Claude 4 is **whitespace-agnostic**, consistent indentation improves human readability during development. Choose either 2 or 4 spaces and maintain consistency.

```xml
<!-- Both perform identically -->
<!-- Formatted -->
<analysis>
	<method>regression</method>
	<confidence>95%</confidence>
</analysis>

<!-- Minified -->
<analysis><method>regression</method><confidence>95%</confidence></analysis>
```

## High-Performance Patterns

### Chain-of-Thought Enhancement
```xml
<problem>Calculate optimal pricing strategy</problem>
<thinking>
	Step 1: Analyze competitor pricing...
	Step 2: Consider cost structure...
</thinking>
<solution>Recommended price point: $X</solution>
```

### Multi-Example Learning
```xml
<examples>
	<example>
		<input>User query about refunds</input>
		<output>Structured refund policy response</output>
	</example>
</examples>
<task>Handle this similar query</task>
```

### Context Isolation
```xml
<system_context>Production environment constraints</system_context>
<user_request>Specific feature request</user_request>
<constraints>Security requirements</constraints>
```

## Common XML Tags That Tokenize Efficiently

These tags process as single tokens, minimizing overhead:
- `<instructions>`, `<example>`, `<context>`, `<output>`
- `<task>`, `<data>`, `<result>`, `<query>`


## Best Practices Summary

1. **Match complexity to task** - Simple tags for simple tasks, hierarchies for complex ones
2. **Maintain consistency** - Same structures throughout conversation enable 90% caching benefits
3. **Prioritize clarity** - Semantic tag names improve comprehension by 30%
4. **Avoid over-nesting** - Stay within 2-3 levels unless absolutely necessary
5. **Keep attributes minimal** - Use only for IDs, priorities, and simple flags
6. **One purpose per tag** - Don't overload tags with multiple responsibilities

## What to Avoid

- Generic tag names (`<item>`, `<data>`, `<info>`)
	- Deep nesting beyond 3 levels
	- Semantic content in attributes
	- Inconsistent tag naming conventions
	- Mixing formatting styles within same prompt
	- Complex hierarchies for simple categorization tasks

# Escaping < > &
- It is unclear if we should escape < > & inside XML tags.
- Will not escape for now.
- No information on in [Anthropic's XML tag guidance](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
- One helper does it: [Prompt XML Studio](https://xmlprompt.carterlasalle.com/)
