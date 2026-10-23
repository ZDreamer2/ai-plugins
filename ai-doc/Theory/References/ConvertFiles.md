# Convert references in files

## Input

One or more file paths.

## Workflow

1. Read [reference path management](ReferencePathManagement.md).
2. Process assigned files one at a time. Read the whole file and applicable editing context. For MUST/SHOULD/MAY read sections, read [reading context guidance](../../Blocks/ReadingContext/ReadingContext.md) and consider how its label and description principles apply to each section.
3. Assess each reference individually, including existing Markdown links. Establish its intended target and read each linked document to understand its content and role in the referencing passage. Consider the label, destination, and surrounding text together, then convert according to the theory. Choose the label and any reading description based on that understanding. Preserve reading obligations and unrelated content, including existing user edits. Leave ambiguous references unchanged and report what prevents their conversion.
4. Before starting the next file, review the diff and the resulting references in context. Verify that each label conveys the intended meaning, each reading description adds useful guidance beyond the label and answers the section's framing question, and each destination reaches the intended target, including fragments.
5. Return a brief result for every assigned file: converted, already compliant, or incomplete, with unresolved references and checks performed.

Edit only assigned files. Do not delegate, commit, or publish changes.
