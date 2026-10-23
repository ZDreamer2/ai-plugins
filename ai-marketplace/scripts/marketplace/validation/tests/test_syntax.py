"""Preserve selection, attribution and read-only source checking."""

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from marketplace.validation import check_syntax


class SyntaxTest(unittest.TestCase):
    def test_mixed_changes_preserve_order_and_never_execute(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {
                'valid.py': b'from pathlib import Path\nPath("trap").touch()\n',
                'invalid.py': b'def broken(:\n',
                'command': b'#!/usr/bin/env python3\nraise RuntimeError()\n',
                'valid.json': b'{"ok": true}',
                'bad.json': b'{',
                'python.json': b'#!/usr/bin/env python3\nx = 1\n',
                'invalid-encoding.py': b'# coding: utf-8\nx = "\xff"\n',
                'invalid-encoding.json': b'"\xff"',
                'source.PY': b'if:\n',
                'source.JSON': b'{',
                'late-shebang': b'\n#!/usr/bin/python\nif:\n',
                'doc.md': b'# Docs\n',
                'deleted.py': b'if:\n',
            }
            for name, data in files.items():
                (root / name).write_bytes(data)
            (root / 'link.py').symlink_to(root / 'invalid.py')
            (root / 'folder.py').mkdir()
            names = list(files) + ['link.py', 'folder.py', 'missing.py']
            changes = [
                {'repo': f'repo-{index}', 'path': name,
                 'kind': 'deleted' if name == 'deleted.py' else 'modified'}
                for index, name in enumerate(names)
            ]
            result = check_syntax({'root': directory, 'changes': changes})
            expected = list(files)[:8]
            self.assertEqual([], result['changed'])
            self.assertEqual([
                {'name': 'JSON syntax' if name in ('valid.json', 'bad.json',
                                                 'invalid-encoding.json')
                 else 'Python syntax', 'repo': f'repo-{index}', 'path': name}
                for index, name in enumerate(expected)
            ], result['ran'])
            failed = ['invalid.py', 'bad.json', 'invalid-encoding.py',
                      'invalid-encoding.json']
            self.assertEqual(failed, [item['path'] for item in result['findings']])
            for finding in result['findings']:
                index = names.index(finding['path'])
                self.assertEqual(f'repo-{index}', finding['repo'])
                self.assertTrue(finding['message'].startswith(
                    'JSON syntax: ' if finding['path'].endswith('.json')
                    else 'Python syntax: '))
            self.assertEqual(files, {name: (root / name).read_bytes() for name in files})
            self.assertEqual(set(names) - {'missing.py'},
                             {path.name for path in root.iterdir()})

    def test_execution_errors_reach_protocol_caller(self) -> None:
        with self.assertRaises(KeyError):
            check_syntax({})
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'source.py').touch()
            with patch.object(Path, 'read_bytes', side_effect=OSError('cannot read')):
                with self.assertRaisesRegex(OSError, 'cannot read'):
                    check_syntax({'root': directory, 'changes': [
                        {'repo': '.', 'path': 'source.py', 'kind': 'added'},
                    ]})
