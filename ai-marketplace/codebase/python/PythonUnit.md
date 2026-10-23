# Python unit conventions

A Python unit is a package with a cohesive responsibility. Its owner determines its location: plugin-local libraries stay with the plugin; cross-plugin libraries live under the marketplace's `@common/scripts/`, with an import namespace chosen by that marketplace. [Python file conventions](PythonFile.md) govern implementation style.

## Package structure

```text
<package>/
  __init__.py                 # Public API, usage docstring and exports
  _<concern>.py               # Private implementation modules
  tests/                     # Tests and fixtures
```

External consumers enter through the package API. Implementation modules remain private regardless of their filenames.

## Public API

`__init__.py` contains an `Intent:` docstring describing the responsibility, a `Usage:` section showing imports and calls, and an explicit `__all__` list. It exposes selected implementations through re-exports or small wrappers.

For example, a serialization package can expose `loads` and `dumps` while keeping parsing and formatting in private modules. The public API describes the capability; consumers need no knowledge of those modules.

## Implementation

Split implementation modules by cohesive responsibility. Function-oriented private modules use an `_` prefix. Class-based packages can use descriptive module names and a central class that exposes collaborating components. Shared state belongs to an explicit context passed to those components.

## Tests

Tests live in the package's `tests/` directory, with fixtures beside the tests that use them. Test the package through its public API. The marketplace's test tooling determines discovery and invocation; test dependencies follow its dependency policy.
