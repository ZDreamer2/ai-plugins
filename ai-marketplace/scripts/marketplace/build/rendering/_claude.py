"""Produce Claude mappings from the caller's resolved source identities."""

from copy import deepcopy
from typing import Any

from marketplace.source import MarketplaceIdentity, SourceInventory, SourcePlugin


def claude_plugin_metadata(plugin: SourcePlugin) -> dict[str, Any]:
    return deepcopy(plugin.manifest)


def claude_marketplace_metadata(
    inventory: SourceInventory, identity: MarketplaceIdentity = MarketplaceIdentity(),
) -> dict[str, Any]:
    return {
        "name": identity.name,
        "owner": {"name": identity.owner},
        "metadata": {"description": identity.description},
        "plugins": [
            {
                "name": deepcopy(plugin.manifest["name"]),
                "source": "./" if plugin.root == "." else "./" + plugin.root,
                "description": deepcopy(plugin.manifest.get("description")),
            }
            for plugin in inventory.plugins
        ],
    }
