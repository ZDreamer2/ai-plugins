# Host Rendering for zd-plugins

The build renders shared plugin sources for Claude Code, Codex and Pi. Use this reference when deciding how content behaves in each host; [authoring syntax](AuthoringSyntax.md) owns the rules for writing it. Development lifecycle and testing procedures belong to the consuming marketplace's guidance.

## Generated metadata

`ai-plugin.yml` is the only hand-written plugin manifest. The build resolves its identity once and generates:

| Host | Per-plugin metadata | Root registry |
|------|---------------------|---------------|
| Claude Code | `.claude-plugin/plugin.json`: the resolved manifest, including additional source keys | `.claude-plugin/marketplace.json` |
| Codex | `.codex-plugin/plugin.json`: `name`, `version`, `description`, `author`, plus `"skills": "./skills/"` when that folder exists | `.agents/plugins/marketplace.json` |
| Pi | `package.json`: package identity and explicit skill/extension entry points; `.pi-plugin/plugin.json`: resolved name and version for bundled scripts | None; each plugin is an independent package |

Additional manifest keys such as `hooks`, `mcpServers` and `lsp` pass through to Claude metadata unchanged. Codex and Pi metadata carry only their fixed generated fields; Pi packages do not activate Claude hook configuration.

A Pi package with one skill has this shape:

```json
{
  "name": "@zdreamer2/pi-plugin-<plugin-name>",
  "version": "<resolved version>",
  "description": "<manifest description>",
  "keywords": ["pi-package"],
  "pi": {
    "skills": ["./skills/<skill>"]
  }
}
```

`pi.skills` explicitly lists published skill directories under `skills/`. If present, extension entry points at `extensions/*/index.js`, `index.mjs` or `index.ts` are listed in `pi.extensions`. Workflows, scripts and materialized `@common` resources retain their source layout.

## Skill frontmatter and identity

| Source field | Claude Code | Codex | Pi |
|--------------|-------------|-------|----|
| `name` | Kept | Kept; invocation uses `$plugin:skill` | Rewritten to the namespaced name below |
| `description` | Kept | Kept; argument hint appended | Kept unchanged |
| `argument-hint` | Usage hint | Folded into description as `Usage: $plugin:skill <hint>.` | Dropped |
| `disable-model-invocation` | Controls automatic invocation | `true` generates `agents/openai.yaml` with `policy.allow_implicit_invocation: false` | Kept |
| `user-invocable` | Controls direct invocation | Dropped | Dropped |
| Other fields | Kept | Dropped; non-default unsupported values reported | Keeps `license`, `compatibility`, `metadata`, `allowed-tools`; drops other fields |

Descriptions are the routing signal Codex and Pi use before loading a skill. Codex folds the hint into that signal; Pi does not. Do not hand-write the generated Codex `agents/openai.yaml`: the build fails on a collision.

Pi uses the resolved manifest name as the namespace. A same-named hub skill keeps that name (`crm` -> `/skill:crm`); other skills receive the plugin prefix (`forge` + `load` -> `/skill:forge-load`). A plugin directory name that differs from its manifest name is not an alias.

Before writing any tree, the build rejects invalid, duplicate or overlength Pi skill names. Names use lowercase letters, numbers and single hyphens, with a 64-character limit. It also rejects missing or malformed frontmatter, a source name differing from the skill directory, empty instructions, missing descriptions and descriptions over 1024 characters.

## Document and script paths

Claude and Codex load installed caches; project-local Pi loads generated package roots. Document-relative links work in each location, including inside a plugin's bundled `@common` folder. Ordinary document links and agent-executed script paths pass through the builder unchanged.

The agent reads linked context explicitly when needed and resolves script paths from the containing document to quoted absolute paths, retaining the task's working directory. This supports reuse of sufficient, current context on repeated skill use without depending on source-checkout paths or another plugin's installation.

## Agent placeholders

