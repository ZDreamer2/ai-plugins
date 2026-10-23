# Start Simple: Iterative Documentation Development for AI Agents

## Why minimal first

[AiDoc writing principles](AiDocBaseFormat.md#core-philosophy) state the principle: minimal documentation is correct, and detail is added on evidence. This document gives the reasoning behind it and how to apply it over a document's life.

Intuition about what an agent needs is frequently wrong until tested - the author's intuition, human or AI. Guidance written ahead of usage mostly addresses problems that never occur. Each such line still costs attention in every task that loads the document, and has to be kept in sync with the workflows it describes. A short document reaches real use sooner, and real use is the only reliable source of what is missing. This is YAGNI applied to documentation.

## Creating a document

Write what can be used immediately:
- Main sections only
- One working example
- Rules already known to be necessary

Leave out content whose only justification is that a situation might arise. Omitted content will usually sound useful; the test is whether usage has asked for it, not whether it is plausible.

## Editing a document

Treat the current content as sufficient. Brevity is a result of the method, not a gap to fill.

Evidence for adding detail comes from usage: the user reports what an agent did wrong or could not do in a real session, or the [documentation debugging workflow](../workflows/debug/do.md) traces a session anomaly to the document.

Your own anticipation of what could go wrong is not evidence. When you see a likely gap, raise it with the user and leave the document as it is until usage confirms it.

Add the narrowest change that closes the observed gap. Evidence works in both directions: content that usage shows agents do without is a candidate for removal.

## Relation to constraint theory

[Constraint theory](GuideVsGiveFreedom.md) decides how much a document constrains the agent's execution: constrain coordination and proven patterns, not investigation. StartSimple decides how much a document contains and when it grows. A short document can still over-prescribe, and a long one can still leave the agent free. Apply both.
