"""Carry rendered content and unwritten file companions to the tree owner."""

from dataclasses import dataclass, field

from ._constructs import CodexConstructFinding, PiConstructFinding


@dataclass
class FileRendering:
    """Extra paths are relative to the rendered document's own folder."""

    content: str
    extra_files: dict[str, str] = field(default_factory=dict)
    findings: list[CodexConstructFinding | PiConstructFinding] = field(default_factory=list)
