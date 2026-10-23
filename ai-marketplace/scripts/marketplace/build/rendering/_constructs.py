"""Find literal host constructs in final Codex and Pi Markdown."""

from dataclasses import dataclass
from enum import Enum
import re

from marketplace.source import (
    SourceInventory, codex_skill_names, pi_source_skill_names,
)


class CodexConstruct(Enum):
    """Adaptation decisions, in the order used by the Codex report."""

    CLAUDE_VARIABLE = "claude_variable"
    CLAUDE_TOOL = "claude_tool"
    SKILL_INVOCATION = "skill_invocation"
    CROSS_PLUGIN_REFERENCE = "cross_plugin_reference"
    SKILL_FRONTMATTER = "skill_frontmatter"

    def title(self) -> str:
        return {
            self.CLAUDE_VARIABLE: "Claude variables",
            self.CLAUDE_TOOL: "Claude tool names and arguments",
            self.SKILL_INVOCATION: "Skill invocation wording",
            self.CROSS_PLUGIN_REFERENCE: "Cross-plugin references",
            self.SKILL_FRONTMATTER: "Skill frontmatter",
        }[self]


@dataclass(frozen=True)
class CodexConstructFinding:
    """One match; frontmatter lines refer to source, other lines to output."""

    category: CodexConstruct
    line: int
    text: str


class PiConstruct(Enum):
    """Adaptation decisions, in the order used by the Pi report."""

    HOST_VARIABLE = "host_variable"
    HOST_TOOL = "host_tool"
    SKILL_INVOCATION = "skill_invocation"
    CROSS_PLUGIN_REFERENCE = "cross_plugin_reference"

    def title(self) -> str:
        return {
            self.HOST_VARIABLE: "Host variables and roots",
            self.HOST_TOOL: "Host tool names and arguments",
            self.SKILL_INVOCATION: "Skill invocation wording",
            self.CROSS_PLUGIN_REFERENCE: "Cross-plugin references",
        }[self]


@dataclass(frozen=True)
class PiConstructFinding:
    """One construct left literal, with its rendered Pi line number."""

    category: PiConstruct
    line: int
    text: str


_TOOL_NAMES = (
    "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList", "TodoWrite",
    "EnterPlanMode", "ExitPlanMode", "SendMessage", "Agent tool",
    "subagent_type", "general-purpose", "--model", "model sonnet",
    "model opus", "model haiku",
)

_PATTERNS = (
    (CodexConstruct.CLAUDE_VARIABLE,
     re.compile(r"\$\{CLAUDE_[A-Z_]+\}|\$ARGUMENTS")),
    (CodexConstruct.CLAUDE_TOOL, re.compile(
        r"(?<![A-Za-z0-9_-])(?:"
        + "|".join(re.escape(term) for term in _TOOL_NAMES)
        + r")(?![A-Za-z0-9_-])",
    )),
    (CodexConstruct.SKILL_INVOCATION,
     re.compile(r"slash[- ]commands?", re.IGNORECASE | re.ASCII)),
)
_CROSS_PLUGIN = re.compile(r"AI_DOC_PLUGIN/\S*", re.ASCII)

_PI_TOOL_NAMES = (
    "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList", "TodoWrite",
    "EnterPlanMode", "ExitPlanMode", "SendMessage", "Agent tool",
    "spawn_agent", "followup_task", "subagent_type", "fork_turns",
)
_PI_PATTERNS = (
    (PiConstruct.HOST_VARIABLE, re.compile(
        r"\$\{(?:CLAUDE|CODEX)_[A-Z_]+\}|"
        r"\$(?:ARGUMENTS|CODEX_HOME|[0-9]+)(?![A-Za-z0-9_])",
    )),
    (PiConstruct.HOST_TOOL, re.compile(
        r"(?<![A-Za-z0-9_-])(?:"
        + "|".join(re.escape(term) for term in _PI_TOOL_NAMES)
        + r")(?![A-Za-z0-9_-])",
    )),
    (PiConstruct.SKILL_INVOCATION,
     re.compile(r"slash[- ]commands?", re.IGNORECASE | re.ASCII)),
    (PiConstruct.CROSS_PLUGIN_REFERENCE, _CROSS_PLUGIN),
)


def _slash_pattern(names: list[str]) -> re.Pattern[str]:
    return re.compile(
        r"(?<![A-Za-z0-9_/.-])/(?:"
        + "|".join(re.escape(name) for name in names)
        + r")(?![A-Za-z0-9_/-])(?!\.[A-Za-z0-9])",
    )


def scan_codex(
    content: str, inventory: SourceInventory,
) -> list[CodexConstructFinding]:
    """Report every match, including examples and duplicates, in LF line order."""
    names = sorted(
        codex_skill_names(inventory),
        key=lambda name: len(name.encode("utf-8", "surrogateescape")),
        reverse=True,
    )
    patterns = list(_PATTERNS)
    if names:
        patterns.append((CodexConstruct.SKILL_INVOCATION, _slash_pattern(names)))
    patterns.append((CodexConstruct.CROSS_PLUGIN_REFERENCE, _CROSS_PLUGIN))
    return [
        CodexConstructFinding(category, index, match.group())
        for index, line in enumerate(content.split("\n"), start=1)
        for category, pattern in patterns
        for match in pattern.finditer(line)
    ]


def scan_pi(
    content: str, inventory: SourceInventory,
) -> list[PiConstructFinding]:
    """Report every occurrence in PHP pattern order, including fenced examples."""
    names = sorted(
        pi_source_skill_names(inventory),
        key=lambda name: len(name.encode("utf-8", "surrogateescape")),
        reverse=True,
    )
    patterns = list(_PI_PATTERNS)
    if names:
        patterns.append((PiConstruct.SKILL_INVOCATION, _slash_pattern(names)))
    qualified = [name for name in names if ":" in name]
    if qualified:
        patterns.append((PiConstruct.SKILL_INVOCATION, re.compile(
            r"(?<![A-Za-z0-9_$])\$(?:"
            + "|".join(re.escape(name) for name in qualified)
            + r")(?![A-Za-z0-9_:-])",
        )))
    return [
        PiConstructFinding(category, index, match.group())
        for index, line in enumerate(content.split("\n"), start=1)
        for category, pattern in patterns
        for match in pattern.finditer(line)
    ]
