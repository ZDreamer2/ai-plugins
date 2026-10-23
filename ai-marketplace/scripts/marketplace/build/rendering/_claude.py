"""Produce Claude mappings from the caller's resolved source identities."""

from copy import deepcopy
from typing import Any

from marketplace.source import SourceInventory, SourcePlugin


def claude_plugin_metadata(plugin: SourcePlugin) -> dict[str, Any]:
    return deepcopy(plugin.manifest)


def claude_marketplace_metadata(
    inventory: SourceInventory,
) -> dict[str, Any]:
    return {
        "name": "zd-plugins",
        "owner": {"name": "ZDreamer2"},
        "metadata": {"description": "AI documentation and marketplace authoring plugins"},
        "plugins": [
            {
                "name": deepcopy(plugin.manifest["name"]),
                "source": "./" if plugin.root == "." else "./" + plugin.root,
                "description": deepcopy(plugin.manifest.get("description")),
            }
            for plugin in inventory.plugins
        ],
    }
