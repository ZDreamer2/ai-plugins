"""Pin the PHP scanner's lexical vocabulary, boundaries and occurrence order."""

from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from marketplace.build.rendering import (
    CodexConstruct, CodexConstructFinding, PiConstruct, PiConstructFinding,
    render_file_result, scan_codex, scan_pi,
)
from marketplace.source import discover_source


class ConstructTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("forge/ai-plugin.yml", "name: authored-manifest\ndescription: Forge\n")
        for skill in ("forge", "chunk-plan", "chunk", "odd+name"):
            self.write(f"forge/skills/{skill}/SKILL.md", "---\nname: authored\ndescription: Text\n---\nBody")
        self.source = discover_source(self.root)

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8", "surrogateescape"))

    def matches(self, text: str) -> list[tuple[CodexConstruct, int, str]]:
        return [(item.category, item.line, item.text) for item in scan_codex(text, self.source)]

    def pi_matches(self, text: str) -> list[tuple[PiConstruct, int, str]]:
        return [(item.category, item.line, item.text) for item in scan_pi(text, self.source)]

    def test_pi_complete_vocabulary_and_pattern_order(self) -> None:
        variable = PiConstruct.HOST_VARIABLE
        tool = PiConstruct.HOST_TOOL
        invocation = PiConstruct.SKILL_INVOCATION
        cross = PiConstruct.CROSS_PLUGIN_REFERENCE
        self.assertEqual(self.pi_matches(
            "$authored-manifest:chunk AI_DOC_PLUGIN/x /forge AskUserQuestion "
            "${CLAUDE_PLUGIN_ROOT} Slash-Commands $ARGUMENTS[2] "
            "/authored-manifest:chunk-plan slash command\n"
            "```text\nTaskCreate TaskCreate /forge:chunk-plan ${CODEX_ROOT} $123\n```"
        ), [
            (variable, 1, "${CLAUDE_PLUGIN_ROOT}"),
            (variable, 1, "$ARGUMENTS"),
            (tool, 1, "AskUserQuestion"),
            (invocation, 1, "Slash-Commands"),
            (invocation, 1, "slash command"),
            (cross, 1, "AI_DOC_PLUGIN/x"),
            (invocation, 1, "/forge"),
            (invocation, 1, "/authored-manifest:chunk-plan"),
            (invocation, 1, "$authored-manifest:chunk"),
            (variable, 3, "${CODEX_ROOT}"),
            (variable, 3, "$123"),
            (tool, 3, "TaskCreate"), (tool, 3, "TaskCreate"),
            (invocation, 3, "/forge:chunk-plan"),
        ])
        self.assertEqual([category.title() for category in PiConstruct], [
            "Host variables and roots", "Host tool names and arguments",
            "Skill invocation wording", "Cross-plugin references",
        ])

    def test_pi_exact_tool_vocabulary_and_codex_only_negatives(self) -> None:
        tools = [
            "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList", "TodoWrite",
            "EnterPlanMode", "ExitPlanMode", "SendMessage", "Agent tool",
            "spawn_agent", "followup_task", "subagent_type", "fork_turns",
        ]
        self.assertEqual(self.pi_matches("; ".join(tools)), [
            (PiConstruct.HOST_TOOL, 1, text) for text in tools
        ])
        self.assertEqual(self.pi_matches(
            "general-purpose --model model sonnet model opus model haiku "
            "askuserquestion TASKCREATE Agent Tool subagent ask_user_question "
            "xTaskList TaskList2 _TodoWrite SendMessage_ spawn_agent-extra "
            "fork_turns_ xfollowup_task"
        ), [])
        self.assertEqual(self.pi_matches("éspawn_agenté 漢fork_turns漢"), [
            (PiConstruct.HOST_TOOL, 1, "spawn_agent"),
            (PiConstruct.HOST_TOOL, 1, "fork_turns"),
        ])

    def test_pi_variables_and_numeric_suffix_boundaries(self) -> None:
        self.assertEqual(self.pi_matches(
            "${CLAUDE_} ${CODEX_A1} ${claude_ROOT} $arguments $CODEX_HOME2 "
            "$ARGUMENTSsuffix $1a $12_ $1234x ${CLAUDE_A__} ${CODEX_HOME} "
            "x$ARGUMENTS[12] $$ARGUMENTS $CODEX_HOME/path $0 $123 $01. "
            "$1é $2- ${CODEX_ROOT}tail"
        ), [(PiConstruct.HOST_VARIABLE, 1, text) for text in (
            "${CLAUDE_A__}", "${CODEX_HOME}", "$ARGUMENTS", "$ARGUMENTS",
            "$CODEX_HOME", "$0", "$123", "$01", "$1", "$2", "${CODEX_ROOT}",
        )])

    def test_pi_both_identity_namespaces_and_qualified_dollar_boundaries(self) -> None:
        self.assertEqual(self.pi_matches(
            "/forge:chunk-plan /authored-manifest:chunk-plan /chunk /odd+name "
            "/forge.é é/forgeé (/chunk), /chunk... "
            "$forge:chunk-plan $authored-manifest:chunk-plan "
            "($forge:chunk), é$forge:chunké $forge:chunk.md /$forge:chunk "
            "$forge:chunk/path .$forge:chunk -$forge:chunk"
        ), [(PiConstruct.SKILL_INVOCATION, 1, text) for text in (
            "/forge:chunk-plan", "/authored-manifest:chunk-plan", "/chunk", "/odd+name",
            "/forge", "/forge", "/chunk", "/chunk",
            "$forge:chunk-plan", "$authored-manifest:chunk-plan",
            "$forge:chunk", "$forge:chunk", "$forge:chunk", "$forge:chunk",
            "$forge:chunk", "$forge:chunk", "$forge:chunk",
        )])
        self.assertEqual(self.pi_matches(
            "path/forge ./forge ../forge /forge.md /forge.2 /forge/path "
            "/forge-other /forge_2 a/forge 1/forge -/forge "
            "/missing /authored /FORGE $forge $chunk $odd+name "
            "a$forge:chunk _$forge:chunk 2$forge:chunk $$forge:chunk "
            "$forge:chunk_2 $forge:chunk-other $forge:chunk:other "
            "$forge:chunk-planX $missing:chunk"
        ), [])

    def test_pi_longest_utf8_alternatives_and_escaped_names(self) -> None:
        # A dot is punctuation unless followed by an ASCII filename suffix.
        # These source names intentionally bypass strict Pi publishing policy:
        # the lexical scanner must still recognize every inventoried source name.
        for skill in ("chunk.", "chunk.é", "é", "é.", "a+b"):
            self.write(f"forge/skills/{skill}/SKILL.md", "Unvalidated source")
        inventory = discover_source(self.root)
        self.assertEqual([item.text for item in scan_pi(
            "/chunk.é /chunk. /é. /a+b $forge:chunk.é $authored-manifest:a+b", inventory,
        )], [
            "/chunk.é", "/chunk.", "/é.", "/a+b",
            "$forge:chunk.é", "$authored-manifest:a+b",
        ])

    def test_pi_ascii_whitespace_and_lf_only_lines(self) -> None:
        cross = PiConstruct.CROSS_PLUGIN_REFERENCE
        self.assertEqual(self.pi_matches(
            "AI_DOC_PLUGIN/ AI_DOC_PLUGIN/a\tAI_DOC_PLUGIN/b\r"
            "AI_DOC_PLUGIN/c\vAI_DOC_PLUGIN/d\fAI_DOC_PLUGIN/e\u00a0f "
            "AI_DOC_PLUGIN/z\u2028q\nAI_DOC_PLUGIN/end"
        ), [
            (cross, 1, "AI_DOC_PLUGIN/"), (cross, 1, "AI_DOC_PLUGIN/a"),
            (cross, 1, "AI_DOC_PLUGIN/b"), (cross, 1, "AI_DOC_PLUGIN/c"),
            (cross, 1, "AI_DOC_PLUGIN/d"), (cross, 1, "AI_DOC_PLUGIN/e\u00a0f"),
            (cross, 1, "AI_DOC_PLUGIN/z\u2028q"), (cross, 2, "AI_DOC_PLUGIN/end"),
        ])
        self.assertEqual(self.pi_matches("SLASH COMMANDS slash\tcommand slash\u00a0command"), [
            (PiConstruct.SKILL_INVOCATION, 1, "SLASH COMMANDS"),
        ])

    def test_pi_no_skills_and_source_root_identity(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        self.assertEqual(scan_pi("/forge $forge:chunk slash-command", discover_source(empty)), [
            PiConstructFinding(PiConstruct.SKILL_INVOCATION, 1, "slash-command"),
        ])
        self.write("root-plugin/ai-plugin.yml", "name: different\ndescription: Test\n")
        self.write("root-plugin/skills/run/SKILL.md", "name differs")
        source = discover_source(self.root / "root-plugin")
        self.assertEqual([item.text for item in scan_pi(
            "/root-plugin:run /run /different:run $root-plugin:run $different:run $run", source,
        )], ["/root-plugin:run", "/run", "/different:run", "$root-plugin:run", "$different:run"])

    def test_every_category_pattern_and_per_line_pattern_order(self) -> None:
        variable = CodexConstruct.CLAUDE_VARIABLE
        tool = CodexConstruct.CLAUDE_TOOL
        invocation = CodexConstruct.SKILL_INVOCATION
        cross = CodexConstruct.CROSS_PLUGIN_REFERENCE
        self.assertEqual(self.matches(
            "AI_DOC_PLUGIN/x /forge AskUserQuestion ${CLAUDE_PLUGIN_ROOT} "
            "Slash-Commands $ARGUMENTS[2] /forge:chunk-plan slash command\n"
            "```text\nTaskCreate TaskCreate /forge:chunk-plan ${CLAUDE_SESSION_ID}\n```"
        ), [
            (variable, 1, "${CLAUDE_PLUGIN_ROOT}"),
            (variable, 1, "$ARGUMENTS"),
            (tool, 1, "AskUserQuestion"),
            (invocation, 1, "Slash-Commands"),
            (invocation, 1, "slash command"),
            (invocation, 1, "/forge"),
            (invocation, 1, "/forge:chunk-plan"),
            (cross, 1, "AI_DOC_PLUGIN/x"),
            (variable, 3, "${CLAUDE_SESSION_ID}"),
            (tool, 3, "TaskCreate"), (tool, 3, "TaskCreate"),
            (invocation, 3, "/forge:chunk-plan"),
        ])
        self.assertEqual([category.title() for category in CodexConstruct], [
            "Claude variables", "Claude tool names and arguments",
            "Skill invocation wording", "Cross-plugin references", "Skill frontmatter",
        ])

    def test_exact_tool_vocabulary_and_case(self) -> None:
        tools = [
            "AskUserQuestion", "TaskCreate", "TaskUpdate", "TaskList", "TodoWrite",
            "EnterPlanMode", "ExitPlanMode", "SendMessage", "Agent tool",
            "subagent_type", "general-purpose", "--model", "model sonnet",
            "model opus", "model haiku",
        ]
        self.assertEqual(self.matches("; ".join(tools)), [
            (CodexConstruct.CLAUDE_TOOL, 1, text) for text in tools
        ])
        self.assertEqual(self.matches(
            "Agent Sonnet opus haiku askuserquestion TASKCREATE Agent Tool "
            "--model-name xTaskList TaskList2 _TodoWrite SendMessage_ "
            "foo-general-purpose general-purpose-extra model Sonnet"
        ), [])
        self.assertEqual(self.matches("éTaskListé 漢--model漢"), [
            (CodexConstruct.CLAUDE_TOOL, 1, "TaskList"),
            (CodexConstruct.CLAUDE_TOOL, 1, "--model"),
        ])

    def test_variables_are_literal_without_word_boundaries(self) -> None:
        self.assertEqual(self.matches(
            "${CLAUDE_} ${CLAUDE_A1} ${claude_ROOT} $arguments $0 $123 "
            "${CLAUDE_A__} x$ARGUMENTS[12] $ARGUMENTSsuffix $$ARGUMENTS"
        ), [
            (CodexConstruct.CLAUDE_VARIABLE, 1, "${CLAUDE_A__}"),
            (CodexConstruct.CLAUDE_VARIABLE, 1, "$ARGUMENTS"),
            (CodexConstruct.CLAUDE_VARIABLE, 1, "$ARGUMENTS"),
            (CodexConstruct.CLAUDE_VARIABLE, 1, "$ARGUMENTS"),
        ])

    def test_invocation_identity_escaping_punctuation_and_filename_exclusions(self) -> None:
        self.assertEqual(self.matches(
            "/forge:chunk-plan /forge:chunk /odd+name /chunk-plan. /forge... "
            "(/forge), [/forge] é/forgeé /forge.é"
        ), [(CodexConstruct.SKILL_INVOCATION, 1, match) for match in (
            "/forge:chunk-plan", "/forge:chunk", "/odd+name", "/chunk-plan",
            "/forge", "/forge", "/forge", "/forge", "/forge",
        )])
        self.assertEqual(self.matches(
            "path/forge Skill.md/forge ./forge ../forge /forge.md /forge.2 "
            "/forge/path /forge-other /forge_2 a/forge 1/forge -/forge "
            "/missing /authored-manifest:chunk /authored "
            "[ordinary](../docs/file.md) /FORGE"
        ), [])

    def test_ascii_whitespace_and_lf_only_lines(self) -> None:
        cross = CodexConstruct.CROSS_PLUGIN_REFERENCE
        self.assertEqual(self.matches(
            "AI_DOC_PLUGIN/ AI_DOC_PLUGIN/a\tAI_DOC_PLUGIN/b\r"
            "AI_DOC_PLUGIN/c\vAI_DOC_PLUGIN/d\fAI_DOC_PLUGIN/e\u00a0f "
            "AI_DOC_PLUGIN/z\u2028q\nAI_DOC_PLUGIN/end"
        ), [
            (cross, 1, "AI_DOC_PLUGIN/"), (cross, 1, "AI_DOC_PLUGIN/a"),
            (cross, 1, "AI_DOC_PLUGIN/b"), (cross, 1, "AI_DOC_PLUGIN/c"),
            (cross, 1, "AI_DOC_PLUGIN/d"), (cross, 1, "AI_DOC_PLUGIN/e\u00a0f"),
            (cross, 1, "AI_DOC_PLUGIN/z\u2028q"), (cross, 2, "AI_DOC_PLUGIN/end"),
        ])
        self.assertEqual(self.matches("SLASH COMMANDS slash\tcommand slash\u00a0command"), [
            (CodexConstruct.SKILL_INVOCATION, 1, "SLASH COMMANDS"),
        ])

    def test_no_skills_and_source_root_directory_identity(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        self.assertEqual(scan_codex("/forge slash-command", discover_source(empty)), [
            CodexConstructFinding(CodexConstruct.SKILL_INVOCATION, 1, "slash-command"),
        ])
        self.write("root-plugin/ai-plugin.yml", "name: different\ndescription: Test\n")
        self.write("root-plugin/skills/run/SKILL.md", "name differs")
        source = discover_source(self.root / "root-plugin")
        self.assertEqual(scan_codex("/root-plugin:run /run /different:run", source), [
            CodexConstructFinding(CodexConstruct.SKILL_INVOCATION, 1, "/root-plugin:run"),
            CodexConstructFinding(CodexConstruct.SKILL_INVOCATION, 1, "/run"),
        ])

    def test_complete_pipeline_scans_documents_and_keeps_frontmatter_first(self) -> None:
        content = (
            "---\nname: authored\ndescription: Text\nmodel: opus\n---\n"
            "${AGENT_QUESTION_TOOL} /forge\n"
        )
        skill = render_file_result(content, "forge/skills/chunk/SKILL.md", "codex", self.source)
        self.assertEqual(skill.findings, [
            CodexConstructFinding(CodexConstruct.SKILL_FRONTMATTER, 4, "model: opus"),
            CodexConstructFinding(CodexConstruct.SKILL_INVOCATION, 5, "/forge"),
        ])
        for path in ("README.md", "forge/workflows/do.md", "forge/docs/example.meta.md"):
            with self.subTest(path=path):
                result = render_file_result(content, path, "codex", self.source)
                self.assertEqual(result.content, content.replace("${AGENT_QUESTION_TOOL}", "request_user_input_async"))
                self.assertEqual(result.extra_files, {})
                self.assertEqual(result.findings, [
                    CodexConstructFinding(CodexConstruct.SKILL_INVOCATION, 6, "/forge"),
                ])

    def test_pi_complete_pipeline_scans_supporting_and_meta_examples(self) -> None:
        content = (
            "---\nname: authored\ndescription: Text\nmodel: opus\n---\n"
            "${AGENT_SUBAGENT_TOOL} spawn_agent spawn_agent $ARGUMENTS\n"
            "```example\n/authored-manifest:chunk $forge:chunk\n```\n"
        )
        for path in ("README.md", "forge/workflows/do.md", "forge/docs/example.meta.md"):
            with self.subTest(path=path):
                result = render_file_result(content, path, "pi", self.source)
                self.assertEqual(result.content, content.replace("${AGENT_SUBAGENT_TOOL}", "subagent"))
                self.assertEqual(result.extra_files, {})
                self.assertEqual(result.findings, [
                    PiConstructFinding(PiConstruct.HOST_VARIABLE, 6, "$ARGUMENTS"),
                    PiConstructFinding(PiConstruct.HOST_TOOL, 6, "spawn_agent"),
                    PiConstructFinding(PiConstruct.HOST_TOOL, 6, "spawn_agent"),
                    PiConstructFinding(PiConstruct.SKILL_INVOCATION, 8, "/authored-manifest:chunk"),
                    PiConstructFinding(PiConstruct.SKILL_INVOCATION, 8, "$forge:chunk"),
                ])

    def test_scanner_and_reports_work_in_an_isolated_copied_plugin(self) -> None:
        plugin = Path(__file__).resolve().parents[5]
        copied = self.root / "installed"
        shutil.copytree(plugin, copied, ignore=shutil.ignore_patterns("__pycache__"))
        code = (
            "import sys\n"
            f"sys.path[:] = [{str(copied / 'scripts')!r}] + [p for p in sys.path if p.startswith(sys.base_prefix) and 'site-packages' not in p]\n"
            "from marketplace.source import discover_source\n"
            "from marketplace.build.rendering import scan_codex, CodexConstruct, scan_pi, PiConstruct\n"
            "from marketplace.build import CodexConstructReport, PiConstructReport\n"
            f"source = discover_source({str(self.root / 'forge')!r})\n"
            "findings = scan_codex('TaskCreate /forge:chunk-plan', source)\n"
            "assert [f.text for f in findings] == ['TaskCreate', '/forge:chunk-plan']\n"
            "report = CodexConstructReport()\n"
            "report.add('docs/x.md', None, findings)\n"
            "assert report.total() == '2 unresolved construct(s) in 1 file(s)'\n"
            "pi_findings = scan_pi('spawn_agent /authored-manifest:chunk-plan $forge:chunk', source)\n"
            "assert [f.text for f in pi_findings] == ['spawn_agent', '/authored-manifest:chunk-plan', '$forge:chunk']\n"
            "assert pi_findings[0].category is PiConstruct.HOST_TOOL\n"
            "pi_report = PiConstructReport()\n"
            "pi_report.add('docs/pi.md', None, pi_findings)\n"
            "assert pi_report.total() == '3 unresolved construct(s) in 1 file(s)'\n"
            "assert '# Unresolved host constructs in the Pi tree' in pi_report.render()\n"
            "assert report.total() == '2 unresolved construct(s) in 1 file(s)'\n"
            "assert 'yaml' not in sys.modules\n"
            "assert not any(name == 'bc' or name.startswith('bc.') for name in sys.modules)\n"
        )
        process = subprocess.run(["python3", "-B", "-S", "-c", code], cwd="/", capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)


if __name__ == "__main__":
    unittest.main()
