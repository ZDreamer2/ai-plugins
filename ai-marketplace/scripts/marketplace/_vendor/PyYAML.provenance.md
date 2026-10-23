# Bundled PyYAML provenance

The marketplace library bundles [PyYAML 6.0.2](https://pypi.org/project/PyYAML/6.0.2/) under its private `marketplace._vendor.yaml` namespace. Source-checkout and installed-plugin execution use this copy without pip, global `yaml` or LibYAML.

## Verified source

- [Official source archive](https://files.pythonhosted.org/packages/54/ed/79a089b6be93607fa5cdaedf301d7dfb23af5f25c398d5ead2525b063e17/pyyaml-6.0.2.tar.gz): `pyyaml-6.0.2.tar.gz`.
- SHA-256: `d584d9ec91ad65861cc08d42e834324ef890a082e591037abe114850ff7bbc3e`.
- Copied implementation: `pyyaml-6.0.2/lib/yaml/*.py`, excluding `cyaml.py`, into `yaml/` beside this document.
- Upstream `LICENSE` is retained verbatim as `PyYAML.LICENSE` beside this document.

## Local boundary

All copied modules retain their upstream bytes except `yaml/__init__.py`: the optional `.cyaml` import block is replaced with `__with_libyaml__ = False`. The omitted `cyaml.py` is the optional native accelerator facade, which imports global `yaml._yaml`. Pure-Python modules already use package-relative imports.

Symfony-compatible parsing and bounded default emission belong to the local marketplace compatibility modules `../_yaml.py` and `../_yaml_dump.py`. Changes to scalar, tag, mapping, error and formatting policy stay outside the upstream snapshot. The public API exposes `parse_yaml` and `dump_yaml`; upstream dumping APIs remain private dependency implementation.

## Replacement

1. Download the selected official source archive and verify its published SHA-256 before extraction. Record the release, archive URL and checksum here.
2. Replace `yaml/` with the archive's `lib/yaml` Python files, excluding the native accelerator facade. Copy the upstream license verbatim to `PyYAML.LICENSE`.
3. In the new `yaml/__init__.py`, replace the optional `.cyaml` import and availability-detection block with `__with_libyaml__ = False`. Verify every other copied file against the archive; record any additional import adaptation here.
4. Run the public parsing and emission fixtures, source, syntax-checker and adapter tests. They cover Symfony compatibility and isolated plugin execution without site packages, including a conflicting global `yaml` package. Keep semantic and formatting corrections in the compatibility wrapper.

From this marketplace root, the owning test roots are `marketplace/tests`, `marketplace/source/tests` and `marketplace/validation/tests` under `ai-marketplace/scripts`, plus `ai-marketplace/codebase/tests`. Package tests use `python3 -B -S -m unittest discover -s <test-root> -t ai-marketplace/scripts -v`; adapter tests omit `-t`. The [marketplace README](../../../../README.md) lists all owning suites.
