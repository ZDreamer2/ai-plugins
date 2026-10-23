# ReadNecessaryFilesStep.meta.md

Specification for editing [Read necessary files step](ReadNecessaryFilesStep.md). Defines purpose, usage patterns, and constraints.

## ReadNecessaryFilesStep.md goals and principles

- Defines reusable block format for workflow steps that load context documents deterministically
- Provides good practices for different complexity levels - from simple file lists to complex path derivation logic
- Despite complexity variations, aims for unified structure when possible
- Enables consistent context-loading patterns across workflows
- Focuses on WHAT files to load and WHY, trusting AI to handle file reading mechanics

## AiDocFormat

[AiDocBlockFormatDoc format](../../BlockFormatDoc/AiDocBlockFormatDoc.format.md)

## MUST read before editing ReadNecessaryFilesStep.md

- [Block concept](../../BlockFormatDoc/BlockConcept.md) - Understand block vs document distinction and scope boundaries
- [AiDocBlockFormatDoc format](../../BlockFormatDoc/AiDocBlockFormatDoc.format.md) - Apply its template and validation requirements
- [StartSimple methodology](../../../Theory/StartSimple.md) - Start minimal, expand based on evidence

## MAY read for additional context before editing ReadNecessaryFilesStep.md

- [AiDoc creation workflow](../../../workflows/build/do.md) - Read when refining sequential reading substeps and their dependencies (1.1-1.5)
- [AiDocMetaDoc creation workflow](../../../workflows/meta/do.md) - Read when refining conditional context gathering or path deduction

## ReadNecessaryFilesStep.md typical use context

### Role ReadNecessaryFilesStep.md serves during use

- Block specification referenced when writing WorkflowDoc instances that need deterministic context loading
- Template for creating "Read necessary files" workflow steps
- Ensures consistency in how workflows specify required reading context

## ReadNecessaryFilesStep.md underlying theory

Workflows require deterministic context loading to ensure all necessary knowledge is available before planning and execution. Incomplete context leads to flawed planning.

The block format supports deterministic loading through:
- Direct file references with Markdown links and brief purposes (5-10 words max)
- Path deduction logic when files must be derived from context
- Path transformation rules when creating new paths from existing ones
- IF/THEN logic for conditional loading based on state

Format specifies WHAT files to load and WHY (purpose), trusting AI to handle HOW (reading mechanics).
