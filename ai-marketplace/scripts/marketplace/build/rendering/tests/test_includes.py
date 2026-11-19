"""Jinja composition and marketplace link rebasing through the rendering API."""

import os
from pathlib import Path
import tempfile
import unittest

from marketplace.build.rendering import render_file, render_markdown
from marketplace.source import discover_source


HOSTS = ("claude", "codex", "pi")


def include(path: str, host: str | None = None) -> str:
    tag = "{% include '" + path + "' %}"
    if host is None:
        return tag
    return "{% if build.host == '" + host + "' %}\n" + tag + "\n{% endif %}"


class IncludeTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.logical_path = "main/skills/deep/README.md"
        self.write("main/ai-plugin.yml", "name: main\ndescription: Main\n")
        self.write("main/docs/note.md", "Note.")

    def write(self, relative: str, content: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def render(self, body: str, host: str = "claude", path: str | None = None) -> str:
        return render_file(body, path or self.logical_path, host, discover_source(self.root))

    def test_selected_includes_and_placeholder_pass_for_every_host(self) -> None:
        for host in HOSTS:
            self.write(f"main/docs/{host}.md", host + " ${AGENT_SUBAGENT_TOOL}.\n")
        content = "Before.\n" + "\n".join(
            include(f"../../docs/{host}.md", host) for host in HOSTS
        ) + "\n\nAfter."
        for host, tool in zip(HOSTS, ("Agent", "spawn_agent", "subagent")):
            with self.subTest(host=host):
                self.assertEqual(render_markdown(
                    content, self.logical_path, host, discover_source(self.root),
                ), f"Before.\n{host} {tool}.\n\nAfter.")

    def test_fragment_trailing_newlines_are_preserved_and_tag_line_is_trimmed(self) -> None:
        for fragment in ("Text", "Text\n", "Text\n\n", "", "\n\n"):
            with self.subTest(fragment=fragment):
                self.write("main/docs/note.md", fragment)
                tag = include("../../docs/note.md")
                self.assertEqual(self.render(tag), fragment)
                self.assertEqual(self.render("Before\n" + tag + "\nAfter"),
                                 "Before\n" + fragment + "After")

    def test_jinja_normalizes_mixed_line_endings(self) -> None:
        self.write("main/docs/note.md", "[Guide](../guide.md)\r\nRun ../scripts/run.py\nLast\r\n\r\n")
        self.assertEqual(self.render("Before\r\n" + include("../../docs/note.md") + "\r\nAfter\nTail"),
                         "Before\n[Guide](../../guide.md)\nRun ../scripts/run.py\nLast\n\nAfter\nTail")

    def test_include_path_normalization_and_literal_comma(self) -> None:
        self.write("main/docs/a,b.md", "Comma.")
        self.assertEqual(self.render(include("../../docs//./a,b.md")), "Comma.")
        self.assertEqual(self.render(include("../../docs/x/../note.md")), "Note.")

    def test_include_requires_relative_markdown_path(self) -> None:
        for path in ("/docs/note.md", "../../docs/note.txt", "../../docs/note.MD",
                     "../../docs/note.md\u00a0", r"../../docs\\note.md"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "relative Markdown path"):
                self.render(include(path))

    def test_include_must_be_required_and_literal_even_in_unselected_branch(self) -> None:
        for argument in ("fragment", "['../../docs/note.md']", "'../../docs/note.md' ignore missing"):
            with self.subTest(argument=argument), self.assertRaisesRegex(ValueError, "required literal include path"):
                self.render("{% if build.host == 'pi' %}{% include " + argument + " %}{% endif %}")

    def test_external_fragments_are_allowed_inside_marketplace_source(self) -> None:
        for path, text in (("README.md", "Root."), ("main-other/note.md", "Sibling."),
                           ("@common/note.md", "Shared.")):
            self.write(path, text)
            for host in HOSTS:
                with self.subTest(path=path, host=host):
                    self.assertEqual(self.render(include("../../../" + path), host), text)
                    self.assertEqual(self.render(include("../../../" + path, "codex"), host),
                                     text if host == "codex" else "")
        with self.assertRaisesRegex(ValueError, "leaves the marketplace source"):
            self.render(include("../../../../x.md", "codex"))

    def test_external_fragment_links_require_existing_plugin_local_targets(self) -> None:
        self.write("@common/note.md", "[Guide](../main/docs/note.md#section)\n"
                   "![Image][image]\n[image]: ../main/image.png\n"
                   "[Web](https://example.com) [Anchor](#local)\n"
                   "`[Literal](missing.md)`\n")
        self.write("main/image.png", b"image")
        path = "../../../@common/note.md"
        for host in HOSTS:
            with self.subTest(host=host):
                self.assertEqual(self.render(include(path), host),
                                 "[Guide](../../docs/note.md#section)\n"
                                 "![Image][image]\n[image]: ../../image.png\n"
                                 "[Web](https://example.com) [Anchor](#local)\n"
                                 "`[Literal](missing.md)`\n")
        self.write("README.md", "Exists outside plugin.")
        for target in ("README.md", "main/docs/missing.md"):
            self.write("@common/note.md", f"[Unavailable](../{target})")
            with self.subTest(target=target), self.assertRaisesRegex(ValueError,
                    f"link target '{target}' is not published in plugin 'main'"):
                self.render(include(path, "codex"), "claude")

    def test_root_level_include_is_bounded_by_marketplace(self) -> None:
        self.write("docs/note.md", "Root note.")
        self.assertEqual(self.render(include("docs/note.md"), path="README.md"), "Root note.")
        with self.assertRaisesRegex(ValueError, "leaves the marketplace source"):
            self.render(include("../outside.md", "codex"), path="README.md")

    def test_source_root_plugin_can_include_relative_documents(self) -> None:
        self.write("ai-plugin.yml", "name: root\ndescription: Root\n")
        self.write("docs/note.md", "Root plugin note.")
        self.assertEqual(self.render(include("docs/note.md"), path="README.md"), "Root plugin note.")

    def test_missing_non_file_and_dangling_symlink_targets_in_any_branch(self) -> None:
        (self.root / "main/docs/directory.md").mkdir()
        (self.root / "main/docs/dangling.md").symlink_to("absent.md")
        for target in ("gone.md", "directory.md", "dangling.md"):
            for host in HOSTS:
                with self.subTest(target=target, host=host), self.assertRaisesRegex(
                    ValueError, f"missing include 'main/docs/{target}'",
                ):
                    self.render(include("../../docs/" + target, "codex"), host)

    def test_unreadable_fragment_fails_even_in_unselected_branch(self) -> None:
        if os.geteuid() == 0:
            self.skipTest("root can read files without their read permission")
        fragment = self.write("main/docs/unreadable.md", "Hidden.")
        fragment.chmod(0)
        self.addCleanup(fragment.chmod, 0o600)
        with self.assertRaisesRegex((ValueError, OSError), "unreadable.md"):
            self.render(include("../../docs/unreadable.md", "codex"), "claude")

    def test_fragment_outside_source_via_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "outside.md"
            target.write_text("Outside.", encoding="utf-8")
            (self.root / "main/docs/escape.md").symlink_to(target)
            with self.assertRaisesRegex(ValueError, "missing include 'main/docs/escape.md'"):
                self.render(include("../../docs/escape.md"))

    def test_unselected_fragment_does_not_resolve_placeholders(self) -> None:
        self.write("main/docs/note.md", "${AGENT_SKILL(unpublished)}")
        self.assertEqual(self.render("Before\n" + include("../../docs/note.md", "claude")
                                     + "\nAfter", "pi"), "Before\nAfter")
        with self.assertRaisesRegex(ValueError, "does not name a published Pi skill"):
            self.render(include("../../docs/note.md"), "pi")

    def test_nested_includes_use_declaring_document_for_lookup_and_final_output_for_links(self) -> None:
        self.write("main/docs/outer.md", "Outer [link](guide.md)\n" + include("nested/inner.md"))
        self.write("main/docs/nested/inner.md", "Inner [link](../peer.md)\n" + include("../note.md"))
        self.assertEqual(self.render(include("../../docs/outer.md")),
                         "Outer [link](../../docs/guide.md)\nInner [link](../../docs/peer.md)\nNote.")

    def test_include_cycle_reports_logical_chain_even_in_unselected_branch(self) -> None:
        self.write("main/docs/outer.md", include("nested/inner.md"))
        self.write("main/docs/nested/inner.md", include(".././outer.md", "pi"))
        with self.assertRaisesRegex(ValueError, "Include cycle: main/skills/deep/README.md -> "
                                   "main/docs/outer.md -> main/docs/nested/inner.md -> main/docs/outer.md"):
            self.render(include("../../docs/outer.md"), "claude")

    def test_fragment_context_and_assignment_scope(self) -> None:
        self.write("main/docs/note.md", "{{ label }}:{{ build.host }}\n"
                   "{% set label = 'child' %}\n" + include("nested.md"))
        self.write("main/docs/nested.md", "{{ label }}:{{ build.host }}\n")
        content = (
            "{% set label = 'parent' %}\n"
            + include("../../docs/note.md") + "\n{{ label }}\n"
        )
        self.assertEqual(render_markdown(content, self.logical_path, "pi", discover_source(self.root)),
                         "parent:pi\nchild:pi\nparent\n")
        with self.assertRaisesRegex(ValueError, "'label' is undefined"):
            render_markdown("{{ label }}", self.logical_path, "pi", discover_source(self.root))

    def test_build_host_cannot_be_shadowed(self) -> None:
        with self.assertRaisesRegex(ValueError, "build is reserved"):
            self.render("{% set build = 'pi' %}Body")
        self.write("main/docs/note.md", "{% set build = 'pi' %}")
        with self.assertRaisesRegex(ValueError, "main/docs/note.md:1: build is reserved"):
            self.render(include("../../docs/note.md", "pi"), "claude")

    def test_fragments_cannot_set_runtime_frontmatter(self) -> None:
        self.write("main/docs/note.md", "---\ndescription: Fragment\n---\nNote.")
        with self.assertRaisesRegex(ValueError, "main/docs/note.md: included fragments cannot set runtime frontmatter"):
            self.render(include("../../docs/note.md"))

    def test_active_legacy_includes_fail_and_escaped_examples_stay_literal(self) -> None:
        for marker in ("${AGENT_INCLUDE_DOC(absent.md)}", "${AGENT_INCLUDE_DOC_FOR(claude, absent.md)}"):
            with self.subTest(marker=marker):
                with self.assertRaisesRegex(ValueError, "is retired; use a Jinja include"):
                    render_markdown(marker, self.logical_path, "claude", discover_source(self.root))
                self.assertEqual(self.render("Prefix $" + marker), "Prefix " + marker)
                self.write("main/docs/note.md", marker)
                with self.assertRaisesRegex(ValueError, "main/docs/note.md.*is retired"):
                    self.render(include("../../docs/note.md"))
                self.write("main/docs/note.md", "$" + marker + "\n$${AGENT_TYPO}\n")
                self.assertEqual(self.render(include("../../docs/note.md")), marker + "\n${AGENT_TYPO}\n")

    def test_shared_symlinks_use_each_consuming_plugin_location(self) -> None:
        shared = self.write("@common/docs/Shared.md", include("../../docs/note.md"))
        self.write("other/ai-plugin.yml", "name: other\ndescription: Other\n")
        self.write("other/docs/note.md", "Other note.")
        for plugin, expected in (("main", "Note."), ("other", "Other note.")):
            (self.root / plugin / "@common").symlink_to(self.root / "@common", target_is_directory=True)
            path = plugin + "/@common/docs/Shared.md"
            with self.subTest(plugin=plugin):
                self.assertEqual(render_file(shared.read_text(encoding="utf-8"), path, "claude",
                                             discover_source(self.root)), expected)
        with self.assertRaisesRegex(ValueError, "main/@common/docs/Shared.md:1: missing include 'main/docs/gone.md'"):
            self.render(include("../../docs/gone.md"), path="main/@common/docs/Shared.md")

    def test_shared_fragment_syntax_error_names_logical_include_path(self) -> None:
        self.write("@common/docs/Note.md", "First\n{% unknown_tag %}\n")
        (self.root / "main/@common").symlink_to(self.root / "@common", target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "main/@common/docs/Note.md:2:.*unknown_tag"):
            self.render(include("../../@common/docs/Note.md", "codex"))

    def test_invalid_utf8_fragment_bytes_survive_composition(self) -> None:
        fixture = Path(__file__).with_name("include_invalid_utf8.bin").read_bytes()
        self.write("main/docs/bytes.md", fixture)
        for host, tool in zip(HOSTS, (b"Agent", b"spawn_agent", b"subagent")):
            with self.subTest(host=host):
                self.assertEqual(self.render(include("../../docs/bytes.md"), host)
                                 .encode("utf-8", "surrogateescape"), b"Invalid: \xff\nTool: " + tool + b"\n")
                self.assertEqual(self.render(include("../../docs/bytes.md", "claude"), host)
                                 .encode("utf-8", "surrogateescape"),
                                 b"Invalid: \xff\nTool: Agent\n" if host == "claude" else b"")

    def test_default_rendering_opt_out_and_non_markdown_boundaries(self) -> None:
        body = include("absent.md")
        source = discover_source(self.root)
        literal = "---\nbuild-template: false\n---\n" + body
        self.assertEqual(render_markdown(literal, self.logical_path, "claude", source), body)
        with self.assertRaisesRegex(ValueError, "missing include"):
            render_markdown(body, self.logical_path, "claude", source)
        for path in ("main/docs/data.txt", "main/docs/README.MD", "main/docs/no-suffix"):
            with self.subTest(path=path):
                self.assertEqual(self.render(literal, path=path), literal)

    def test_opted_out_fragment_keeps_its_literals_and_rebases_its_links(self) -> None:
        example = "{{ title }} {% endraw %} {%} [Note](peer.md)\r\n"
        self.write("main/docs/note.md", "---\nbuild-template: false\n---\n" + example)
        self.assertEqual(self.render(include("../../docs/note.md")),
                         example.replace("(peer.md)", "(../../docs/peer.md)"))

    def test_linked_heading_rebases_for_all_hosts_and_depths(self) -> None:
        self.write("main/domain/map-entry.md", "### [Customer](Customer.md)\n![icon](icons/customer.png)\n")
        for host in HOSTS:
            for owner, prefix in (("main/domain/map.md", ""),
                                  ("main/skills/deep/README.md", "../../domain/")):
                with self.subTest(host=host, owner=owner):
                    self.assertEqual(self.render(include(prefix + "map-entry.md", host), host, owner),
                                     f"### [Customer]({prefix}Customer.md)\n![icon]({prefix}icons/customer.png)\n")

    def test_common_links_use_consuming_copy_not_symlink_origin(self) -> None:
        self.write("@common/domain/Order/map-entry.md", "### [Item](../Item.md)\n")
        (self.root / "main/@common").symlink_to(self.root / "@common", target_is_directory=True)
        for owner, prefix in (("main/domain/map.md", "../"), (self.logical_path, "../../")):
            with self.subTest(owner=owner):
                self.assertEqual(self.render(include(prefix + "@common/domain/Order/map-entry.md"), path=owner),
                                 f"### [Item]({prefix}@common/domain/Item.md)\n")

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
        expected = (
            "[label](../../Peer.md?mode=full#part \"Title\") "
            "![photo](<../../docs/images/a b.png#crop> 'Caption')\n"
            "[ref]: <../../Peer.md?x=1#part> \"Ref title\"\n"
            "[other]: ../../docs/images/icon.svg#small\n"
            "[remote](https://example.org/x) [anchor](#here) "
            "[absolute](/docs/x.md) [network](//example.org/a)\n"
            "`[code](../Peer.md)` \\[escaped](../Peer.md)\n"
            "```md\n[example](../Peer.md)\n```\n"
            "    [indented](../Peer.md)\n"
            "Run ../scripts/run.py and [ordinary][ref].\n"
        )
        self.assertEqual(self.render(include("../../docs/entry.md")), expected)
        self.assertEqual(self.render(fragment), fragment)

    def test_link_labels_can_contain_code_and_nested_brackets(self) -> None:
        for label in ("the `Ticket` entry", "Ticket [alias]", "Ticket (`TrmTicket`)"):
            self.write("main/docs/entry.md", f"### [{label}](Peer.md)\n")
            for host in HOSTS:
                with self.subTest(label=label, host=host):
                    self.assertEqual(self.render(include("../../docs/entry.md"), host),
                                     f"### [{label}](../../docs/Peer.md)\n")

    def test_link_destinations_allow_trailing_whitespace(self) -> None:
        for destination in ("Peer.md ", "Peer.md\t", "<Peer.md> "):
            self.write("main/docs/entry.md", f"[Peer]({destination})\n")
            expected = destination.replace("Peer.md", "../../docs/Peer.md")
            for host in HOSTS:
                with self.subTest(destination=destination, host=host):
                    self.assertEqual(self.render(include("../../docs/entry.md"), host), f"[Peer]({expected})\n")

    def test_multiline_code_spans_and_fence_contents_stay_literal(self) -> None:
        for literal in ("`literal\n[code](Peer.md)\n`\n", "``literal\r\n[code](Peer.md)\r\n``\r\n",
                        "```md\n`unpaired\n[code](Peer.md)\n```\n"):
            self.write("main/docs/entry.md", literal + "[Peer](Peer.md)\n")
            for host in HOSTS:
                with self.subTest(literal=literal, host=host):
                    self.assertEqual(self.render(include("../../docs/entry.md"), host),
                                     literal.replace("\r\n", "\n") + "[Peer](../../docs/Peer.md)\n")

    def test_non_opted_in_content_keeps_line_endings(self) -> None:
        content = "---\r\nname: deep\n---\r\nBody\rOnly\nTail"
        self.assertEqual(render_file(content, self.logical_path, "claude", discover_source(self.root)), content)


if __name__ == "__main__":
    unittest.main()
