# do.meta.md

Specification for creating and editing the [local marketplace editing configuration workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables an agent to prepare a simple source-editing workstation for developers or domain experts without requiring routine Git expertise.
- Provides an opinionated path around one authoritative source checkout in the current working directory while preserving existing installations, configuration and local work.
- Keeps stable Git identity and checkout commands in the workflow while ordinary host, administrator and source-repository instructions own platform-specific installation and access mechanics.
- Makes `ai-doc`, `ai-marketplace` and the plugins needed for the specialist's work available in a fresh session rooted at the source checkout.
- Keeps local readiness distinct from central hosting, compilation, synchronization and publication; setup verification does not require test commits or pushes.

## AiDocFormat

[WorkflowDoc format](AI_DOC_PLUGIN/Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps setup focused on the established specialist workstation path rather than anticipated host variations.
- [Constraint theory](AI_DOC_PLUGIN/Theory/GuideVsGiveFreedom.md) - Helps constrain work preservation and verification while leaving platform investigation to the applicable instructions.
- [Marketplace planning guidance](../../../../../codebase/on-plan.md) - Defines the source, plugin and generated-distribution boundaries that local setup must preserve.
- [Marketplace source synchronization](../../sync/do.md) - Defines the collaboration loop the workstation must support and its plain-language user experience.

## MAY read for additional context before editing do.md

- [Central repository configuration](../configure/do.md) - Read when changing the boundary between local setup and source hosting, CI or generated-distribution publication.
- [Marketplace local compilation](../../compile/do.md) - Read when changing the boundary between setup verification and optional local builds.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Loaded through marketplace system configuration

Administrator or specialist invokes `sys configure-local` -> this workflow coordinates the host, access, plugins and source checkout in the current working directory.

### Role do.md serves during use

- Practical local setup guide producing a fresh agent session ready for marketplace source editing.
