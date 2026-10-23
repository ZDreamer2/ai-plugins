# AI plugins marketplace

A marketplace catalogs and distributes plugins. Each plugin owns a capability delivered through agent instructions, configuration and supporting tools. A source marketplace can produce distributions for several agent hosts.

This guidance defines reusable organization conventions. The concrete marketplace supplies its plugin locations, manifest format, shared-library namespace, supported hosts and toolchain.

## Marketplace organization

```text
marketplace/
  <plugin>/                   # Independently installable capability
  <group>/<plugin>/           # Optional grouping of plugins
  @common/                    # Content reused across plugins
    docs/                     # Shared guidance
    scripts/                  # Shared scripts and Python libraries
```

Grouping organizes discovery; the plugin remains the installation and ownership boundary. Plugin identifiers are unique within the marketplace. The marketplace-root `@common/` owns content shared across plugins. Each consuming plugin exposes that content through its own `@common/`, preserving plugin-local references after installation. The packaging mechanism determines how the shared content reaches that location.

Source manifests and any generated host manifests or catalog entries have distinct roles. Generated artifacts belong to the distribution process; authoring targets their sources.

## Plugin unit

```text
plugin/
  <manifest>                  # Plugin identity and host configuration
  skills/<name>/SKILL.md      # Skill routing metadata and entry instructions
  workflows/                  # Workflows shared at plugin scope
  docs/                       # Practical guidance
  scripts/                    # Plugin-owned tools
    tests/                    # Tests of those tools
  @common/                    # Shared resources used by this plugin
```

Supporting files live with the narrowest skill, workflow or plugin that owns them. Directories appear as their responsibilities are needed. Specialized document collections can have their own folders.

`SKILL.md` is the invocation entry; supporting workflows own the detailed procedure. Markdown instructions and their bundled scripts form one capability even when they use different languages. Installed plugins retain the documents, scripts and other resources their capabilities require. A path into a sibling source plugin does not establish an installed dependency.

## Python libraries and scripts

Scripts own command-line adaptation and workflow-specific behavior. Libraries own reusable functionality behind a public package API. Helpers used only within one plugin stay with that plugin; Python libraries shared across plugins live under the marketplace's `@common/scripts/`. Their import namespace is marketplace-specific.

```text
<library-root>/<package>/
  __init__.py                 # Public API, usage docstring and exports
  _<concern>.py               # Private implementation modules
  tests/                     # Tests and fixtures
```

The package boundary is independent of how the distribution makes it importable. [Python units](python/PythonUnit.md) defines package organization; [Python files](python/PythonFile.md) defines implementation conventions. Dependency provisioning and the import bootstrap belong to the concrete marketplace's runtime contract.

## Documentation

Practical documents guide the agent doing the task. A companion `<name>.meta.md` supplies authoring context and is read when editing that document. Ai-doc supplies document formats and editing workflows; meta documents outside ai-doc refer to its content through `AI_DOC_PLUGIN/...`.

Reusable codebase conventions live in codebase guidance. A particular plugin's workflow and domain knowledge stay with that plugin. Marketplace inventories, deployment details and tool commands belong to the concrete marketplace's documentation.

## Evaluate based on task

- [Python units](python/PythonUnit.md) - creating or changing a Python package, its public API or tests.
- [Python files](python/PythonFile.md) - implementing Python libraries or scripts.
