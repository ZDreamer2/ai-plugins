# PythonUnit.meta.md

Specification for creating and editing [Python unit conventions](PythonUnit.md). Defines purpose, usage patterns, and constraints.

## PythonUnit.md goals and principles

- Gives marketplace planners and builders a shared model for cohesive Python packages, so implementation, public APIs and tests have clear owners.
- Distinguishes ownership nesting from implementation privacy; otherwise a nested unit can become a private helper by accident or acquire needless parent forwarding APIs.
- Remains reusable across marketplaces. Concrete namespaces, runtime provisioning and test commands belong to each marketplace, not this guide.

## AiDocFormat

[CodeDoc format](AI_DOC_PLUGIN/Formats/CodeDoc/CodeDoc.format.md)

## MUST read before editing PythonUnit.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps conventions focused on established organization needs rather than a general-purpose package framework.
- [Python file conventions](PythonFile.md) - Owns naming, imports and dependency rules that package guidance builds on.

## PythonUnit.md typical use context

### 💡 Distinct usage patterns for PythonUnit.md

#### Loaded through marketplace codebase guidance

Marketplace planning or build guidance -> Python package structure or public API work -> this guide supplies unit organization conventions.

#### Direct package-structure review

`Review our Python library structure against PythonUnit.md.`

### Role PythonUnit.md serves during use

- Defines package ownership and public API boundaries, including independently consumable nested units.
- Places implementation and tests without prescribing one marketplace's runtime or domain architecture.
