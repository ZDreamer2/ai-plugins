"""Include selection, validation and link rebasing through the rendering API."""

import os
from pathlib import Path
import tempfile
import unittest

from marketplace.build.rendering import render_file, render_markdown
from marketplace.source import discover_source


class IncludeTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.logical_path = "main/skills/deep/SKILL.md"
        self.write("main/ai-plugin.yml", "name: main\ndescription: Main\n")
        self.write(self.logical_path, "Body.")
        self.write("main/docs/note.md", "Note.")

    def write(self, relative: str, content: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(
            content.encode("utf-8", "surrogateescape")
            if isinstance(content, str) else content
        )
        return path

    def render(
        self, content: str, host: str = "claude", path: str | None = None,
    ) -> str:
        return render_file(
            content, path or self.logical_path, host,
            discover_source(self.root),
        )

    def assert_failure(
        self, content: str, reason: str, marker: str | None = None,
        path: str | None = None, host: str = "claude",
    ) -> None:
        logical_path = path or self.logical_path
        marker = content if marker is None else marker
        common = logical_path.find("@common/")
        origin = (
            f", a copy of '{logical_path[common:]}'" if common >= 0 else ""
        )
        with self.assertRaises(ValueError) as caught:
            self.render(content, host, logical_path)
        self.assertEqual(
            str(caught.exception),
            f"Agent placeholder '{marker}' in '{logical_path}'{origin} "
            f"{reason}.",
        )

    def test_selected_and_dropped_includes_for_every_host(self) -> None:
        self.write("main/docs/claude.md", "Claude ${AGENT_SUBAGENT_TOOL}.\n\n")
        self.write("main/docs/codex.md", "Codex ${AGENT_SUBAGENT_TOOL}.\n")
        self.write("main/docs/pi.md", "Pi ${AGENT_SUBAGENT_TOOL}.")
        content = (
            "Before.\n"
            "  ${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/claude.md)}\n"
            "\t${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/codex.md)}\n"
            "${AGENT_INCLUDE_DOC_FOR(pi, ../../docs/pi.md)}\n"
            "\nAfter."
        )
        for host, expected in (
            ("claude", "Before.\nClaude Agent.\n\nAfter."),
            ("codex", "Before.\nCodex spawn_agent.\n\nAfter."),
            ("pi", "Before.\nPi subagent.\n\nAfter."),
        ):
            with self.subTest(host=host):
                self.assertEqual(render_markdown(
                    content, self.logical_path, host, discover_source(self.root),
                ), expected)

    def test_trailing_lf_and_marker_line_ending(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}"
        for included in ("Text", "Text\n", "Text\n\n", "", "\n\n"):
            self.write("main/docs/note.md", included)
            expected = "Text" if included.startswith("Text") else ""
            for ending in ("", "\n", "\r\n"):
                with self.subTest(included=included, ending=ending):
                    self.assertEqual(
                        self.render(marker + ending),
                        expected + ("\n" if ending else ""),
                    )

    def test_crlf_mixed_endings_and_no_indentation(self) -> None:
        self.write(
            "main/docs/note.md",
            "[Guide](../guide.md)\r\nRun ../scripts/run.py\nLast\r\n\r\n",
        )
        content = (
            "Before\r\n  ${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}"
            "\r\nAfter\nTail"
        )
        self.assertEqual(
            self.render(content),
            "Before\r\n[Guide](../../guide.md)\r\nRun ../scripts/run.py\n"
            "Last\r\n\r\nAfter\nTail",
        )

    def test_php_trim_whitespace_is_accepted_around_marker_and_arguments(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(\x00\tclaude\v, \v../../docs/note.md\x00)}"
        self.assertEqual(self.render(" \t\x00\v" + marker + "\r\n"), "Note.\n")

    def test_unicode_and_form_feed_are_not_placement_whitespace(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}"
        for whitespace in ("\f", "\u00a0", "\u2003"):
            with self.subTest(whitespace=repr(whitespace)):
                self.assert_failure(
                    whitespace + marker,
                    "on line 1 shares its line with other text: "
                    "an include stands alone on its line", marker,
                )

    def test_unknown_host_and_non_php_trim_host_whitespace(self) -> None:
        for tree in ("cursor", "Claude", "\u00a0claude", "claude\f"):
            with self.subTest(tree=tree):
                self.assert_failure(
                    "${AGENT_INCLUDE_DOC_FOR(" + tree + ", ../../docs/note.md)}",
                    "on line 1 names no agent tree: write claude or codex or pi",
                )

    def test_include_argument_is_required(self) -> None:
        for marker in (
            "${AGENT_INCLUDE_DOC_FOR}", "${AGENT_INCLUDE_DOC_FOR()}",
            "${AGENT_INCLUDE_DOC_FOR( \t\x00\v)}",
        ):
            with self.subTest(marker=marker):
                self.assert_failure(
                    marker, "needs the agent tree and document path: write it as "
                    "${AGENT_INCLUDE_DOC_FOR(<agent tree and document path>)}",
                )

    def test_sharing_line_and_second_include_fail_placement(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/note.md)}"
        for content in ("Prefix " + marker, marker + " suffix", marker + marker):
            with self.subTest(content=content):
                self.assert_failure(
                    content, "on line 1 shares its line with other text: "
                    "an include stands alone on its line", marker,
                )

    def test_invalid_document_paths_and_case_sensitive_suffix(self) -> None:
        for argument in (
            "codex", "codex,", "codex, /docs/note.md",
            "codex, ../../docs/note.txt", "codex, ../../docs/note.MD",
            "codex, ../../docs/note.md\u00a0",
        ):
            with self.subTest(argument=argument):
                self.assert_failure(
                    "${AGENT_INCLUDE_DOC_FOR(" + argument + ")}",
                    "on line 1 names no document-relative path to a `.md` file",
                )

    def test_logical_normalization_and_literal_comma_path(self) -> None:
        self.write("main/docs/a,b.md", "Comma.")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs//./a,b.md)}",
        ), "Comma.")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/x/../note.md)}",
        ), "Note.")

    def test_plugin_and_marketplace_containment(self) -> None:
        self.write("README.md", "Root.")
        self.write("main-other/note.md", "Sibling.")
        for path, reason in (
            ("../../../README.md", "names 'README.md', outside the plugin 'main'"),
            ("../../../main-other/note.md", "names 'main-other/note.md', "
             "outside the plugin 'main'"),
            ("../../../../x.md", "names '../../../../x.md', "
             "which leaves the plugin source"),
        ):
            with self.subTest(path=path):
                self.assert_failure(
                    "${AGENT_INCLUDE_DOC_FOR(codex, " + path + ")}",
                    "on line 1 " + reason,
                )

    def test_root_level_include_is_bounded_by_marketplace(self) -> None:
        self.write("docs/note.md", "Root note.")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(claude, docs/note.md)}", path="README.md",
        ), "Root note.")
        self.assert_failure(
            "${AGENT_INCLUDE_DOC_FOR(codex, ../outside.md)}",
            "on line 1 names '../outside.md', which leaves the plugin source",
            path="README.md",
        )

    def test_source_root_plugin_can_include_relative_documents(self) -> None:
        self.write("ai-plugin.yml", "name: root\ndescription: Root\n")
        self.write("docs/note.md", "Root plugin note.")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(claude, docs/note.md)}", path="README.md",
        ), "Root plugin note.")

    def test_missing_non_file_and_dangling_symlink_targets_on_dropped_hosts(self) -> None:
        (self.root / "main/docs/directory.md").mkdir()
        (self.root / "main/docs/dangling.md").symlink_to("absent.md")
        for target in ("gone.md", "directory.md", "dangling.md"):
            for host in ("claude", "codex", "pi"):
                with self.subTest(target=target, host=host):
                    self.assert_failure(
                        "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/" + target + ")}",
                        f"on line 1 names 'main/docs/{target}', "
                        "which is not a readable file", host=host,
                    )

    def test_unreadable_target_is_rejected_even_when_dropped(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("root can read files without their read permission")
        path = self.write("main/docs/unreadable.md", "Hidden.")
        path.chmod(0)
        self.addCleanup(path.chmod, 0o600)
        self.assert_failure(
            "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/unreadable.md)}",
            "on line 1 names 'main/docs/unreadable.md', "
            "which is not a readable file",
        )

    def test_frontmatter_include_reports_one_based_line(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/note.md)}"
        self.assert_failure(
            "---\nname: deep\n" + marker + "\n---\nBody.",
            "on line 3 sits in the frontmatter, where nothing can be included",
            marker,
        )

    def test_frontmatter_requires_exact_lf_terminated_delimiters(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}"
        for opening, closing in (
            ("---\r\n", "---\r\n"), ("---\n", "---\r\n"),
            ("---\r\n", "---\n"), ("---\n", "---"),
            ("---\n", ""), (" ---\n", "---\n"),
        ):
            with self.subTest(opening=opening, closing=closing):
                self.assertEqual(
                    self.render(opening + marker + "\n" + closing),
                    opening + "Note.\n" + closing,
                )

    def test_nested_include_fails_even_when_dropped_or_inside_code(self) -> None:
        nested = "${AGENT_INCLUDE_DOC_FOR(pi, note.md)}"
        for body in (nested, "```\n" + nested + "\n```", "prefix " + nested):
            self.write("main/docs/outer.md", body)
            for host in ("claude", "codex", "pi"):
                with self.subTest(body=body, host=host):
                    self.assert_failure(
                        "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/outer.md)}",
                        "on line 1 names 'main/docs/outer.md', which includes "
                        "another document: an included document includes nothing",
                        host=host,
                    )

    def test_dropped_document_parses_values_without_resolving_pi_targets(self) -> None:
        self.write("main/docs/note.md", "${AGENT_SKILL(unpublished)}")
        self.assertEqual(render_markdown(
            "Before\n${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}\nAfter",
            self.logical_path, "pi", discover_source(self.root),
        ), "Before\nAfter")
        self.write("main/docs/note.md", "${AGENT_SKILL(%s)}")
        with self.assertRaises(ValueError) as caught:
            self.render("${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}", "pi")
        self.assertEqual(
            str(caught.exception),
            "Agent placeholder '${AGENT_SKILL(%s)}' in 'main/docs/note.md' "
            "needs the skill name: write it as ${AGENT_SKILL(<skill name>)}.",
        )

    def test_dropped_document_rejects_unknown_and_malformed_markers(self) -> None:
        for marker, reason in (
            ("${AGENT_TYPO}", "names no placeholder of the vocabulary"),
            ("${AGENT_SKILL(main(extra))}",
             "is not written as a placeholder of the vocabulary"),
        ):
            self.write("main/docs/note.md", marker)
            with self.subTest(marker=marker), self.assertRaises(ValueError) as caught:
                self.render("${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/note.md)}")
            self.assertEqual(
                str(caught.exception),
                f"Agent placeholder '{marker}' in 'main/docs/note.md' {reason}.",
            )

    def test_no_argument_parser_quirks_survive_in_dropped_documents(self) -> None:
        self.write(
            "main/docs/note.md",
            "${AGENT_SUBAGENT_TOOL()} ${AGENT_QUESTION_TOOL(bad argument)}",
        )
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/note.md)}",
        ), "")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}",
        ), "Agent AskUserQuestion")

    def test_escaped_includes_remain_literal_after_one_value_pass(self) -> None:
        marker = "${AGENT_INCLUDE_DOC_FOR(claude, absent.md)}"
        self.assertEqual(self.render("Prefix $" + marker), "Prefix " + marker)
        self.write("main/docs/note.md", "$" + marker + "\n$${AGENT_TYPO}\n")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}",
        ), marker + "\n${AGENT_TYPO}")

    def test_shared_symlinks_use_each_consuming_plugin_location(self) -> None:
        shared = "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/note.md)}"
        self.write("@common/docs/Shared.md", shared)
        self.write("other/ai-plugin.yml", "name: other\ndescription: Other\n")
        self.write("other/docs/note.md", "Other note.")
        for plugin, expected in (("main", "Note."), ("other", "Other note.")):
            (self.root / plugin / "@common").symlink_to(
                self.root / "@common", target_is_directory=True,
            )
            path = plugin + "/@common/docs/Shared.md"
            content = (self.root / path).read_bytes().decode("utf-8")
            with self.subTest(plugin=plugin):
                self.assertEqual(self.render(content, path=path), expected)
        self.assert_failure(
            "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/gone.md)}",
            "on line 1 names 'main/docs/gone.md', which is not a readable file",
            path="main/@common/docs/Shared.md",
        )

    def test_shared_included_syntax_error_names_original_origin(self) -> None:
        self.write("@common/docs/Note.md", "${AGENT_TYPO}")
        (self.root / "main/@common").symlink_to(
            self.root / "@common", target_is_directory=True,
        )
        with self.assertRaises(ValueError) as caught:
            self.render("${AGENT_INCLUDE_DOC_FOR(codex, ../../@common/docs/Note.md)}")
        self.assertEqual(
            str(caught.exception),
            "Agent placeholder '${AGENT_TYPO}' in 'main/@common/docs/Note.md', "
            "a copy of '@common/docs/Note.md' names no placeholder of the vocabulary.",
        )

    def test_invalid_utf8_include_bytes_survive_selection_and_dropping(self) -> None:
        fixture = Path(__file__).with_name("include_invalid_utf8.bin").read_bytes()
        self.write("main/docs/bytes.md", fixture)
        marker = "${AGENT_INCLUDE_DOC_FOR(claude, ../../docs/bytes.md)}"
        self.assertEqual(
            self.render(marker + "\n").encode("utf-8", "surrogateescape"),
            b"Invalid: \xff\nTool: Agent\n",
        )
        for host in ("codex", "pi"):
            with self.subTest(host=host):
                self.assertEqual(render_markdown(
                    marker + "\n", self.logical_path, host,
                    discover_source(self.root),
                ), "")

    def test_host_independent_include_uses_public_rendering_api(self) -> None:
        self.write(
            "main/docs/note.md",
            "[Guide](../guide.md)\r\n${AGENT_SUBAGENT_TOOL}\n\n",
        )
        marker = "${AGENT_INCLUDE_DOC(../../docs/note.md)}"
        for host, tool in (
            ("claude", "Agent"), ("codex", "spawn_agent"),
            ("pi", "subagent"),
        ):
            with self.subTest(host=host):
                self.assertEqual(
                    self.render("Before\n  " + marker + "\nAfter", host,
                                "main/skills/deep/README.md"),
                    "Before\n[Guide](../../guide.md)\r\n" + tool + "\nAfter",
                )
                self.assertEqual(self.render(
                    marker, host, "main/skills/deep/README.md"),
                                 "[Guide](../../guide.md)\r\n" + tool)

    def test_host_independent_include_argument_and_placement(self) -> None:
        for marker in (
            "${AGENT_INCLUDE_DOC}", "${AGENT_INCLUDE_DOC()}",
            "${AGENT_INCLUDE_DOC( \t\x00\v)}",
        ):
            with self.subTest(marker=marker):
                self.assert_failure(
                    marker, "needs the document path: write it as "
                    "${AGENT_INCLUDE_DOC(<document path>)}",
                )
        marker = "${AGENT_INCLUDE_DOC(../../docs/note.md)}"
        self.assertEqual(self.render(" \t\x00" + marker + "\r\n"), "Note.\n")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC(\x00\t../../docs/note.md\v)}",
        ), "Note.")
        for content in ("prefix " + marker, marker + " suffix", marker + marker):
            with self.subTest(content=content):
                self.assert_failure(
                    content, "on line 1 shares its line with other text: "
                    "an include stands alone on its line", marker,
                )
        self.assert_failure(
            "---\nname: deep\n" + marker + "\n---\n",
            "on line 3 sits in the frontmatter, where nothing can be included",
            marker,
        )
        self.assertEqual(self.render("$" + marker), marker)

    def test_host_independent_include_paths_and_targets(self) -> None:
        self.write("main/docs/a,b.md", "Comma.")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC(../../docs//./a,b.md)}",
        ), "Comma.")
        self.assertEqual(self.render(
            "${AGENT_INCLUDE_DOC(../../docs/x/../note.md)}",
        ), "Note.")
        for path, reason in (
            ("/docs/note.md", "names no document-relative path to a `.md` file"),
            ("../../docs/note.MD", "names no document-relative path to a `.md` file"),
            ("../../docs/note.md\u00a0", "names no document-relative path to a `.md` file"),
            ("../../../README.md", "names 'README.md', outside the plugin 'main'"),
            ("../../../../x.md", "names '../../../../x.md', which leaves the plugin source"),
            ("../../docs/missing.md", "names 'main/docs/missing.md', which is not a readable file"),
        ):
            with self.subTest(path=path):
                self.assert_failure(
                    "${AGENT_INCLUDE_DOC(" + path + ")}", "on line 1 " + reason,
                )
        (self.root / "main/docs/directory.md").mkdir()
        self.assert_failure(
            "${AGENT_INCLUDE_DOC(../../docs/directory.md)}",
            "on line 1 names 'main/docs/directory.md', which is not a readable file",
        )

    def test_both_include_kinds_reject_both_nested_kinds(self) -> None:
        for outer in (
            "${AGENT_INCLUDE_DOC(../../docs/outer.md)}",
            "${AGENT_INCLUDE_DOC_FOR(codex, ../../docs/outer.md)}",
        ):
            for nested in (
                "${AGENT_INCLUDE_DOC(note.md)}",
                "${AGENT_INCLUDE_DOC_FOR(pi, note.md)}",
            ):
                self.write("main/docs/outer.md", "```\n" + nested + "\n```")
                for host in ("claude", "codex", "pi"):
                    with self.subTest(outer=outer, nested=nested, host=host):
                        self.assert_failure(
                            outer, "on line 1 names 'main/docs/outer.md', "
                            "which includes another document: an included "
                            "document includes nothing", host=host,
                        )

    def test_host_independent_shared_origin_and_surrogateescape(self) -> None:
        self.write("@common/docs/Note.md", "${AGENT_TYPO}")
        (self.root / "main/@common").symlink_to(
            self.root / "@common", target_is_directory=True,
        )
        marker = "${AGENT_INCLUDE_DOC(../../@common/docs/Note.md)}"
        with self.assertRaises(ValueError) as caught:
            self.render(marker)
        self.assertEqual(
            str(caught.exception),
            "Agent placeholder '${AGENT_TYPO}' in 'main/@common/docs/Note.md', "
            "a copy of '@common/docs/Note.md' names no placeholder of the vocabulary.",
        )
        self.write("main/docs/bytes.md", b"Invalid: \xff\n${AGENT_SUBAGENT_TOOL}\n")
        for host, tool in (
            ("claude", b"Agent"), ("codex", b"spawn_agent"),
            ("pi", b"subagent"),
        ):
            with self.subTest(host=host):
                self.assertEqual(
                    self.render("${AGENT_INCLUDE_DOC(../../docs/bytes.md)}\n", host,
                                "main/skills/deep/README.md")
                    .encode("utf-8", "surrogateescape"),
                    b"Invalid: \xff\n" + tool + b"\n",
                )

    def test_non_markdown_boundary_precedes_include_validation(self) -> None:
        content = "${AGENT_INCLUDE_DOC_FOR(cursor, absent.txt)}"
        for path in ("main/docs/data.txt", "main/docs/README.MD", "main/docs/no-suffix"):
            with self.subTest(path=path):
                self.assertEqual(self.render(content, path=path), content)
        with self.assertRaisesRegex(ValueError, "names no agent tree"):
            render_markdown(
                content, "main/docs/data.txt", "claude",
                discover_source(self.root),
            )

    def test_linked_heading_rebases_for_both_includes_all_hosts_and_depths(self) -> None:
        fragment = "### [Customer](Customer.md)\n![icon](icons/customer.png)\n"
        self.write("main/domain/map-entry.md", fragment)
        for host in ("claude", "codex", "pi"):
            for owner, target in (
                ("main/domain/map.md", "Customer.md"),
                ("main/skills/deep/README.md", "../../domain/Customer.md"),
            ):
                for marker in (
                    "${AGENT_INCLUDE_DOC(../../domain/map-entry.md)}"
                    if "skills" in owner else "${AGENT_INCLUDE_DOC(map-entry.md)}",
                    "${AGENT_INCLUDE_DOC_FOR(" + host + ", " +
                    ("../../domain/map-entry.md" if "skills" in owner else
                     "map-entry.md") + ")}",
                ):
                    with self.subTest(host=host, owner=owner, marker=marker):
                        self.assertEqual(
                            render_markdown(marker + "\n", owner, host,
                                            discover_source(self.root)),
                            "### [Customer](" + target + ")\n![icon](" +
                            ("../../domain/icons/customer.png" if "skills" in owner
                             else "icons/customer.png") + ")\n",
                        )

    def test_common_links_use_consuming_copy_not_symlink_origin(self) -> None:
        self.write("@common/domain/Order/map-entry.md", "### [Item](../Item.md)\n")
        (self.root / "main/@common").symlink_to(
            self.root / "@common", target_is_directory=True,
        )
        marker = "${AGENT_INCLUDE_DOC(../@common/domain/Order/map-entry.md)}"
        self.assertEqual(self.render(marker + "\n", path="main/domain/map.md"),
                         "### [Item](../@common/domain/Item.md)\n")
        marker = "${AGENT_INCLUDE_DOC(../../@common/domain/Order/map-entry.md)}"
        self.assertEqual(self.render(marker + "\n", path="main/skills/deep/SKILL.md"),
                         "### [Item](../../@common/domain/Item.md)\n")

    def test_reference_images_suffixes_and_literal_code(self) -> None:
        fragment = (
            "[label](../Peer.md?mode=full#part \"Title\") "
            "![photo](<images/a b.png#crop> 'Caption')\n"
            "[ref]: <../Peer.md?x=1#part> \"Ref title\"\r\n"
            "[other]: images/icon.svg#small\n"
            "[remote](https://example.org/x) [anchor](#here) "
            "[absolute](/docs/x.md) [network](//example.org/a)\n"
            "`[code](../Peer.md)` \\[escaped](../Peer.md)\n"
            "```md\n[example](../Peer.md)\n```\n"
            "    [indented](../Peer.md)\n"
            "Run ../scripts/run.py and [ordinary][ref].\n"
        )
        self.write("main/docs/entry.md", fragment)
        marker = "${AGENT_INCLUDE_DOC(../../docs/entry.md)}"
        expected = (
            "[label](../../Peer.md?mode=full#part \"Title\") "
            "![photo](<../../docs/images/a b.png#crop> 'Caption')\n"
            "[ref]: <../../Peer.md?x=1#part> \"Ref title\"\r\n"
            "[other]: ../../docs/images/icon.svg#small\n"
            "[remote](https://example.org/x) [anchor](#here) "
            "[absolute](/docs/x.md) [network](//example.org/a)\n"
            "`[code](../Peer.md)` \\[escaped](../Peer.md)\n"
            "```md\n[example](../Peer.md)\n```\n"
            "    [indented](../Peer.md)\n"
            "Run ../scripts/run.py and [ordinary][ref].\n"
        )
        self.assertEqual(self.render(marker + "\n"), expected)
        self.assertEqual(self.render(fragment), fragment)

    def test_link_labels_can_contain_code_and_nested_brackets(self) -> None:
        for label in ("the `Ticket` entry", "Ticket [alias]", "Ticket (`TrmTicket`)"):
            fragment = "### [" + label + "](Peer.md)\n"
            self.write("main/docs/entry.md", fragment)
            for host in ("claude", "codex", "pi"):
                with self.subTest(label=label, host=host):
                    self.assertEqual(
                        self.render("${AGENT_INCLUDE_DOC(../../docs/entry.md)}\n",
                                    host, "main/skills/deep/README.md"),
                        "### [" + label + "](../../docs/Peer.md)\n",
                    )

    def test_link_destinations_allow_trailing_whitespace(self) -> None:
        for destination in ("Peer.md ", "Peer.md\t", "<Peer.md> "):
            self.write("main/docs/entry.md", "[Peer](" + destination + ")\n")
            expected = destination.replace("Peer.md", "../../docs/Peer.md")
            for host in ("claude", "codex", "pi"):
                with self.subTest(destination=destination, host=host):
                    self.assertEqual(
                        self.render("${AGENT_INCLUDE_DOC(../../docs/entry.md)}\n",
                                    host, "main/skills/deep/README.md"),
                        "[Peer](" + expected + ")\n",
                    )

    def test_multiline_code_spans_and_fence_contents_stay_literal(self) -> None:
        for literal in (
            "`literal\n[code](Peer.md)\n`\n",
            "``literal\r\n[code](Peer.md)\r\n``\r\n",
            "```md\n`unpaired\n[code](Peer.md)\n```\n",
        ):
            self.write("main/docs/entry.md", literal + "[Peer](Peer.md)\n")
            for host in ("claude", "codex", "pi"):
                with self.subTest(literal=literal, host=host):
                    self.assertEqual(
                        self.render("${AGENT_INCLUDE_DOC(../../docs/entry.md)}\n",
                                    host, "main/skills/deep/README.md"),
                        literal + "[Peer](../../docs/Peer.md)\n",
                    )

    def test_ordinary_content_without_includes_keeps_line_endings(self) -> None:
        content = "---\r\nname: deep\n---\r\nBody\rOnly\nTail"
        self.assertEqual(self.render(content), content)


if __name__ == "__main__":
    unittest.main()
