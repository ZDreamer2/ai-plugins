"""Exercise the checker JSON contract with source files that must never execute."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1] / 'on-diff-check'
PLUGIN_PATH = Path('ai-marketplace')


class DiffCheckTest(unittest.TestCase):
    def test_syntax_findings_deletions_and_no_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            sources = {
                'valid.py': 'raise RuntimeError("must not execute")\n',
                'invalid.py': 'def broken(:\n',
                'command': '#!/usr/bin/env python3\nif:\n',
                'valid.json': '{"ok": true}',
                'invalid.json': '{',
                'doc.md': '# Docs\n',
            }
            changes = []
            for name, content in sources.items():
                (folder / name).write_text(content)
                changes.append({'repo': '.', 'path': str((folder / name).relative_to(folder)), 'kind': 'added'})
            changes.append({'repo': '.', 'path': 'removed.py', 'kind': 'deleted'})
            payload = {'root': str(folder), 'changes': changes}
            result = subprocess.run([str(CHECKER)], cwd=folder, input=json.dumps(payload), text=True, capture_output=True, check=True)
            output = json.loads(result.stdout)
            self.assertEqual('', result.stderr)
            self.assertEqual([], output['changed'])
            self.assertEqual(5, len(output['ran']))
            self.assertEqual({'invalid.py', 'command', 'invalid.json'}, {Path(item['path']).name for item in output['findings']})
            self.assertFalse((folder / '__pycache__').exists())
            self.assertEqual(sources, {path.name: path.read_text() for path in folder.iterdir()})

    def test_markdown_only_does_not_claim_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'README.md').write_text('# Marketplace\n')
            payload = {'root': directory, 'changes': [{'repo': '.', 'path': 'README.md', 'kind': 'modified'}]}
            result = subprocess.run([str(CHECKER)], input=json.dumps(payload), text=True, capture_output=True, check=True)
            self.assertEqual({'changed': [], 'findings': [], 'ran': []}, json.loads(result.stdout))

    def test_empty_group_claims_no_checks(self):
        result = subprocess.run(
            [str(CHECKER)], input=json.dumps({'root': '.', 'changes': []}),
            text=True, capture_output=True, check=True,
        )
        self.assertEqual({'changed': [], 'findings': [], 'ran': []}, json.loads(result.stdout))

    def test_bad_input_is_execution_failure(self):
        result = subprocess.run([str(CHECKER)], input='{}', text=True, capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual('', result.stdout)
        self.assertIn('on-diff-check:', result.stderr)

    def test_protocol_failure_categories(self) -> None:
        for payload in ['{', '{}', '[]', '{"root": null, "changes": []}',
                        '{"root": ".", "changes": [{}]}']:
            with self.subTest(payload=payload):
                result = subprocess.run([str(CHECKER)], input=payload, text=True,
                                        capture_output=True)
                self.assertEqual(1, result.returncode)
                self.assertEqual('', result.stdout)
                self.assertTrue(result.stderr.startswith('on-diff-check: '))

    def test_file_read_failure_is_not_a_syntax_finding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'source.py').touch()
            payload = {'root': directory, 'changes': [
                {'repo': '.', 'path': 'source.py', 'kind': 'modified'},
            ]}
            code = (
                'from pathlib import Path\n'
                'from unittest.mock import patch\n'
                'import runpy, sys\n'
                'with patch.object(Path, "read_bytes", side_effect=OSError("read failed")):\n'
                '    runpy.run_path(sys.argv[1], run_name="__main__")\n'
            )
            result = subprocess.run([sys.executable, '-S', '-c', code, str(CHECKER)],
                                    input=json.dumps(payload), text=True,
                                    capture_output=True)
            self.assertEqual(1, result.returncode)
            self.assertEqual('', result.stdout)
            self.assertEqual('on-diff-check: read failed\n', result.stderr)

    def test_isolated_marketplace_and_import_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marketplace = root / 'isolated-marketplace'
            plugin = marketplace / PLUGIN_PATH
            # Only this concrete adapter and its owning validator plugin accompany the copy.
            shutil.copytree(CHECKER.parents[3] / PLUGIN_PATH, plugin, symlinks=True,
                            ignore=shutil.ignore_patterns('@common', '__pycache__'))
            copied_checker = marketplace / '@common/docs/forge/on-diff-check'
            copied_checker.parent.mkdir(parents=True)
            shutil.copy2(CHECKER, copied_checker)
            unrelated = root / 'unrelated'
            unrelated.mkdir()
            (unrelated / 'valid.py').write_text('raise RuntimeError("no execution")\n')
            (unrelated / 'invalid.py').write_text('if:\n')
            payload = {'root': str(unrelated), 'changes': [
                {'repo': 'copied', 'path': 'valid.py', 'kind': 'modified'},
                {'repo': 'copied', 'path': 'invalid.py', 'kind': 'added'},
            ]}
            result = subprocess.run([sys.executable, '-I', '-S', '-B', str(copied_checker)],
                                    cwd=unrelated, input=json.dumps(payload), text=True,
                                    capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual('', result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual([], output['changed'])
            self.assertEqual(['valid.py', 'invalid.py'],
                             [item['path'] for item in output['ran']])
            self.assertEqual(['invalid.py'],
                             [item['path'] for item in output['findings']])
            self.assertEqual({'valid.py', 'invalid.py'},
                             {path.name for path in unrelated.iterdir()})
            probe = '''
import sys
sys.path.insert(0, sys.argv[1])
from marketplace.validation import check_syntax, validate_pi_distribution
result = check_syntax({'root': '.', 'changes': [
    {'repo': '.', 'path': 'valid.py', 'kind': 'modified'},
]})
assert not result['findings']
assert not any(name == 'yaml' or name.startswith('marketplace.source')
               or name.startswith('marketplace.build')
               or name.startswith('marketplace._yaml')
               or name.startswith('marketplace._vendor')
               or name == 'subprocess' for name in sys.modules)
from marketplace.source import read_manifest
manifest = read_manifest(sys.argv[2])
assert manifest['name'] == 'ai-marketplace'
assert 'yaml' not in sys.modules
'''
            result = subprocess.run([
                sys.executable, '-I', '-S', '-B', '-c', probe,
                str(plugin / 'scripts'), str(plugin / 'ai-plugin.yml'),
            ], cwd=unrelated, text=True, capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == '__main__':
    unittest.main()
