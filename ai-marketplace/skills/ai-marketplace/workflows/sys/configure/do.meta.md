# do.meta.md

Authoring context for [marketplace repository configuration](do.md).

## do.md goals and principles

- Enables an agent to perform repository configuration, not merely assess its principles. Combines the intended working state with concrete use of the bundled Python builder and validator, and a practical setup path through hosting, CI and publication. Exact API calls remain platform- and access-dependent.
- Covers GitLab and GitHub configuration while keeping hosting topology specific to the marketplace. Source ownership, source synchronization and publication of host-specific builds are distinct responsibilities; mirroring source and mirroring a built distribution achieve different outcomes.
- Connects repository configuration to usable distributions for the marketplace's supported agent hosts. Verification concerns what consumers receive, not merely whether repositories exist or CI accepts its configuration.
- Keeps access and activation boundaries explicit: preparing configuration differs from enabling automatic publication. Missing permissions and unresolved operator choices remain visible rather than being replaced with assumed credentials or destinations.
- Remains reusable outside zd-plugins and Bico. Concrete repository names, runner assignments, credentials and deployment status belong to the configured marketplace; examples illustrate the model without establishing universal requirements.

## AiDocFormat

[WorkflowDoc format](AI_DOC_PLUGIN/Formats/WorkflowDoc/WorkflowDoc.format.md) - Actionable configuration steps with concrete tools and verifiable outcomes, without fixing one hosting topology.

## MUST read before editing do.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps the setup guidance focused on established configuration needs rather than an exhaustive hosting checklist.
- [Constraint theory](AI_DOC_PLUGIN/Theory/GuideVsGiveFreedom.md) - Explains why target-state and consequential coordination constraints are useful while investigation and provisioning mechanics remain flexible.

## MAY read for additional context before editing do.md

- [Marketplace organization](../../../../../codebase/on-plan.md) - When describing source, plugin and distribution boundaries.
- [Host rendering](../../../../../docs/HostRendering.md) - When describing the generated outputs and the distinction between successful rendering and host acceptance.
- [zd-plugins operations](../../../../../../docs/Maintaining.md) - Concrete GitLab and GitHub publication example; its current topology is not the generic configuration contract.
- `ai-marketplace/scripts/build.py` and `ai-marketplace/scripts/validate_pi.py` - Own the bundled converter's actual CLI; setup guidance should use these tools rather than leave the agent to invent a build system.
- `.gitlab-ci.yml` and `.gitlab/publish.sh` - When using the existing GitLab publication implementation as evidence for configuration outcomes and safeguards.
- [GitLab CI documentation](https://docs.gitlab.com/ci/) and [GitHub Actions documentation](https://docs.github.com/en/actions) - When platform capabilities affect the guidance; these own current platform mechanics rather than the workflow duplicating them.

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Direct configuration request

`Configure this marketplace repository for GitLab and GitHub using this guidance.`

### Role do.md serves during use

- Practical setup guide connecting repository configuration to the bundled converter, host-specific publication and verified delivery.
