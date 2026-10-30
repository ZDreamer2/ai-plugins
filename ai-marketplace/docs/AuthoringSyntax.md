# Marketplace Markdown authoring syntax

Write plugin Markdown once using the shared syntax below. The build adapts it for supported agents. Choose an agent only when an instruction genuinely needs an agent-specific include or feature; [host rendering](HostRendering.md) explains the rendered outputs.

## Skill frontmatter

- `SKILL.md` MUST set `name` and `description`; keep the description concise, specific and sufficient on its own to decide when to use the skill
- `argument-hint` is OPTIONAL; write it as plain text, never as a YAML list
- `user-invocable` controls direct user invocation; `disable-model-invocation` restricts automatic selection where supported

## Editing-only frontmatter

- Markdown documents MAY use `edit-only-context` with a YAML string path to a meta or format document. Resolve it relative to the containing document; references to ai-doc from outside that plugin use `AI_DOC_PLUGIN/...`
- This property is for editing only. The build removes it before expanding includes in every host tree, preserving other frontmatter properties and removing the entire frontmatter when no properties remain

## Document references

- References to Markdown documents in the same project or plugin use paths relative to the referencing document's directory, including `SKILL.md`, workflows and meta files
- Write document references as Markdown links with concise labels identifying the target's subject or role. Keep destinations out of backticks; use backticks for literal paths, filenames, commands, syntax examples and references to other file types
- Project code references use paths from the project root, such as `src/example.py`
- Required vs optional reading is carried by the section or sentence: `MUST read` requires reading, `MAY read` makes it optional, and an `IF ... THEN` reference is required only when the condition applies. A link alone neither loads its target nor requires reading
- MUST NOT use `@path` context injection anywhere, including `SKILL.md` and supporting documents. Read referenced context explicitly when needed and reuse content already available in the session when sufficient and current
- When reading, retain the referencing document's full path, resolve references using their documented bases and pass the resolved full path to file tools, regardless of the shell working directory
- Bundled dependencies of documents used from installed plugins stay within that plugin. Shared documents are reached through its local `@common/` copy using document-relative paths; links between documents within `@common/` remain relative within that tree. Source meta documents follow the rules below
- Directory references use backticked paths relative to the containing document. Literal checkout paths in build commands, configuration and examples keep their required base

### References in meta files

- Source meta documents may reference the entire marketplace repository, including sibling plugins. Markdown links and directory references use the containing meta document's directory as their base
- Code and other non-Markdown files within the marketplace use paths from the marketplace repository root, such as `tools/example/scripts/run.py` or `@common/scripts/run.py`. References outside the marketplace retain the owning project's path convention
- A meta document outside ai-doc MUST reference ai-doc content with `AI_DOC_PLUGIN/path.md`, for example `[CodeDoc format](AI_DOC_PLUGIN/Formats/CodeDoc/CodeDoc.format.md)`. Ai-doc editing workflows resolve the prefix from the ai-doc plugin root; it is not a filesystem directory
- Meta documents inside ai-doc use document-relative links

## Agent-executed commands

- Commands needed at skill start MUST be explicit agent-run steps; MUST NOT use `` !`command` `` load-time execution
- Bundled script paths in commands the agent reads and executes MUST be relative to the containing document, including paths within `@common/`
- Resolve bundled script paths to absolute paths before execution, quote the resolved paths, and keep the task’s working directory; command arguments retain their own documented path bases
- State local path-resolution instructions only when they differ from this default
- For example, a plugin's `docs/Task.md` invokes `../scripts/run.py` after resolving that path from its own directory
- Automatically executed hooks and configuration commands use their host’s runtime path resolution

## Agent placeholders

Use these markers for agent operations and skill invocations in shared Markdown. The examples use an extra `$` so they remain literal after rendering; actionable source instructions use one `$`.

| Marker shown literally | Meaning |
|---|---|
| `$${AGENT_SUBAGENT_TOOL}` | Tool for delegating to a subagent |
| `$${AGENT_FORK}` | Fork inheriting the parent agent's context; use it as a whole phrase |
| `$${AGENT_SUBAGENT_FOLLOWUP_TOOL}` | Tool for following up with an existing subagent |
| `$${AGENT_QUESTION_TOOL}` | Tool for asking the user a question |
| `$${AGENT_SKILL(example)}` | Invocation of the `example` plugin's hub skill |
| `$${AGENT_SKILL(example:run)}` | Invocation of its `run` skill |

- Substituted in every markdown file, inside backticks and fences included
- A marker the build cannot resolve fails the build: an unknown name, a missing, empty or malformed argument, an argument on a placeholder that takes none
- The argument of `$${AGENT_SKILL(...)}` uses the resolved `ai-plugin.yml` name and an existing skill: `plugin:skill`, or the bare plugin name for its same-named hub skill. A plugin folder name is not an alias for a different manifest name
- `$${AGENT_FORK}` stands for a whole phrase rather than a tool name: the sentence around it says only what the fork is for, never what a fork is or which tool runs it
- MUST NOT put an invocation marker inside a double-quoted shell command or inside a prompt addressed to another agent (such as a sub-agent of a fixed kind): the reader of that text is not the agent holding the document. Write those invocations literally
- To show a marker as written, escape it with a second `$`: `$$${AGENT_SKILL(example)}` renders as `$${AGENT_SKILL(example)}` in every tree
- Adding a placeholder requires a corresponding renderer change

## Agent includes

The build replaces an include's line with a document's lines. Include shared instructions in every supported tree:

```markdown
$${AGENT_INCLUDE_DOC(../../docs/includes/example.md)}
```

For instructions specific to one agent, name its tree; the build removes the marker line from other trees:

```markdown
$${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/includes/example.md)}
```

- The document path names a `.md` file relative to the including document and stays inside the marketplace source root supplied to the build. It may reach canonical sources outside the consuming plugin; build from the marketplace root when using these includes. Host-specific includes take an agent tree, `claude`, `codex` or `pi`, followed by that path
- The marker stands alone on its line, apart from surrounding whitespace
- For host-specific includes, leave no blank line before the marker and keep the usual one after it: the tree that drops the marker then has the spacing the file would have without the include
- The included text becomes part of the including document; its placeholders resolve normally. Write Markdown link and image destinations relative to the included file: the build rebases them, including reference definitions, for the including document. For a source outside the consuming plugin, relative link/image targets MUST be existing files inside that plugin's logical tree; expose runtime dependencies there rather than linking to unbundled marketplace sources. Link syntax inside code stays literal
- Literal paths and agent-executed commands in included text use the including document as their base. Name that base in the included text where needed
- The build fails on a marker sharing its line with other text, an unknown tree, a path that is not a readable `.md` file inside the marketplace source, an external include with a relative link/image target outside the plugin or missing there, a marker inside the leading YAML frontmatter, and an include inside an included document
- A second `$` escapes an include as it does any other marker
- Including a document does not add it to the plugin's published files. Plugin-local documents are still published normally; marketplace-only INCLUDE sources need no plugin-local copy or symlink
- Include text the agent needs before it can be told to read anything, such as how to run a skill's commands; elsewhere a link serves. A difference inside a sentence is a placeholder's job
