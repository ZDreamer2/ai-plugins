# Documentation usefulness

## Purpose and reader

Spend editorial effort once to make repeated reading easier. Every line costs attention in every task that loads the document; the more tasks load it, the more of them pay for each line.

Revise each document around what its intended reader needs to understand and do. Use its purpose, usage context and level of abstraction to judge what belongs. The result should help a fresh reader understand what matters and proceed with less effort.

## Content that earns its place

Preserve the map of the system, intent, contracts, constraints and non-obvious facts that support decisions or prevent likely mistakes. Each detail should contribute to the document's purpose and what its reader needs beyond the source code and other available documents.

Explain implementation details when understanding them is necessary for that purpose; otherwise leave them in source. Add missing context where its absence makes the document difficult to understand or use.

## Reduce the effort of repeated reading

Remove repetition, incidental detail and explanations better owned elsewhere. When a compact explanation is sufficient for the document's purpose and level of abstraction, keep that version locally and link to the fuller treatment elsewhere. Retain enough context for readers to understand the subject and decide when they need the detail.

Weigh editorial effort by how often the text is read and by whom: text loaded on every invocation earns stricter editing than text read only when the document itself is edited.

Revise surrounding passages when changes leave the rest of the document inconsistent, including sections untouched by the original edit. When documents are used together, resolve redundant or conflicting explanations with their respective purposes in mind.

Cut substantially where useful while preserving the meaning, intent, contracts and constraints readers rely on. Judge the result by how easily the reader can understand and act, rather than by its length alone. Growth is a cost to justify, not a neutral outcome: a change that leaves a document larger has to buy that size with something the reader would otherwise get wrong or lack. Leave text unchanged when a revision would not measurably reduce the reader's effort; rewording that preserves the same content spends attention without a reader benefit.

### When to split detail into satellites

Consider moving secondary or task-specific detail into a satellite document when doing so reduces repeated reading effort. Keep the main document useful on its own at its intended level of abstraction: it should explain the whole subject, support its reader's decisions and make clear when the linked detail is needed. A compact explanation in the main document may overlap with a fuller treatment in the satellite when that overlap preserves understanding. Keep material together when readers routinely need both parts or separating them would fragment understanding. Judge the combined reading and navigation effort, rather than the main document's length alone.
