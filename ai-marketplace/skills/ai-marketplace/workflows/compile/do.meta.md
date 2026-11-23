# do.meta.md

Specification for creating and editing the [marketplace local compilation workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables developers and domain experts to compile and validate the current marketplace working tree through one reusable command route, including uncommitted edits.
- Uses the shared builder bundled with ai-marketplace rather than repository-specific snapshots or invented build commands.
- Keeps local rendering, domain-specific checks, fresh-session testing, source synchronization and publication visibly distinct.
- Reports enough source and tooling provenance to interpret the result without implying that local compilation established installed-host behavior or live publication.
- Remains reusable across marketplaces; repository instructions own plugin-specific checks and isolated test-session procedures.

## AiDocFormat

[WorkflowDoc format](AI_DOC_PLUGIN/Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps the route focused on established local compilation rather than installation or publication features.
- [Constraint theory](AI_DOC_PLUGIN/Theory/GuideVsGiveFreedom.md) - Supports concrete compilation coordination while leaving repository-specific verification flexible.
- [Marketplace planning guidance](../../../../codebase/on-plan.md) - Defines the source and generated-distribution boundaries compilation must preserve.

## MAY read for additional context before editing do.md

- [Marketplace repository configuration](../sys/configure-central/do.md) - Read when changing the boundary between local compilation, CI and publication.
- [Marketplace source synchronization](../sync/do.md) - Read when changing the boundary between compiling a working tree and sharing source changes.
- `ai-marketplace/scripts/build.py` and `ai-marketplace/scripts/validate_pi.py` - Own the bundled tools' actual command-line contracts.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Loaded through the ai-marketplace hub

User requests local marketplace compilation -> ai-marketplace selects Compile -> loads this workflow with the current source checkout and repository instructions.

### Role do.md serves during use

- Produces local host distributions and validation evidence from the current source working tree without conflating this operation with marketplace implementation through Build.
- Gives the maintainer output locations and provenance needed for subsequent domain checks or an isolated fresh-session trial.
