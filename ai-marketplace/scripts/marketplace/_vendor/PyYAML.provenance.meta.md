# PyYAML.provenance.meta.md

Specification for creating and editing [PyYAML provenance](PyYAML.provenance.md).

## PyYAML.provenance.md goals and principles

- Enables maintainers to verify and replace the privately bundled dependency while retaining standalone plugin execution.
- Distinguishes upstream implementation from the library's Symfony compatibility policy, so dependency updates preserve the ownership boundary.
- Keeps the upstream license and reproducible archive identity available to maintainers.

## AiDocFormat

[BaseDoc format](AI_DOC_PLUGIN/Formats/BaseDoc/BaseDoc.format.md)

## MUST read before editing PyYAML.provenance.md

- [StartSimple methodology](AI_DOC_PLUGIN/Theory/StartSimple.md) - Keeps maintenance guidance focused on the established replacement task.
- `ai-marketplace/scripts/marketplace/_vendor/yaml/__init__.py` and `ai-marketplace/scripts/marketplace/_yaml.py` - Establish the import adaptation and compatibility boundary the provenance records.
- [Official PyYAML releases](https://pypi.org/project/PyYAML/) - Own archive identity and upstream release details.

## PyYAML.provenance.md typical use context

### 💡 Distinct usage patterns for PyYAML.provenance.md

#### Dependency maintenance

Maintainer inspects the bundled parser -> loads this provenance beside its license before verifying or replacing the snapshot.

### Role PyYAML.provenance.md serves during use

- Supplies the reproducible source and local adaptation record for the dependency.
