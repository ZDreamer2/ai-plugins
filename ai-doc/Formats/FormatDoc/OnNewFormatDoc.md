# Creating a New AiDocFormat From Scratch

## Creating a new format is hard

An AiDocFormatDoc is itself a kind of meta document — it describes how to write other documents. That extra layer makes from-scratch creation hard and requires special attention

## DocTemplate.md is important

Setting format right helps all future agents follow AiDocFormatDoc easily, it is what makes everything work

## Start with the template alone

The first good step is almost always to focus narrowly on the `[AiDocFormat] template` section — the template structure only, WITHOUT Template Notes, example, or Validation Rules — and clarify it with the user before going further.

While drafting that template, think about:

- The actual target docs this format will produce — what content they need to carry
- [Document template block](../../Blocks/DocTemplate/DocTemplate.md) - apply its template structure and placeholder naming conventions

Confirm the template with the user then continue as you see fit
