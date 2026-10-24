# AI Plugins

Plugins for working with AI-assisted documentation and developing AI plugin marketplaces, available for Claude Code, Codex and Pi.

## Plugins

### ai-doc

Create and maintain documentation that guides an AI agent through practical tasks. AiDoc pairs a document with a companion `.meta.md` file that preserves its purpose, audience and editing context.

Use it to create documentation and its meta, refine edits, compact long guides, relocate documents with their references, or investigate why instructions did not work as intended.

For example, invoke the skill with: `Create a meta document for docs/Deployment.md, then build the deployment guide from it.`

See the [AiDoc entry skill](ai-doc/skills/ai-doc/SKILL.md) for available workflows and [AiDoc terminology](ai-doc/Theory/AiDocTerminology.md) for the document model.

### ai-marketplace

Develop plugin marketplaces from shared sources for Claude Code, Codex and Pi. The plugin supplies authoring guidance and Python tools for building host-specific metadata, rendering instructions and validating Pi distributions.

For example, invoke the skill with: `Help me add a plugin to this marketplace and check its output for Claude Code, Codex and Pi.`

See the [marketplace entry skill](ai-marketplace/skills/ai-marketplace/SKILL.md), [authoring syntax](ai-marketplace/docs/AuthoringSyntax.md) and [host rendering reference](ai-marketplace/docs/HostRendering.md).

## Install

Choose your host's distribution. Each installation page includes the commands for that host; you do not need to build this source repository.

| Host | Installation |
|------|--------------|
| Claude Code | [Claude Code distribution](https://github.com/ZDreamer2/ai-plugins-claude#install) |
| Codex | [Codex distribution](https://github.com/ZDreamer2/ai-plugins-codex#install) |
| Pi | [Pi distribution](https://github.com/ZDreamer2/ai-plugins-pi#install) |

Install either plugin or both. Review plugin instructions and bundled scripts before use: these workflows can direct your agent to edit files and execute commands.

## First use

After installation, start a new host session in the project you want to work on and invoke the relevant skill with your request:

| Host | Documentation | Marketplace development |
|------|---------------|-------------------------|
| Claude Code | `/ai-doc:ai-doc` | `/ai-marketplace:ai-marketplace` |
| Codex | `$ai-doc:ai-doc` | `$ai-marketplace:ai-marketplace` |
| Pi | `/skill:ai-doc` | `/skill:ai-marketplace` |

Documentation workflows use the companion meta as editing context; create it first when the target has none. The marketplace plugin guides work in your own source checkout rather than editing an installed plugin cache.

## Development and feedback

This is the source repository. The three host repositories are generated distributions; propose changes and report issues here.

For local build/test commands, README generation and publication operations, see the [maintainer guide](docs/Maintaining.md). Builds and publication are validated separately from installed-host behavior; end-to-end installed-host acceptance has not yet been completed.

## License

Project code uses the BSD Zero Clause license (`LICENSE`, SPDX `0BSD`). Vendored PyYAML retains its separate license; see its [provenance and license information](ai-marketplace/scripts/marketplace/_vendor/PyYAML.provenance.md).
