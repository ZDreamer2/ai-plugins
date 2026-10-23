# Marketplace plan review

Check that the plan places the capability with its owning plugin, keeps Python functionality shared across plugins behind a shared package API and preserves installed-plugin dependencies. A source-checkout sibling path alone does not make a dependency available after installation.

For documentation changes, check that the plan identifies authoritative documents and applicable formats, preserves companion metas and updates live references when moving knowledge. For Python work, check package and script boundaries against [Python units](python/PythonUnit.md) and [Python files](python/PythonFile.md).

Evaluate verification against the behavior or distribution contract the change affects. Each proposed check should address a concrete failure it could detect; avoid expanding scope solely because a manifest, shared file or package was touched. Require artifact or host acceptance when the affected contract cannot be established by source inspection or focused tests, or when the project explicitly requires it.

Package tests belong in the package's `tests/`; plugin script tests belong beside those scripts. Syntax checks alone do not establish behavioral correctness or successful packaging.
