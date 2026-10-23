# Python file conventions

Python libraries and scripts follow PEP 8 naming and style.

## Types and imports

Use type hints on function signatures. Annotation syntax and evaluation follow the supported Python runtime and any runtime type-inspection requirements.

Group standard-library, third-party and local imports separately. Consumers import other packages through their public APIs; internal modules use local implementation imports.

## Dependencies

A distributed script's imports MUST be available in its installed execution environment. Dependency provisioning belongs to the marketplace: bundled libraries, vendored dependencies or an explicitly managed runtime can provide it. A dependency available only in the developer's checkout does not satisfy that contract.

Third-party implementation details stay behind the owning library's API when consumers do not need them.

## Docstrings

Module docstrings state intent; class docstrings explain design role. Document behavior that names and types do not convey. Package-level usage belongs in the public API docstring described by [Python units](PythonUnit.md).
