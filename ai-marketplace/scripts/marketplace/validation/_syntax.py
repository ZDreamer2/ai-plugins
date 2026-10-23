"""Check source syntax using the established changed-file selection contract."""

import json
from pathlib import Path
from typing import TypedDict


class Change(TypedDict):
    repo: str
    path: str
    kind: str


class CheckGroup(TypedDict):
    root: str
    changes: list[Change]


class RanCheck(TypedDict):
    name: str
    repo: str
    path: str


class Finding(TypedDict):
    message: str
    repo: str
    path: str


class CheckResult(TypedDict):
    changed: list[Change]
    findings: list[Finding]
    ran: list[RanCheck]


def check_syntax(group: CheckGroup) -> CheckResult:
    root = Path(group['root']).resolve()
    result: CheckResult = {'changed': [], 'findings': [], 'ran': []}
    for change in group['changes']:
        if change['kind'] == 'deleted':
            continue
        path = root / change['path']
        # Symlinks are packaging inputs; do not follow them into another owner.
        if path.is_symlink() or not path.is_file():
            continue
        data = path.read_bytes()
        is_python = path.suffix == '.py' or (
            data.startswith(b'#!') and b'python' in data.split(b'\n', 1)[0]
        )
        if not is_python and path.suffix != '.json':
            continue
        name = 'Python syntax' if is_python else 'JSON syntax'
        result['ran'].append({
            'name': name, 'repo': change['repo'], 'path': change['path'],
        })
        try:
            if is_python:
                compile(data, str(path), 'exec')
            else:
                json.loads(data)
        except (SyntaxError, ValueError, UnicodeError) as error:
            result['findings'].append({
                'message': f'{name}: {error}',
                'repo': change['repo'], 'path': change['path'],
            })
    return result
