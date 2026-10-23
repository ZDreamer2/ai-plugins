"""Intent: Check bundled parsing against saved Symfony default-flags results."""

import base64
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from marketplace import TaggedValue, parse_yaml


def _expected(record: dict) -> object:
    kind, value = record["type"], record["value"]
    if kind == "list":
        return [_expected(item) for item in value]
    if kind == "dict":
        return {_expected(key): _expected(item) for key, item in value}
    if kind == "bytes":
        return base64.b64decode(value)
    if kind == "tagged":
        return TaggedValue(**value)
    if kind == "float" and value in ("+inf", "-inf"):
        return math.inf if value == "+inf" else -math.inf
    return value


class YamlTest(unittest.TestCase):
    def assert_exact(self, actual: object, expected: object) -> None:
        self.assertIs(type(actual), type(expected))
        self.assertEqual(actual, expected)
        if isinstance(expected, dict):
            for actual_key, expected_key in zip(actual, expected):
                self.assert_exact(actual_key, expected_key)
                self.assert_exact(actual[actual_key], expected[expected_key])
        elif isinstance(expected, list):
            for actual_item, expected_item in zip(actual, expected):
                self.assert_exact(actual_item, expected_item)

    def test_saved_symfony_default_flag_results(self) -> None:
        # Captured from library/vendor/symfony/yaml via Yaml::parse(source),
        # with no flags. The fixture is independent of PHP at test runtime.
        fixture = Path(__file__).with_name("symfony_yaml.json")
        for case in json.loads(fixture.read_text(encoding="utf-8")):
            with self.subTest(source=case["source"]):
                if case.get("error"):
                    with self.assertRaises(ValueError):
                        parse_yaml(case["source"])
                else:
                    self.assert_exact(parse_yaml(case["source"]), _expected(case["expected"]))

    def test_flow_collection_line_suffix_symfony_results(self) -> None:
        # Exact default-flags Yaml::parse probes against the repository's
        # Symfony installation. Only the outer collection's line tail is lost.
        cases = [
            ("argument-hint: [issue-id|IssueSpec-path] [branch]",
             {"argument-hint": ["issue-id|IssueSpec-path"]}),
            ("key: [a] garbage", {"key": ["a"]}),
            ("key: {a: b} suffix", {"key": {"a": "b"}}),
            ("- [a] garbage", [["a"]]),
            ("- {a: b} suffix", [{"a": "b"}]),
            ("[a] garbage", ["a"]),
            ("{a: b} suffix", {"a": "b"}),
            ("---\n[a] garbage", ["a"]),
            ("key:\n  [a] garbage", {"key": ["a"]}),
            ("key: [a]garbage", {"key": ["a"]}),
            ("key: [a] : bad", {"key": ["a"]}),
            ('key: [a] "unterminated', {"key": ["a"]}),
            ("key: &x [a] garbage\ncopy: *x",
             {"key": ["a"], "copy": ["a"]}),
            ("- &x [a] garbage\n- *x", [["a"], ["a"]]),
            ('key: ["x] y", {a: "}"}] suffix\nnext: 2',
             {"key": ["x] y", {"a": "}"}], "next": 2}),
            ("key: [a, {b: [c]}\n ] garbage\nnext: true",
             {"key": ["a", {"b": ["c"]}], "next": True}),
            ("key: [a # ] ignore\n ] suffix", {"key": ["a"]}),
            ("key: [a\n  ] suffix\nnext: false",
             {"key": ["a"], "next": False}),
            ('key: "[a] garbage"', {"key": "[a] garbage"}),
            ("key: |\n  [a] garbage\nnext: b",
             {"key": "[a] garbage\n", "next": "b"}),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assert_exact(parse_yaml(source), expected)

    def test_flow_collection_suffix_does_not_hide_symfony_errors(self) -> None:
        sources = [
            "{key: [a] garbage}",
            "key: {a: [b] garbage} suffix",
            "key: [a} garbage",
            "key: [a garbage",
            "key: {a: b suffix",
            'key: ["a] suffix',
            "[a]\nnext: true",
            "key: [a] garbage\nkey: b",
            "key: !!str [a] garbage",
            "key: ! [a] garbage",
            "key: !php/object [a] garbage",
            "key: [*missing] garbage",
        ]
        for source in sources:
            with self.subTest(source=source), self.assertRaises(ValueError):
                parse_yaml(source)

    def test_empty_container_shapes(self) -> None:
        self.assert_exact(parse_yaml("{}"), {})
        self.assert_exact(parse_yaml("[]"), [])

    def test_nontext_and_unreadable_scalar_input_fail_usefully(self) -> None:
        for value in (None, b"name: test", 3, "\x00", "date: 2026-99-30"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_yaml(value)

    def test_no_object_constructor_can_execute(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            command = f"touch {marker}"
            source = "!!python/object/apply:os.system [" + json.dumps(command) + "]"
            with self.assertRaises(ValueError):
                parse_yaml(source)
            self.assertFalse(marker.exists())

    def test_isolated_copy_with_conflicting_global_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = Path(__file__).resolve().parents[2]
            shutil.copytree(scripts / "marketplace", root / "marketplace")
            (root / "yaml.py").write_text("raise RuntimeError('global YAML imported')\n")
            code = """
import sys
sys.path.insert(0, sys.argv[1])
import marketplace
assert not any(name.startswith('marketplace._vendor') for name in sys.modules)
assert marketplace.parse_yaml('yes: on\\ndate: 2026-09-30') == {'yes': 'on', 'date': 1790726400}
assert 'yaml' not in sys.modules
assert not any(name.startswith('marketplace._vendor.yaml.cyaml') for name in sys.modules)
assert marketplace.parse_yaml('!!binary /w==') == b'\\xff'
"""
            result = subprocess.run(
                [sys.executable, "-I", "-S", "-c", code, str(root)],
                cwd=directory, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
