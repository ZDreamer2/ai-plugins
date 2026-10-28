# Python unit conventions

A Python unit is a package with a cohesive responsibility. Its owner determines its location: plugin-local libraries stay with the plugin; cross-plugin libraries live under the marketplace's `@common/scripts/`, with an import namespace chosen by that marketplace. [Python file conventions](PythonFile.md) govern implementation style.

## Comprehensive Example

```text
<package>/
  __init__.py                 # Public API, usage docstring and exports
  model.py                    # Class-based implementation
  _operations.py              # Function-oriented implementation
  child/                      # Separately consumable nested unit
    __init__.py               # Child's public API, docstring and exports
    child.py                  # Child's implementation
    tests/                    # Child's tests and fixtures
  tests/                      # Parent's tests and fixtures
```

## Public API

`__init__.py` contains an `Intent:` docstring describing the responsibility, a `Usage:` section showing imports and calls, and an explicit `__all__` list. It exposes selected implementations through re-exports or small wrappers.

For example, a serialization package can expose `loads` and `dumps` while keeping parsing and formatting in private modules. The public API describes the capability; consumers need no knowledge of those modules.

## Nested units

A child package with its own consumable responsibility is a unit with its own public API and tests. Nesting expresses ownership; consumers can import the child's public API directly without forwarding every operation through the parent. A helper subpackage used only to implement its parent remains private rather than becoming a separately consumable unit.

## Implementation

Split implementation modules by cohesive responsibility. Function-oriented private modules use an `_` prefix. Class-based packages use descriptive snake_case module names, such as `chunk_folder.py` for `ChunkFolder`, and can expose collaborating components through a central class. Shared state belongs to an explicit context passed to those components.

## Tests

The marketplace's test tooling determines discovery and invocation; test dependencies follow its dependency policy.

## Rules

- MUST access another unit through its public API; implementation modules remain private regardless of their filenames.
- MUST place tests and fixtures in the owning unit's `tests/` directory, including for nested units, and test through that unit's public API.
