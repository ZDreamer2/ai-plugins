"""Editing metadata stays in sources, not rendered documents or includes."""

from pathlib import Path
import tempfile
import unittest

from marketplace import parse_yaml
from marketplace.build.rendering import (
    render_file, render_file_result, render_markdown,
)
from marketplace.source import discover_source


class EditingContextTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("main/ai-plugin.yml", "name: main\ndescription: Main\n")
        self.write("main/skills/main/SKILL.md", (
            "---\nname: main\ndescription: Main\n---\nInstructions.\n"
        ))

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content.encode("utf-8", "surrogateescape"))

    def test_sole_property_removed_for_all_hosts_and_rendering_apis(self) -> None:
        content = "---\nedit-only-context: Context.meta.md\n---\n\n# Body\n"
        for host in ("claude", "codex", "pi"):
            for renderer in (render_file, render_markdown):
                for path in ("README.md", "main/docs/layout.md"):
                    with self.subTest(host=host, renderer=renderer, path=path):
                        self.assertEqual(renderer(
                            content, path, host, discover_source(self.root),
                        ), "\n# Body\n")

    def test_other_properties_and_body_survive(self) -> None:
        content = (
            "---\nname: example\nedit-only-context: Context.meta.md\n"
            "description: 'A: description'\nsettings:\n"
            "  edit-only-context: runtime\n  enabled: true\n---\nBody\n"
        )
        for host in ("claude", "codex", "pi"):
            with self.subTest(host=host):
                rendered = render_file(
                    content, "main/docs/layout.md", host,
                    discover_source(self.root),
                )
                header, body = rendered[4:].split("---\n", 1)
                self.assertEqual(parse_yaml(header), {
                    "name": "example", "description": "A: description",
                    "settings": {"edit-only-context": "runtime", "enabled": True},
                })
                self.assertEqual(body, "Body\n")

    def test_quoted_key_and_compound_values_are_removed(self) -> None:
        for value in (
            "Context.meta.md", "null", "false", "''", "",
            "|\n  first\n  second", "\n  - first\n  - second",
            "\n  meta: Context.meta.md",
        ):
            with self.subTest(value=value):
                content = f"---\n'edit-only-context': {value}\n---\nBody"
                self.assertEqual(render_markdown(
                    content, "main/docs/layout.md", "claude",
                    discover_source(self.root),
                ), "Body")

    def test_absent_property_preserves_bytes_and_existing_invalid_headers(self) -> None:
        for content in (
            "Body edit-only-context\n---\nedit-only-context: example\n---\n",
            "```yaml\nedit-only-context: example\n```\n",
            "---\nsettings:\n  edit-only-context: nested\n---\nBody\n",
            "---\nname: 'quoted' # comment\n---\nBody\udcff",
            "---\r\nedit-only-context: example\r\n---\r\nBody",
            "---\nedit-only-context: example\n---",
            "---\nedit-only-context: [broken\n---\nBody",
            "---\n- edit-only-context\n---\nBody",
        ):
            with self.subTest(content=content):
                self.assertEqual(render_markdown(
                    content, "main/docs/layout.md", "claude",
                    discover_source(self.root),
                ), content)

    def test_removed_metadata_is_not_processed_as_placeholders_or_includes(self) -> None:
        content = (
            "---\nedit-only-context: |\n"
            "  ${AGENT_UNKNOWN}\n"
            "  ${AGENT_INCLUDE_DOC(missing.md)}\n---\nBody\n"
        )
        for host in ("claude", "codex", "pi"):
            with self.subTest(host=host):
                self.assertEqual(render_markdown(
                    content, "main/docs/layout.md", host,
                    discover_source(self.root),
                ), "Body\n")

    def test_included_metadata_is_removed_before_validation_and_rebasing(self) -> None:
        self.write("main/docs/part.md", (
            "---\nedit-only-context: |\n"
            "  ${AGENT_INCLUDE_DOC(missing.md)}\n"
            "  ${AGENT_UNKNOWN}\n---\n[Guide](guide.md)\n"
        ))
        for host in ("claude", "codex", "pi"):
            for marker in (
                "${AGENT_INCLUDE_DOC(docs/part.md)}",
                f"${{AGENT_INCLUDE_DOC_FOR({host}, docs/part.md)}}",
                "${AGENT_INCLUDE_DOC_FOR(claude, docs/part.md)}",
            ):
                with self.subTest(host=host, marker=marker):
                    expected = (
                        "" if "FOR(claude" in marker and host != "claude"
                        else "[Guide](docs/guide.md)\n"
                    )
                    self.assertEqual(render_markdown(
                        marker + "\n", "main/README.md", host,
                        discover_source(self.root),
                    ), expected)

    def test_runtime_nested_includes_still_fail(self) -> None:
        self.write("main/docs/part.md", (
            "---\nedit-only-context: Context.meta.md\n---\n"
            "${AGENT_INCLUDE_DOC(other.md)}\n"
        ))
        with self.assertRaisesRegex(ValueError, "includes another document"):
            render_markdown(
                "${AGENT_INCLUDE_DOC(docs/part.md)}\n",
                "main/README.md", "claude", discover_source(self.root),
            )

    def test_skill_host_adaptation_sees_only_runtime_fields(self) -> None:
        content = (
            "---\nname: main\ndescription: Main\n"
            "edit-only-context: Context.meta.md\n---\nInstructions.\n"
        )
        for host in ("claude", "codex", "pi"):
            with self.subTest(host=host):
                result = render_file_result(
                    content, "main/skills/main/SKILL.md", host,
                    discover_source(self.root),
                )
                self.assertNotIn("edit-only-context", result.content)
                self.assertEqual(result.findings, [])
                self.assertIn("Instructions.", result.content)

    def test_non_markdown_files_are_not_changed(self) -> None:
        content = "---\nedit-only-context: Context.meta.md\n---\nBody\n"
        self.assertEqual(render_file(
            content, "main/example.txt", "claude", discover_source(self.root),
        ), content)
