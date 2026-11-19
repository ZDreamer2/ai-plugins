"""Keep marker detection, PHP-compatible parsing and diagnostics together."""

import re
from typing import NoReturn

from marketplace.source import SourceInventory, pi_skill_for_invocation


MARKER_PATTERN = re.compile(r"(?P<escaped>\$)?\$\{AGENT_[^}\n]*\}")
_MARKER_SYNTAX = re.compile(
    r"\$\{AGENT_(?P<name>[A-Z_]+)(?:\((?P<argument>[^()]*)\))?\}"
)
_ARGUMENT_SYNTAX = re.compile(r"[A-Za-z0-9_-]+(?::[A-Za-z0-9_-]+)?")
_ARGUMENT_NAMES = {
    "SUBAGENT_TOOL": None,
    "FORK": None,
    "SUBAGENT_FOLLOWUP_TOOL": None,
    "QUESTION_TOOL": None,
    "SKILL": "skill name",
}
_VALUES = {
    "SUBAGENT_TOOL": {
        "claude": "Agent", "codex": "spawn_agent", "pi": "subagent",
    },
    "FORK": {
        "claude": "the Agent tool with `subagent_type: fork` "
                  "(a fork: it inherits the parent session's context)",
        "codex": '`spawn_agent` with `fork_turns: "all"` '
                 "(a fork: it inherits the parent session's context)",
        "pi": '`subagent` with `context: "fork"` and `model: "inherit"` '
              "(a fork: it inherits the parent session's context)",
    },
    "SUBAGENT_FOLLOWUP_TOOL": {
        "claude": "SendMessage", "codex": "followup_task",
        "pi": "`subagent` with `steer` for a running child or `resume` "
              "for a completed child",
    },
    "QUESTION_TOOL": {
        "claude": "AskUserQuestion", "codex": "request_user_input_async",
        "pi": "ask_user_question",
    },
}


def fail(marker: str, logical_path: str, reason: str) -> NoReturn:
    common_at = logical_path.find("@common/")
    origin = (
        "" if common_at == -1
        else f", a copy of '{logical_path[common_at:]}'"
    )
    raise ValueError(
        f"Agent placeholder '{marker}' in '{logical_path}'{origin} {reason}."
    )


def parse(marker: str, logical_path: str) -> tuple[str, str | None]:
    parts = _MARKER_SYNTAX.fullmatch(marker)
    if parts is None:
        fail(marker, logical_path,
             "is not written as a placeholder of the vocabulary")
    name = parts["name"]
    if name not in _ARGUMENT_NAMES:
        fail(marker, logical_path, "names no placeholder of the vocabulary")
    given = parts["argument"] or ""
    recognized = _ARGUMENT_SYNTAX.fullmatch(given) is not None
    argument = given if recognized else None
    argument_name = _ARGUMENT_NAMES[name]
    # PHP treats a malformed value argument as absent, even for no-arg cases.
    if (argument_name is None) != (argument is None):
        rule = (
            f"takes no argument: write it as ${{AGENT_{name}}}"
            if argument_name is None else
            f"needs the {argument_name}: write it as "
            f"${{AGENT_{name}(<{argument_name}>)}}"
        )
        fail(marker, logical_path, rule)
    return name, argument


def reject_legacy_includes(content: str, logical_path: str) -> None:
    """Reject live old includes without interpreting escaped examples."""
    for match in MARKER_PATTERN.finditer(content):
        if not match['escaped'] and re.match(r"\$\{AGENT_INCLUDE_DOC(?:_FOR)?\b", match[0]):
            fail(match[0], logical_path, 'is retired; use a Jinja include')


def substitute(
    content: str, logical_path: str, host: str, inventory: SourceInventory,
) -> str:
    def replace(match: re.Match[str]) -> str:
        marker = match[0]
        if match["escaped"]:
            return marker[1:]
        name, argument = parse(marker, logical_path)
        if name == "SKILL":
            if host == "pi":
                published = pi_skill_for_invocation(inventory, argument)
                if published is None:
                    fail(marker, logical_path,
                         "does not name a published Pi skill")
                return "/skill:" + published
            if host == "claude":
                return "/" + argument
            qualified = argument if ":" in argument else f"{argument}:{argument}"
            return "$" + qualified
        return _VALUES[name][host]

    return MARKER_PATTERN.sub(replace, content)
