# AI Plugins

Plugins for creating reliable AI guidance and developing cross-client AI plugin marketplaces.

## Plugins

### ai-doc

Create and maintain project documentation that guides AI agents through practical work. The plugin helps you define a document's purpose, build it, refine edits, reduce bloat, move it safely and investigate instructions that did not work as intended.

For reliable repeated editing, a document can have a companion `.meta.md` file that preserves its purpose, audience and authoring context without adding that information to the document itself.

A useful meta request explains what the document should achieve, when it is used and which boundaries or sources matter. A typical start:

1. Define the authoring context:

   ```text
   Create a meta document for docs/Deployment.md.
   - Goal: guide an AI agent through safe, repeatable deployments
   - Use context: loaded when preparing or carrying out a production release
   - Boundary: cover deployment and verification; link to environment setup instead of duplicating it
   ```

2. After reviewing the generated meta: `Build docs/Deployment.md.`

See the [AiDoc usage guide](ai-doc/HowToUse.md) for the document model, available workflows and more examples.

### ai-marketplace

Create and manage an AI plugin marketplace from shared sources, then convert its plugins into distributions for different AI clients. The current build targets Claude Code, Codex and Pi.

This plugin is under construction. The conversion tooling and authoring model are present, while the guided marketplace-management workflow is still incomplete.

See the current [authoring syntax](ai-marketplace/docs/AuthoringSyntax.md) and [host rendering reference](ai-marketplace/docs/HostRendering.md).

## Install

Choose your host's distribution. Each installation page includes the commands for that host; you do not need to build this source repository.

| Host | Installation |
|------|--------------|
| Claude Code | [Claude Code distribution](https://github.com/ZDreamer2/ai-plugins-claude#install) |
| Codex | [Codex distribution](https://github.com/ZDreamer2/ai-plugins-codex#install) |
| Pi | [Pi distribution](https://github.com/ZDreamer2/ai-plugins-pi#install) |

Install either plugin or both. Review their instructions and bundled scripts before use because the workflows can edit files and execute commands.

## First use

After installation, start a new host session in the project you want to work on and invoke the relevant skill with your request:

| Host | Documentation | Marketplace development |
|------|---------------|-------------------------|
| Claude Code | `/ai-doc:ai-doc` | `/ai-marketplace:ai-marketplace` |
| Codex | `$ai-doc:ai-doc` | `$ai-marketplace:ai-marketplace` |
| Pi | `/skill:ai-doc` | `/skill:ai-marketplace` |

## Development and feedback

This is the source repository. The three host repositories are generated distributions; propose changes and report issues here.

See the [maintainer guide](docs/Maintaining.md) for local development and publishing.

## License

Licensed under [0BSD](LICENSE).
