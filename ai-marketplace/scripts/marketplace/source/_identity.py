"""Resolve publishing identity independently of source discovery."""

from dataclasses import replace
from datetime import datetime, tzinfo
from pathlib import Path
import subprocess
from zoneinfo import ZoneInfo

from ._inventory import SourceInventory, SourcePlugin, plugin_name


def _git_log(directory: Path, root: str, format: str) -> str:
    try:
        result = subprocess.run(
            ["git", "log", "-1", f"--format={format}", "--", root, "@common"],
            cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, check=False,
        )
    except OSError:
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def resolve_identity(
    inventory: SourceInventory, *, now: datetime | None = None,
    timezone: tzinfo | None = None,
) -> SourceInventory:
    """Copy raw mappings and resolve defaults from the latest touching commit.

    `now` supplies the no-history clock; naive datetimes use `timezone`.
    Explicit versions still permit automatic author resolution.
    """
    timezone = timezone if timezone is not None else ZoneInfo("Europe/Moscow")
    resolved: list[SourcePlugin] = []
    for plugin in inventory.plugins:
        data = plugin.manifest.copy()
        data["name"] = plugin_name(plugin)
        for seen in resolved:
            if seen.manifest["name"] == data["name"]:
                raise ValueError(
                    f"Plugins '{seen.root}' and '{plugin.root}' "
                    "share the name "
                    f"'{data['name']}': plugin names must be unique."
                )
        author = _git_log(inventory.directory, plugin.root, "%an")
        if data.get("author") is None and author:
            data["author"] = {"name": author}
        version = data.get("version")
        if version is None or version == "AUTO_VERSION":
            timestamp = _git_log(inventory.directory, plugin.root, "%ct")
            if timestamp:
                date = datetime.fromtimestamp(int(timestamp), timezone)
            else:
                date = now if now is not None else datetime.now(timezone)
                date = (
                    date.replace(tzinfo=timezone) if date.tzinfo is None
                    else date.astimezone(timezone)
                )
            # Normalize complete SemVer components, not the embedded HHMMSS.
            data["version"] = ".".join(
                str(int(part)) for part in date.strftime("%y.%m.%d%H%M%S").split(".")
            )
        resolved.append(replace(plugin, manifest=data))
    return replace(inventory, plugins=tuple(resolved))
