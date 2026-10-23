"""PHP-derived expectations for shared vocabulary and file selection."""

from pathlib import Path
import tempfile
import unittest

from marketplace.build.rendering import (
    render_file, render_file_result, render_markdown,
)
from marketplace.source import discover_source


class MarkdownTests(unittest.TestCase):
    def setUp(self) -> None:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.write("folder/ai-plugin.yml", "name: alpha\ndescription: Test\n")
        self.write("folder/skills/alpha/SKILL.md", "hub")
        self.write("folder/skills/load/SKILL.md", "load")
        self.source = discover_source(self.root)

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode("utf-8"))

    def test_complete_shared_output_for_every_host(self) -> None:
        content = (
            "---\nname: authored\nuser-invocable: true\n---\n"
            "Run `${AGENT_SKILL(alpha)}` and ${AGENT_SKILL(alpha:load)}.\n"
            "Use ${AGENT_SUBAGENT_TOOL}; fork with ${AGENT_FORK}.\n"
            "Follow up via ${AGENT_SUBAGENT_FOLLOWUP_TOOL}.\n"
            "Ask ${AGENT_QUESTION_TOOL}.\n"
            "```text\n${AGENT_SUBAGENT_TOOL}\n```\n"
            "[doc](../docs/x.md); python3 ../scripts/run.py\n"
            "${CLAUDE_PLUGIN_ROOT} $ARGUMENTS ${CLAUDE_SESSION_ID}\n"
            "Quoted $${AGENT_TYPO} and $$${AGENT_SKILL(alpha)}.\n"
        )
        expected = {
            "claude": (
                "---\nname: authored\nuser-invocable: true\n---\n"
                "Run `/alpha` and /alpha:load.\n"
                "Use Agent; fork with the Agent tool with `subagent_type: fork` "
                "(a fork: it inherits the parent session's context).\n"
                "Follow up via SendMessage.\nAsk AskUserQuestion.\n"
                "```text\nAgent\n```\n"
                "[doc](../docs/x.md); python3 ../scripts/run.py\n"
                "${CLAUDE_PLUGIN_ROOT} $ARGUMENTS ${CLAUDE_SESSION_ID}\n"
                "Quoted ${AGENT_TYPO} and $${AGENT_SKILL(alpha)}.\n"
            ),
            "codex": (
                "---\nname: authored\nuser-invocable: true\n---\n"
                "Run `$alpha:alpha` and $alpha:load.\n"
                'Use spawn_agent; fork with `spawn_agent` with `fork_turns: "all"` '
                "(a fork: it inherits the parent session's context).\n"
                "Follow up via followup_task.\nAsk request_user_input_async.\n"
                "```text\nspawn_agent\n```\n"
                "[doc](../docs/x.md); python3 ../scripts/run.py\n"
                "${CLAUDE_PLUGIN_ROOT} $ARGUMENTS ${CLAUDE_SESSION_ID}\n"
                "Quoted ${AGENT_TYPO} and $${AGENT_SKILL(alpha)}.\n"
            ),
            "pi": (
                "---\nname: authored\nuser-invocable: true\n---\n"
                "Run `/skill:alpha` and /skill:alpha-load.\n"
                'Use subagent; fork with `subagent` with `context: "fork"` '
                'and `model: "inherit"` '
                "(a fork: it inherits the parent session's context).\n"
                "Follow up via `subagent` with `steer` for a running child "
                "or `resume` for a completed child.\nAsk ask_user_question.\n"
                "```text\nsubagent\n```\n"
                "[doc](../docs/x.md); python3 ../scripts/run.py\n"
                "${CLAUDE_PLUGIN_ROOT} $ARGUMENTS ${CLAUDE_SESSION_ID}\n"
                "Quoted ${AGENT_TYPO} and $${AGENT_SKILL(alpha)}.\n"
            ),
        }
        for host, output in expected.items():
            with self.subTest(host=host):
                if host == "pi":
                    self.assertEqual(render_markdown(
                        content, "folder/skills/load/SKILL.md", host, self.source,
                    ), output)
                    continue
                result = render_file_result(
                    content, "folder/skills/load/SKILL.md", host, self.source,
                )
                self.assertEqual(result.content, output)
                self.assertEqual(result.extra_files, {})
                self.assertEqual(render_file(
                    content, "folder/skills/load/SKILL.md", host, self.source,
                ), output)

    def test_shared_api_does_not_reduce_or_scan_skills(self) -> None:
        text = "---\ndescription: Test\nuser-invocable: false\n---\nAgent"
        path = "folder/skills/load/SKILL.md"
        self.assertEqual(render_markdown(text, path, "codex", self.source), text)
        result = render_file_result(text, path, "codex", self.source)
        self.assertEqual(result.content, "---\ndescription: Test\n---\nAgent")
        self.assertEqual(render_file(text, path, "codex", self.source), result.content)
        self.assertTrue(result.findings)

    def test_value_failures_quote_exact_marker_path_and_reason(self) -> None:
        cases = {
            "${AGENT_TYPO}": "names no placeholder of the vocabulary",
            "${AGENT_VAR(CLAUDE_PLUGIN_ROOT)}":
                "names no placeholder of the vocabulary",
            "${AGENT_Skill}":
                "is not written as a placeholder of the vocabulary",
            "${AGENT_SKILL(a(b))}":
                "is not written as a placeholder of the vocabulary",
            "${AGENT_SKILL}": "needs the skill name: write it as "
                "${AGENT_SKILL(<skill name>)}",
            "${AGENT_SUBAGENT_TOOL(fork)}": "takes no argument: write it as "
                "${AGENT_SUBAGENT_TOOL}",
            "${AGENT_FORK(all)}": "takes no argument: write it as ${AGENT_FORK}",
            "${AGENT_SUBAGENT_FOLLOWUP_TOOL(reviewer)}":
                "takes no argument: write it as ${AGENT_SUBAGENT_FOLLOWUP_TOOL}",
            "${AGENT_QUESTION_TOOL(question)}": "takes no argument: write it as "
                "${AGENT_QUESTION_TOOL}",
        }
        for bad in ("", "deep run", "alpha:", "a:b:c", "50%", " alpha "):
            cases[f"${{AGENT_SKILL({bad})}}"] = (
                "needs the skill name: write it as ${AGENT_SKILL(<skill name>)}"
            )
        for host in ("claude", "codex", "pi"):
            for marker, reason in cases.items():
                with self.subTest(host=host, marker=marker):
                    with self.assertRaises(ValueError) as error:
                        render_file(marker, "folder/docs/x.md", host, self.source)
                    self.assertEqual(str(error.exception),
                        f"Agent placeholder '{marker}' in 'folder/docs/x.md' "
                        f"{reason}.")

    def test_escaped_unknown_and_malformed_markers_are_literal_once(self) -> None:
        for host in ("claude", "codex", "pi"):
            self.assertEqual(render_file(
                "$${AGENT_TYPO} $${AGENT_SKILL(50%)} "
                "$$${AGENT_SKILL(a(b))}", "README.md", host, self.source,
            ), "${AGENT_TYPO} ${AGENT_SKILL(50%)} $${AGENT_SKILL(a(b))}")

    def test_unclosed_multiline_and_nonmarkers_stay_unchanged(self) -> None:
        text = "BC_AI_AGENT_WORKSHOP {project} ${AGENT_SKILL(\nalpha)} ${AGENT_"
        self.assertEqual(render_file(
            text, "README.md", "claude", self.source,
        ), text)

    def test_no_argument_parser_quirks(self) -> None:
        for argument in ("", "two words", "a:b:c", "50%", " ", "\r"):
            for name, expected in (
                ("SUBAGENT_TOOL", "Agent"),
                ("QUESTION_TOOL", "AskUserQuestion"),
            ):
                with self.subTest(name=name, argument=argument):
                    self.assertEqual(render_file(
                        f"${{AGENT_{name}({argument})}}", "README.md",
                        "claude", self.source,
                    ), expected)

    def test_only_pi_requires_published_manifest_identity(self) -> None:
        for invocation in ("folder", "folder:load", "missing", "alpha:missing"):
            marker = f"${{AGENT_SKILL({invocation})}}"
            self.assertEqual(render_file(
                marker, "README.md", "claude", self.source,
            ), "/" + invocation)
            codex = invocation if ":" in invocation else f"{invocation}:{invocation}"
            self.assertEqual(render_file(
                marker, "README.md", "codex", self.source,
            ), "$" + codex)
            with self.assertRaises(ValueError) as error:
                render_file(marker, "README.md", "pi", self.source)
            self.assertEqual(str(error.exception),
                f"Agent placeholder '{marker}' in 'README.md' "
                "does not name a published Pi skill.")
        self.assertEqual(render_file(
            "${AGENT_SKILL(alpha:alpha)}", "README.md", "pi", self.source,
        ), "/skill:alpha")

    def test_shared_origin_and_percent_diagnostics(self) -> None:
        with self.assertRaises(ValueError) as error:
            render_file("${AGENT_SKILL(50%)}",
                        "folder/@common/docs/Shared.md", "pi", self.source)
        self.assertEqual(str(error.exception),
            "Agent placeholder '${AGENT_SKILL(50%)}' in "
            "'folder/@common/docs/Shared.md', a copy of '@common/docs/Shared.md' "
            "needs the skill name: write it as ${AGENT_SKILL(<skill name>)}.")

    def test_non_markdown_bypasses_markers_and_shared_stage_is_reusable(self) -> None:
        text = "${AGENT_TYPO} ${AGENT_INCLUDE_DOC_FOR(pi, /missing.md)}"
        for path in ("hooks.json", "README.MD", "scripts/run", "data.md.txt"):
            self.assertEqual(render_file(text, path, "pi", self.source), text)
        self.assertEqual(render_markdown(
            "${AGENT_SUBAGENT_TOOL}", "body.txt", "codex", self.source,
        ), "spawn_agent")

    def test_line_endings_and_invalid_bytes_round_trip(self) -> None:
        data = b"\xff raw\r\n${AGENT_SUBAGENT_TOOL}\r\nother\nfinal\r"
        text = data.decode("utf-8", "surrogateescape")
        result = render_file(text, "README.md", "claude", self.source)
        self.assertEqual(result.encode("utf-8", "surrogateescape"),
                         b"\xff raw\r\nAgent\r\nother\nfinal\r")
        for text in ("body\r\n", "body\r\nnext\nend", "no final newline"):
            self.assertEqual(render_file(
                text, "README.md", "claude", self.source,
            ), text)


if __name__ == "__main__":
    unittest.main()
