# Marketplace planning guidance authoring context

[on-plan.md](on-plan.md) maps marketplace and plugin responsibilities to directories and file roles. It serves any marketplace adopting this CodebaseType. Workspace guidance identifies concrete marketplaces and routes their changes here.

## Authoring sources

- [BaseDoc format](AI_DOC_PLUGIN/Formats/BaseDoc/BaseDoc.format.md) and [StartSimple](AI_DOC_PLUGIN/Theory/StartSimple.md) govern the document's form and scope.

Keep `on-plan.md` declarative, with both marketplace and unit structure. The `python/` guides own detailed Python conventions. Build and review instructions belong in their own phase entries.

`@common/` is a standard of this CodebaseType: the marketplace owns shared sources there, and consuming plugins expose them through a plugin-local `@common/`. Its `docs/` and `scripts/` folders organize shared guidance and executable code. The SDK namespace and the mechanism supplying the plugin-local resources remain marketplace-specific.

Distinguish reusable organization from a concrete marketplace's choices. Plugin inventories, role-folder names, manifest formats, SDK namespaces, supported hosts, dependency provisioning, commands and deployment policies belong to the concrete marketplace. Practical guidance MUST NOT require one marketplace's authoring or build guide as a universal prerequisite. Examples use neutral names and do not establish a required namespace or distribution mechanism.
