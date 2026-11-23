# do.meta.md

Specification for creating and editing the [local marketplace editing configuration workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Enables an agent invoked in an existing authoritative marketplace source checkout to prepare that checkout and the current session for source editing by developers or domain experts without requiring routine Git expertise.
- Treats the running agent and the current working directory as the source checkout root as prerequisites; local configuration does not install an agent, clone a repository or select another checkout.
- Preserves existing configuration and local work, uses the employee's own Git identity and credentials, and leaves platform-specific access mechanics to applicable host, administrator and source-repository instructions.
- Leaves host-specific plugin enablement to separate host procedures because no shared Claude, Codex or Pi protocol is currently established.
- Keeps local readiness distinct from central hosting, compilation, synchronization and publication; setup verification does not require test commits or pushes.

## AiDocFormat

[WorkflowDoc format](AI_DOC_PLUGIN/Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps setup focused on the established in-session checkout path rather than anticipated host variations.
- [Constraint theory](AI_DOC_PLUGIN/Theory/GuideVsGiveFreedom.md) - Helps constrain existing-environment preservation and verification while leaving platform investigation to the applicable instructions.
- [Marketplace planning guidance](../../../../../codebase/on-plan.md) - Defines the source, plugin and generated-distribution boundaries that local setup must preserve.
- [Marketplace source synchronization](../../sync/do.md) - Defines the collaboration loop the configured checkout and session must support and its plain-language user experience.

## MAY read for additional context before editing do.md

- [Central repository configuration](../configure-central/do.md) - Read when changing the boundary between local setup and source hosting, CI or generated-distribution publication.
- [Marketplace local compilation](../../compile/do.md) - Read when changing the boundary between setup verification and optional local builds.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Loaded through marketplace system configuration

Developer or domain expert invokes `sys configure-local` from an agent session rooted at the authoritative source checkout -> this workflow configures and verifies repository access and editing readiness in that session.

### Role do.md serves during use

- Practical in-session setup guide producing a verified source checkout and current agent session ready for marketplace source editing.
