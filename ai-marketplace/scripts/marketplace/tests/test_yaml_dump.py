"""Exact fixtures derived from the local Symfony default dumper, without PHP."""

import copy
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from marketplace import TaggedValue, dump_yaml, parse_yaml


class YamlDumpTests(unittest.TestCase):
    def test_retained_types_and_depth(self) -> None:
        value = {
            "name": ["x", {"quoted": "true", "empty": []}],
            "description": "Use tools.", "truth": True, "false": False,
            "null": None, "count": 3, "whole": 2.0,
        }
        suffix = (
            "description: 'Use tools.'\ntruth: true\n'false': false\n"
            "'null': null\ncount: 3\nwhole: 2.0\n"
        )
        expectations = {
            0: "{ name: [x, { quoted: 'true', empty: {  } }], "
               "description: 'Use tools.', truth: true, 'false': false, "
               "'null': null, count: 3, whole: 2.0 }",
            1: "name: [x, { quoted: 'true', empty: {  } }]\n" + suffix,
            2: "name:\n    - x\n    - { quoted: 'true', empty: {  } }\n" + suffix,
            3: "name:\n    - x\n    -\n        quoted: 'true'\n"
               "        empty: {  }\n" + suffix,
        }
        before = copy.deepcopy(value)
        for depth, expected in expectations.items():
            with self.subTest(depth=depth):
                self.assertEqual(expected, dump_yaml(value, inline=depth))
        self.assertEqual(before, value)
        parsed = parse_yaml(dump_yaml(value))
        self.assertIs(parsed["truth"], True)
        self.assertIs(parsed["false"], False)
        self.assertIsNone(parsed["null"])
        self.assertIs(type(parsed["count"]), int)
        self.assertIs(type(parsed["whole"]), float)
        self.assertEqual("true", parsed["name"][1]["quoted"])

    def test_indent_empty_and_php_array_key_order(self) -> None:
        value = {"a": {"b": [{"c": 1}]}, "empty": [], "empty-map": {},
                 "numeric": {0: "zero", 1: "one"}}
        self.assertEqual(
            "a:\n  b:\n    - { c: 1 }\nempty: {  }\nempty-map: {  }\n"
            "numeric:\n  - zero\n  - one\n", dump_yaml(value, inline=3, indent=2)
        )
        self.assertEqual("1: one\n0: zero\n", dump_yaml({1: "one", 0: "zero"}))
        self.assertEqual("- zero\n- one\n", dump_yaml({"0": "zero", "1": "one"}))
        self.assertEqual("'01': leading\n", dump_yaml({"01": "leading"}))
        for empty in ([], {}):
            self.assertEqual("{  }", dump_yaml(empty))
        self.assertEqual("policy:\n  allow_implicit_invocation: false\n", dump_yaml(
            {"policy": {"allow_implicit_invocation": False}}, indent=2
        ))

    def test_string_quoting(self) -> None:
        quoted = ["true", "FALSE", "null", "~", "yes", "off", "001", "-0",
                  "+1", "1e3", "1_000", "0xFF", "2026-10-01", "a b", "a:b",
                  "a#b", "a?b", "-start", "@start", "\u2003a", "a\u2003b"]
        for text in quoted:
            with self.subTest(text=text):
                self.assertEqual("'" + text + "'", dump_yaml(text))
                self.assertEqual(text, parse_yaml(dump_yaml(text)))
        # These Symfony defaults deliberately do not quote every evaluable
        # string. The bounded API preserves the oracle, not generic round trips.
        for text in (".inf", "0o777", "1_2.3_4", "a/b", "$tool", "é🙂", "a\\b"):
            self.assertEqual(text, dump_yaml(text))
        self.assertEqual("''", dump_yaml(""))
        self.assertEqual('"\'"', dump_yaml("'"))
        self.assertEqual("'a''b\"c'", dump_yaml("a'b\"c"))
        self.assertEqual('"a\\\\b\\n"', dump_yaml("a\\b\n"))

    def test_unicode_whitespace_and_backslashes(self) -> None:
        for text in ("a\u1680b", "a\u2000b", "\u1680a", "\u2000a"):
            self.assertEqual("'" + text + "'", dump_yaml(text))
        for text in ("a\u200bb", "a\ufeffb", "a\\b", "\\", "\\\\"):
            self.assertEqual(text, dump_yaml(text))
        self.assertEqual("!!binary YRxi", dump_yaml("a\x1cb"))
        self.assertEqual("'a\"b'", dump_yaml('a"b'))

    def test_multiline_controls_and_unicode(self) -> None:
        value = {
            "line": "first\nsecond\n", "crlf": "first\r\nsecond",
            "controls": "\0\a\b\t\n\v\f\r\x1b\x7f",
            "unicode": "a\x85\xa0\u2028\u2029b", "visible": "é🙂",
        }
        expected = (
            'line: "first\\nsecond\\n"\ncrlf: "first\\r\\nsecond"\n'
            'controls: "\\0\\a\\b\\t\\n\\v\\f\\r\\e\\x7f"\n'
            'unicode: "a\\N\\_\\L\\Pb"\nvisible: é🙂\n'
        )
        self.assertEqual(expected, dump_yaml(value))
        self.assertEqual(value, parse_yaml(expected))

    def test_binary_and_tagged_retained_values(self) -> None:
        tagged = parse_yaml("name: !note |\n  hello\n  world\n")["name"]
        value = {"tag": tagged, "binary": b"\xff\x00", "text": "é🙂",
                 "name": {1: "one", 0: "zero"}}
        self.assertEqual(
            'tag: !note "hello\\nworld\\n"\nbinary: !!binary /wA=\ntext: é🙂\n'
            'name:\n    1: one\n    0: zero\n', dump_yaml(value)
        )
        self.assertEqual('!note "hello\\n"\n', dump_yaml(TaggedValue("note", "hello\n")))
        self.assertEqual('!note "hello\\n"', dump_yaml(TaggedValue("note", "hello\n"), inline=0))
        self.assertEqual("!!binary YQFi", dump_yaml("a\x01b"))
        self.assertEqual("!!binary /wA=", dump_yaml("\udcff\0"))
        self.assertEqual("plain", dump_yaml(b"plain"))
        self.assertEqual(b"\xff\x00", parse_yaml(dump_yaml(b"\xff\x00")))

    def test_php_float_representation(self) -> None:
        fixtures = [(1.2345678901234567, "1.2345678901235"), (1e14, "1.0E+14"),
                    (1e-5, "1.0E-5"), (1e-4, "0.0001"), (-0.0, "-0.0"),
                    (math.inf, ".Inf"), (-math.inf, "-.Inf"), (math.nan, "NAN"),
                    (-17581357947954.59, "-17581357947955")]
        for value, expected in fixtures:
            self.assertEqual(expected, dump_yaml(value))

    def test_bounded_input_errors(self) -> None:
        circular = []
        circular.append(circular)
        for value in (object(), (1, 2), {True: "bool key"}, circular):
            with self.subTest(value=type(value).__name__):
                with self.assertRaises(ValueError):
                    dump_yaml(value)
        for options in ({"indent": 0}, {"indent": True}, {"inline": "2"}):
            with self.assertRaises(ValueError):
                dump_yaml({}, **options)

    def test_standalone_lazy_public_api(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            scripts = Path(temporary) / "scripts"
            shutil.copytree(
                root, scripts / "marketplace",
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            (scripts / "yaml.py").write_text(
                "raise RuntimeError('global yaml imported')\n"
            )
            program = (
                "import sys; sys.path.insert(0, sys.argv[1]); "
                "import marketplace; "
                "assert 'marketplace._yaml' not in sys.modules; "
                "assert 'marketplace._yaml_dump' not in sys.modules; "
                "assert not any(n.startswith('marketplace._vendor.yaml') "
                "for n in sys.modules); "
                "assert marketplace.dump_yaml({'description': 'true'}) == "
                "\"description: 'true'\\n\"; "
                "assert marketplace.parse_yaml('name: 2')['name'] == 2; "
                "assert 'yaml' not in sys.modules"
            )
            result = subprocess.run(
                [sys.executable, "-B", "-S", "-c", program, str(scripts)],
                cwd=temporary, capture_output=True, text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
