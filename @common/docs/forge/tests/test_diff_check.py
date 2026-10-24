"""Verify the concrete check entry independently of the caller's directory."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


CHECKER = Path(__file__).resolve().parents[1] / 'on-diff-check'


class ConcreteDiffCheckTest(unittest.TestCase):
    def test_syntax_only_without_source_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources = {
                'valid.py': 'raise RuntimeError("must not execute")\n',
                'invalid.py': 'if:\n',
                'invalid.json': '{',
                'README.md': '# Documentation\n',
            }
            for name, content in sources.items():
                (root / name).write_text(content)
            changes = [
                {'repo': 'marketplace', 'path': name, 'kind': 'added'}
                for name in sources
            ]
            changes.append({'repo': 'marketplace', 'path': 'deleted.py', 'kind': 'deleted'})
            result = subprocess.run(
                [str(CHECKER)], cwd=root, text=True, capture_output=True,
                input=json.dumps({'root': directory, 'changes': changes}), check=True,
                env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
            )
            output = json.loads(result.stdout)
            self.assertEqual('', result.stderr)
            self.assertEqual([], output['changed'])
            self.assertEqual(3, len(output['ran']))
            self.assertEqual({'invalid.py', 'invalid.json'},
                             {finding['path'] for finding in output['findings']})
            self.assertEqual(sources, {p.name: p.read_text() for p in root.iterdir()})

    def test_bad_input_fails(self) -> None:
        result = subprocess.run([str(CHECKER)], input='{}', text=True, capture_output=True)
        self.assertEqual(1, result.returncode)
        self.assertEqual('', result.stdout)
        self.assertTrue(result.stderr.startswith('on-diff-check: '))

    def test_empty_group_claims_no_checks(self) -> None:
        result = subprocess.run(
            [str(CHECKER)], input=json.dumps({'root': '.', 'changes': []}),
            text=True, capture_output=True, check=True,
        )
        self.assertEqual({'changed': [], 'findings': [], 'ran': []}, json.loads(result.stdout))


if __name__ == '__main__':
    unittest.main()
