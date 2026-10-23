# On Build Done

Every line costs Agent attention, and the Agent reading it is competent: it has more context in its situation than the doc can have. A line earns its place only by conveying something enduring the Agent would not otherwise know or do. The higher the doc's altitude (how global it is), the more tasks pay that cost.

Recurring ways changes fail this test. Check the changes against each, with the doc's altitude in mind:

- Micromanagement - "how" where "what" and "why" would do
  - Does the change guide the goal and trust the Agent's judgment? Does every "how" it gives earn its place, or would the Agent find it itself?

- Enumerations - instances where the rule would do
  - Did we add enumerations? Does each one own its place, or would the rule behind it do?

- Patching - diff instead of state
  - Do we state the current state of things, or "patch" changes on top of the old document?
  - Do any "no"/"not" statements argue with the old version? We want the current state, unless the AiDocMetaDoc asks for history

- Describing instead of naming
  - Is there a paragraph where an established term (TDD, dependency injection, idempotent) would point at what the Agent already knows?
  - Is every term we use a real term of art? A coined or near-miss name activates the wrong knowledge just as confidently

Discuss anything you are unsure about.
