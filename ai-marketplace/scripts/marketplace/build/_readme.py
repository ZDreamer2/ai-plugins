"""Render optional consumer README configuration before replacing host trees."""

import json
from pathlib import Path
from string import Template


HOST_NAMES = {"claude": "Claude Code", "codex": "Codex", "pi": "Pi"}


def distribution_readmes(source: Path) -> dict[str, str]:
    """Use a shared template when .marketplace/readme.json is present.

    Marketplaces without configuration retain their ordinary root README copy.
    All supported hosts are required so a malformed configuration fails before
    any output is replaced, including during dry runs.
    """
    config_path = source / ".marketplace/readme.json"
    if not config_path.exists():
        return {}
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("expected an object")
        values = {key: config[key] for key in ("marketplace", "source_url")}
        installations = config["installation"]
        if not isinstance(installations, dict):
            raise ValueError("installation must be an object")
        values.update({host: installations[host] for host in HOST_NAMES})
        if any(not isinstance(value, str) or not value.strip()
               for value in values.values()):
            raise ValueError(
                "marketplace, source_url and installations must be nonempty strings"
            )
    except (KeyError, ValueError, TypeError) as error:
        raise ValueError(
            f"Invalid distribution README config '{config_path}': {error}"
        ) from error
    template = Template(
        (Path(__file__).parent / "templates/README.md").read_text(encoding="utf-8")
    )
    return {
        host: template.substitute(
            marketplace=values["marketplace"], host=name,
            source_url=values["source_url"], installation=values[host].strip(),
        )
        for host, name in HOST_NAMES.items()
    }