Tools and skill invocations have different host names. These markers own the whole operation or invocation, not just its prefix. The extra `$` keeps the examples literal in this rendered reference:

| Marker shown literally | Claude output | Codex output | Pi output |
|-----------------------|---------------|--------------|-----------|
| `$${AGENT_SUBAGENT_TOOL}` | `Agent` | `spawn_agent` | `subagent` |
| `$${AGENT_FORK}` | the Agent tool with `subagent_type: fork` | `spawn_agent` with `fork_turns: "all"` | `subagent` with `context: "fork"` and `model: "inherit"` |
| `$${AGENT_SUBAGENT_FOLLOWUP_TOOL}` | `SendMessage` | `followup_task` | `subagent` with `steer` for a running child or `resume` for a completed child |
| `$${AGENT_QUESTION_TOOL}` | `AskUserQuestion` | `request_user_input_async` | `ask_user_question` |
| `$${AGENT_SKILL(example)}` | `/example` | `$example:example` | `/skill:example` |
| `$${AGENT_SKILL(example:run)}` | `/example:run` | `$example:run` | `/skill:example-run` |

The fork marker also renders a gloss explaining inherited parent context. It owns a whole phrase because hosts express the fork through different arguments; substituting a tool name alone would not specify the operation.

The vocabulary covers only constructs with deliberate supported renderings. `TaskCreate`, model aliases and fixed-kind workers such as `subagent_type: claude` remain literal. A fixed-kind worker is not a context-inheriting fork.

Adding a placeholder or include marker is a build change: maintain the Python renderers at `ai-marketplace/scripts/marketplace/build/rendering/_placeholders.py` and `_includes.py` in the marketplace checkout. Update this reference and [authoring syntax](AuthoringSyntax.md), and check affected renderings for every host, including Claude.

## Agent includes

`$${AGENT_INCLUDE_DOC(../../docs/includes/example.md)}` splices a document into every supported tree. `$${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/includes/example.md)}` splices it only into the named tree and removes the marker line from the others. Includes embed short instructions needed at entry without a separate read; ordinary linked context avoids loading larger or task-specific documents in every invocation.

Includes are one level deep. The included document is also published on its own, and its placeholders resolve normally. Relative Markdown links and images, including reference definitions, are rebased from its consuming plugin-local location to preserve their targets in the including document. Code examples and literal paths remain unchanged; agent-executed commands use the including document as their base. Files without includes pass through this stage byte-for-byte. The placement and validation rules are in [authoring syntax](AuthoringSyntax.md#agent-includes).

## Runtime and host-specific behavior

Hook configuration retains `${CLAUDE_PLUGIN_ROOT}` literally: the host supplies the installed plugin root when executing the hook. Configuration files are copied without Markdown rendering. Host variables belong where the host expands them, rather than in document references or agent-executed commands.

Claude skill text can use `$ARGUMENTS` for invocation arguments, `$ARGUMENTS[N]` or `$N` for indexed arguments, and `${CLAUDE_SESSION_ID}` for the session identifier. Codex and Pi do not substitute these values in skill text. Pi does not emulate `${CLAUDE_PLUGIN_ROOT}`. Host-specific MCP naming and configuration belong to the target integration rather than the generic skill format.

## Construct reports

The build writes `codex-report.md` and `pi-report.md` beside the generated trees. They list constructs left literal, grouped by plugin or shared origin, with file and line:

- Codex: host variables, tool names, skill invocation wording, `AI_DOC_PLUGIN` references and dropped frontmatter.
- Pi: host-specific invocations, tools, variables and roots, and cross-plugin references.

Reports scan skills, supporting documents, examples and meta documents. Their lexical finding counts are not counts of broken skills: they are adaptation backlogs, not build gates. Reports remain outside published build repositories; CI keeps them in the pipeline artifact.

Output inspection and host acceptance follow the consuming marketplace's testing procedures.
