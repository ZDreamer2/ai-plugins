# Constraint Theory: When to Guide vs Trust AI

## The Core Distinction

AI agents excel at investigation and discovery when given freedom, but benefit from specificity when executing proven patterns. The key is knowing which situation you're documenting.

Fundamental principle: Constrain coordination and proven patterns, not investigation and problem-solving.

## When Constraints Help

Constraints add value when they:

- Document proven patterns: Specific prompts or tool usage that consistently work (e.g., a fresh-context subagent given a specific guide)
- Coordinate multi-step processes: When order matters for correctness or dependencies exist
- Highlight non-obvious requirements: Gotchas, edge cases, or counterintuitive needs
- Establish safety boundaries: Critical restrictions, security requirements, or data protection
- Specify resource loading: When specific files must be loaded in particular order

These constraints document hard-won knowledge about what works.

## When Constraints Hinder

Avoid constraints for:

- Investigation tasks: Let AI determine how to explore and understand problems
- Obvious data interpretation: AI can read error messages, test output, and logs without guidance
- Problem-solving approaches: Multiple valid paths often exist; let AI choose based on context
- Pattern recognition: AI excels at seeing patterns across files and outputs
- Debugging strategies: The actual error guides investigation better than predetermined steps

Trust AI to leverage its full context visibility and pattern recognition. We should provide a light touch that orients
thinking rather than prescribing specifics.

## The Decision Framework

Ask yourself:

1. Is this a proven pattern that works? → Document it specifically
2. Can AI see the answer in the context? → Don't prescribe how to find it
3. Does order matter for correctness? → Specify the sequence
4. Is this discovery or execution? → Guide execution, trust discovery

If unsure, err on the side of fewer constraints.

## Examples

### Example 1: Test Investigation

Over-constrained:
```
1. Read test file to understand structure
2. Run tests and identify which assertions fail
3. Check if it's a field mapping issue
4. Verify nullable handling
```

Appropriately flexible:
```
Run tests to see what fails.
```

The AI sees the test output and will naturally investigate based on actual failures.

### Example 2: Proven Workflow Pattern

Under-constrained:
```
Update multiple files as needed.
```

Appropriately specific:
```
Launch a fresh-context subagent with the prompt: "Update `{file_path}` following [the migration guide](path/to/guide.md)"
```

This documents a proven pattern that consistently works.

### Example 3: File Discovery

Over-constrained:
```
First use Glob for extensions, then Grep for content, then combine results.
```

Appropriately flexible:
```
Use search tools (Glob, Grep) to find target files.
```

AI can determine the best search strategy based on the actual need.

## Quick Reference

- Provide goals and tools, not procedures
- Constrain the WHAT and WHEN, not the HOW
- Document patterns, trust investigation
- Reference existing docs, don't duplicate
- Specify coordination, not exploration

Remember: AI agents have full context visibility and excellent pattern recognition. Instructions should orchestrate and reference proven patterns while trusting investigative judgment. The best constraint is often the one you don't write.