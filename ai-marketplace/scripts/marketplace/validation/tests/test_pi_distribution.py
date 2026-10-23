"""Independently author Pi artifacts and damage one gate property at a time."""

import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from marketplace.validation import validate_pi_distribution


class PiDistributionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.source = self.folder / 'source'
        self.tree = self.folder / 'downloaded'
        self.source.mkdir()
        self.tree.mkdir()
        self.roots = ('main', 'group/fallback')
        self.skills = ['./skills/alpha', './skills/zulu']
        self.extensions = [
            './extensions/alpha/index.ts', './extensions/beta/index.mjs',
            './extensions/gamma/index.js',
        ]
        self._write(self.source / '@common/docs/Shared.md', b'Authored shared docs\n')
        self._write(self.source / '@common/config.bin', b'\xff\x00shared bytes')
        for root in self.roots:
            source = self.source / root
            package = self.tree / root
            manifest = (
                'name: main\n' if root == 'main' else 'name: null\n'
            ) + 'description: Example\nversion: 999.0\n'
            self._write(source / 'ai-plugin.yml', manifest.encode())
            payloads = {
                'skills/zulu/SKILL.md': b'Authored zulu instructions\n',
                'skills/alpha/SKILL.md': b'Authored alpha instructions\n',
                '.hidden/resource': b'Hidden resources remain required\n',
                '.settings': b'{"local":true}',
                'scripts/run.py': b'raise RuntimeError("must never execute")\n',
                'docs/Guide.md': b'Authored ordinary markdown\n',
                'docs/Guide.MD': b'Uppercase extension stays byte-identical\n',
                'data.bin': b'\x00\xff\xfe',
                'extensions/gamma/index.js': b'export default () => {};\n',
                'extensions/beta/index.mjs': b'export default () => {};\n',
                'extensions/alpha/index.ts': b'export default () => {};\n',
            }
            for relative, content in payloads.items():
                self._write(source / relative, content)
                self._write(package / relative, content)
            (source / 'scripts/run.py').chmod(0o755)
            (package / 'scripts/run.py').chmod(0o755)
            (source / '@common').symlink_to(self.source / '@common', target_is_directory=True)
            self._write(package / '@common/docs/Shared.md', b'Rendered shared docs\n')
            self._write(package / '@common/config.bin', b'\xff\x00shared bytes')
            # The artifact gate does not parse skill frontmatter or compare Markdown.
            self._write(package / 'skills/alpha/SKILL.md', b'Changed nonempty instructions')
            metadata = {
                'name': '@zdreamer2/pi-plugin-' + source.name, 'version': '42.0',
                'description': 'Example', 'unrelated': {'allowed': True},
                'pi': {'skills': self.skills, 'extensions': self.extensions},
            }
            self._json(package / 'package.json', metadata)
            self._json(package / '.pi-plugin/plugin.json', {
                'name': source.name, 'version': '42.0',
            })

    @staticmethod
    def _write(path: Path, content: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def _json(self, path: Path, value: object) -> None:
        self._write(path, json.dumps(value, ensure_ascii=False).encode())

    def _change_package(self, transform) -> None:
        path = self.tree / 'main/package.json'
        metadata = json.loads(path.read_bytes())
        transform(metadata)
        self._json(path, metadata)

    def _snapshot(self) -> dict:
        result = {}
        for current, directories, files in os.walk(self.folder, followlinks=False):
            for name in directories + files:
                path = Path(current) / name
                mode = stat.S_IMODE(path.lstat().st_mode)
                value = (
                    ('link', os.readlink(path)) if path.is_symlink()
                    else ('directory',) if path.is_dir()
                    else ('file', path.read_bytes())
                )
                result[path.relative_to(self.folder).as_posix()] = (mode, value)
        return result

    def _validate(self, output: Path | str | None = None) -> int:
        return validate_pi_distribution(self.source, self.tree, output)

    def _assert_rejected(self, pattern: str = '.', output=None) -> None:
        before = self._snapshot()
        with self.assertRaisesRegex(ValueError, pattern):
            self._validate(output)
        self.assertEqual(before, self._snapshot())

    def test_multiple_grouped_packages_are_read_only_and_independent(self) -> None:
        before = self._snapshot()
        with patch('subprocess.run', side_effect=AssertionError('no Git or scripts')):
            self.assertEqual(2, self._validate())
        self.assertEqual(before, self._snapshot())
        self.assertFalse((self.source / '@build').exists())

    def test_name_missing_has_the_same_directory_fallback_as_null(self) -> None:
        path = self.source / 'group/fallback/ai-plugin.yml'
        path.write_text('description: Example\n', encoding='utf-8')
        self.assertEqual(2, self._validate())

    def test_scalar_names_preserve_php_package_concatenation_and_identity(self) -> None:
        for yaml_name, identity, suffix in (
            ('true', True, '1'), ('false', False, ''), ('7', 7, '7'),
            ('1.0', 1.0, '1'), ('-0.0', -0.0, '-0'),
            ('1.0e20', 1e20, '1.0E+20'), ('1.0e-9', 1e-9, '1.0E-9'),
        ):
            with self.subTest(name=yaml_name):
                (self.source / 'main/ai-plugin.yml').write_text(
                    'name: ' + yaml_name + '\ndescription: Example\n')
                self._change_package(lambda data: data.update(
                    name='@zdreamer2/pi-plugin-' + suffix))
                self._json(self.tree / 'main/.pi-plugin/plugin.json', {
                    'name': identity, 'version': '42.0',
                })
                self.assertEqual(2, self._validate())

    def test_corruption_matrix(self) -> None:
        pristine = self.folder / 'pristine-artifact'
        shutil.copytree(self.tree, pristine)
        defects = {
            'missing package': lambda: (self.tree / 'main/package.json').unlink(),
            'extra package': lambda: self._json(self.tree / 'extra/package.json', {}),
            'malformed package': lambda: self._write(self.tree / 'main/package.json', b'{'),
            'wrong name': lambda: self._change_package(lambda data: data.update(name='wrong')),
            'wrong description': lambda: self._change_package(lambda data: data.update(description='wrong')),
            'wrong version type': lambda: self._change_package(lambda data: data.update(version=42)),
            'empty version': lambda: self._change_package(lambda data: data.update(version='')),
            'missing version': lambda: self._change_package(lambda data: data.pop('version')),
            'script mismatch': lambda: self._json(self.tree / 'main/.pi-plugin/plugin.json', {'name': 'main', 'version': 'stale'}),
            'missing script identity': lambda: (self.tree / 'main/.pi-plugin/plugin.json').unlink(),
            'extra identity': lambda: self._json(self.tree / 'main/.pi-plugin/plugin.json', {'name': 'main', 'version': '42.0', 'extra': True}),
            'reordered identity': lambda: self._json(self.tree / 'main/.pi-plugin/plugin.json', {'version': '42.0', 'name': 'main'}),
            'missing skills': lambda: self._change_package(lambda data: data['pi'].update(skills=[])),
            'reordered skills': lambda: self._change_package(lambda data: data['pi'].update(skills=self.skills[::-1])),
            'reordered pi keys': lambda: self._change_package(lambda data: data.update(pi={'extensions': self.extensions, 'skills': self.skills})),
            'malformed pi': lambda: self._change_package(lambda data: data.update(pi=[])),
            'extra pi field': lambda: self._change_package(lambda data: data['pi'].update(extra=[])),
            'wrong skills type': lambda: self._change_package(lambda data: data['pi'].update(skills=True)),
            'reordered extensions': lambda: self._change_package(lambda data: data['pi'].update(extensions=self.extensions[::-1])),
            'missing skill': lambda: (self.tree / 'main/skills/alpha/SKILL.md').unlink(),
            'empty skill': lambda: (self.tree / 'main/skills/alpha/SKILL.md').write_bytes(b''),
            'missing extension': lambda: (self.tree / 'main/extensions/alpha/index.ts').unlink(),
            'missing shared': lambda: (self.tree / 'main/@common/config.bin').unlink(),
            'missing hidden': lambda: (self.tree / 'main/.hidden/resource').unlink(),
            'lost executable': lambda: (self.tree / 'main/scripts/run.py').chmod(0o644),
            'stale script': lambda: (self.tree / 'main/scripts/run.py').write_bytes(b'old'),
            'stale uppercase Markdown': lambda: (self.tree / 'main/docs/Guide.MD').write_bytes(b'changed'),
            'stale binary': lambda: (self.tree / 'main/data.bin').write_bytes(b'changed'),
            'source manifest': lambda: self._write(self.tree / 'main/ai-plugin.yml', b'name: main'),
            'hidden source manifest': lambda: self._write(self.tree / 'main/.hidden/ai-plugin.yml', b'name: hidden'),
        }
        for name, damage in defects.items():
            with self.subTest(defect=name):
                damage()
                self._assert_rejected()
                # Restore this test's known artifact; do not use the builder.
                shutil.rmtree(self.tree)
                shutil.copytree(pristine, self.tree)

    def test_forbidden_root_content_and_artifact_links(self) -> None:
        for name in ('package.json', '@common', 'pi-report.md', 'codex-report.md',
                     '.claude-plugin', '.agents', '@setup'):
            with self.subTest(path=name):
                path = self.tree / name
                self._write(path, b'forbidden')
                self._assert_rejected('must not be published')
                path.unlink()
        for target in (self.source / 'main/data.bin', self.source / 'main',
                       self.source / 'missing'):
            with self.subTest(target=target):
                link = self.tree / 'main/link'
                link.symlink_to(target)
                self._assert_rejected("materialize symlink 'main/link'")
                link.unlink()

    def test_malformed_metadata_never_accepts_python_json_extensions(self) -> None:
        path = self.tree / 'main/package.json'
        original = path.read_bytes()
        for content in (b'null', b'"scalar"', b'true', b'42', b'[]'):
            with self.subTest(content=content):
                path.write_bytes(content)
                self._assert_rejected('Pi metadata|package identity')
                path.write_bytes(original)
        for field in (b'"x":NaN', b'"x":Infinity', b'"x":-Infinity',
                      b'"x":"\xff"', b'"x":"\\ud800"',
                      b'"\\udfff":null', b'"x":"\\ud800","x":0',
                      b'"\\ud800":0,"\\ud800":1'):
            with self.subTest(field=field):
                path.write_bytes(original[:-1] + b',' + field + b'}')
                self._assert_rejected('Could not read Pi metadata')
                path.write_bytes(original)
        # A valid surrogate pair is decoded by both PHP and Python, including
        # in unrelated fields that the gate deliberately does not constrain.
        path.write_bytes(original[:-1] + b',"emoji":"\\ud83d\\ude00"}')
        self.assertEqual(2, self._validate())

    def test_json_associative_arrays_keep_php_strict_types_and_order(self) -> None:
        manifest = self.source / 'main/ai-plugin.yml'
        for source_value, artifact_value, accepted in (
            ('{first: 1, second: 2}', {'first': 1, 'second': 2}, True),
            ('{first: 1, second: 2}', {'second': 2, 'first': 1}, False),
            ('[a, b]', {'0': 'a', '1': 'b'}, True),
            ('{}', [], True), ('[]', {}, True),
            ('true', 1, False), ('1', True, False), ('1', 1.0, False),
            ('1.0', 1, False), ('1.0', 1.0, True),
            ('9223372036854775808', 9223372036854775808, False),
            ('9223372036854775808.0', 9223372036854775808, True),
            ('!!binary RXhhbXBsZQ==', 'Example', True),
            ('!!binary /w==', '\ufffd', False),
        ):
            with self.subTest(source=source_value, artifact=artifact_value):
                manifest.write_text('name: main\ndescription: ' + source_value + '\n')
                self._change_package(lambda data: data.update(description=artifact_value))
                if accepted:
                    self.assertEqual(2, self._validate())
                else:
                    self._assert_rejected('description')

    def test_numeric_index_objects_are_php_entry_point_lists(self) -> None:
        self._change_package(lambda data: data['pi'].update(
            skills={str(index): value for index, value in enumerate(self.skills)}))
        self.assertEqual(2, self._validate())

    def test_plugins_without_extensions_omit_the_declaration(self) -> None:
        shutil.rmtree(self.source / 'main/extensions')
        shutil.rmtree(self.tree / 'main/extensions')
        self._change_package(lambda data: data['pi'].pop('extensions'))
        self.assertEqual(2, self._validate())
        self._change_package(lambda data: data['pi'].update(extensions=[]))
        self._assert_rejected('entry points')

    def test_hidden_and_vcs_traversal_rules_are_distinct(self) -> None:
        self._json(self.tree / '.hidden/package.json', {})
        self._write(self.source / '.hidden-plugin/ai-plugin.yml', b'description: ignored')
        self._write(self.source / 'main/.git/ignored', b'not required')
        self._write(self.tree / 'main/.git/ai-plugin.yml', b'not inspected')
        (self.tree / 'main/.git/link').symlink_to('missing')
        # Source manifest files are excluded independently of ordinary resource
        # reads; a dangling nested source manifest is not a bundled resource.
        dangling = self.source / 'main/nested/ai-plugin.yml'
        dangling.parent.mkdir()
        dangling.symlink_to('missing')
        self.assertEqual(2, self._validate())
        self._write(self.tree / '.hidden/ai-plugin.yml', b'forbidden')
        self._assert_rejected('Source manifests')

    def test_missing_empty_and_root_manifest_inputs(self) -> None:
        for source, tree in ((self.folder / 'missing', self.tree),
                             (self.source, self.folder / 'missing')):
            with self.subTest(source=source, tree=tree):
                with self.assertRaisesRegex(ValueError, 'missing'):
                    validate_pi_distribution(source, tree)
        file = self.folder / 'file'
        file.touch()
        with self.assertRaisesRegex(ValueError, 'directory'):
            validate_pi_distribution(file, self.tree)
        with self.assertRaisesRegex(ValueError, 'directory'):
            validate_pi_distribution(self.source, file)
        empty = self.folder / 'empty'
        empty.mkdir()
        with self.assertRaisesRegex(ValueError, 'No source plugins'):
            validate_pi_distribution(empty, self.tree)
        self._write(self.source / 'ai-plugin.yml', b'description: root')
        self._assert_rejected('marketplace root')

    def test_default_and_nested_custom_outputs_exclude_resources_and_aliases(self) -> None:
        for relative, default in (('@build', True), ('main/generated', False),
                                  ('main/skills/generated', False),
                                  ('main/extensions/generated', False)):
            with self.subTest(output=relative):
                output = self.source / relative
                self._write(output / 'ai-plugin.yml', b'description: output')
                self._write(output / 'SKILL.md', b'generated skill')
                self._write(output / 'index.ts', b'generated extension')
                self._write(output / 'nested/output.bin', b'generated content')
                directory_alias = self.source / 'main/generated-alias'
                file_alias = self.source / 'main/output-alias.bin'
                manifest_alias = self.source / 'ghost/ai-plugin.yml'
                manifest_alias.parent.mkdir(exist_ok=True)
                manifest_alias.symlink_to(output / 'ai-plugin.yml')
                directory_alias.symlink_to(output, target_is_directory=True)
                file_alias.symlink_to(output / 'nested/output.bin')
                before = self._snapshot()
                self.assertEqual(2, self._validate(None if default else output))
                self.assertEqual(before, self._snapshot())
                directory_alias.unlink()
                file_alias.unlink()
                manifest_alias.unlink()
                shutil.rmtree(output)

    def test_output_path_canonical_alias_and_working_directory_resolution(self) -> None:
        output = self.source / 'main/generated'
        self._write(output / 'ai-plugin.yml', b'description: generated')
        self._write(output / 'input.bin', b'excluded')
        alias = self.folder / 'output-alias'
        alias.symlink_to(output, target_is_directory=True)
        self.assertEqual(2, self._validate(alias))
        previous = Path.cwd()
        try:
            os.chdir(self.folder)
            self.assertEqual(2, self._validate('source/main/generated'))
        finally:
            os.chdir(previous)

    def test_external_outputs_and_ancestors_do_not_exclude_source(self) -> None:
        for output in (self.folder / 'external', self.folder):
            with self.subTest(output=output):
                self.assertEqual(2, self._validate(output))
                path = self.tree / 'main/data.bin'
                original = path.read_bytes()
                path.unlink()
                self._assert_rejected('main/data.bin', output)
                path.write_bytes(original)

    def test_relocated_tree_is_inspected_outside_selected_output(self) -> None:
        generated = self.source / '@build'
        self._write(generated / 'pi/stale/package.json', b'{}')
        self.assertEqual(2, self._validate())
        (self.tree / 'main/data.bin').write_bytes(b'damage downloaded artifact')
        self._assert_rejected('main/data.bin')

    def test_source_directory_cycles_and_dangling_links_fail_contextually(self) -> None:
        code = '''
import sys
sys.path.insert(0, sys.argv[1])
from marketplace.validation import validate_pi_distribution
try:
    validate_pi_distribution(sys.argv[2], sys.argv[3])
except ValueError as error:
    assert 'main/cycle' in str(error), str(error)
else:
    raise AssertionError('Cycle or dangling link accepted')
'''
        scripts = Path(__file__).resolve().parents[3]
        for target in (self.source / 'main', self.source, self.source / 'missing'):
            with self.subTest(target=target):
                link = self.source / 'main/cycle'
                link.symlink_to(target, target_is_directory=True)
                before = self._snapshot()
                result = subprocess.run([
                    sys.executable, '-B', '-S', '-c', code, str(scripts),
                    str(self.source), str(self.tree),
                ], capture_output=True, text=True, cwd=self.folder, timeout=10)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(before, self._snapshot())
                link.unlink()

    def test_filesystem_errors_keep_real_inventory_and_logical_paths(self) -> None:
        original_read = Path.read_bytes
        original_iterdir = Path.iterdir
        failures = (
            ('metadata read', self.tree / 'main/package.json', 'read_bytes'),
            ('source read', self.source / 'main/@common/config.bin', 'read_bytes'),
            ('artifact read', self.tree / 'main/data.bin', 'read_bytes'),
            ('source enumerate', self.source / 'main/.hidden', 'iterdir'),
        )
        for name, failing, operation in failures:
            def read(path):
                if path == failing:
                    raise PermissionError('injected unreadable operation')
                return original_read(path)

            def enumerate_directory(path):
                if path == failing:
                    raise PermissionError('injected enumeration failure')
                return original_iterdir(path)

            with self.subTest(failure=name):
                before = self._snapshot()
                with patch.object(Path, operation, read if operation == 'read_bytes' else enumerate_directory):
                    with self.assertRaisesRegex(ValueError, str(failing)):
                        self._validate()
                self.assertEqual(before, self._snapshot())

    def test_import_is_lazy_and_validation_does_not_import_build(self) -> None:
        code = '''
import sys
sys.path.insert(0, sys.argv[1])
from marketplace.validation import check_syntax, validate_pi_distribution
assert not any(name.startswith(('marketplace.source', 'marketplace._yaml',
                                'marketplace._vendor', 'marketplace.build'))
               or name == 'subprocess' for name in sys.modules)
assert validate_pi_distribution(sys.argv[2], sys.argv[3]) == 2
assert not any(name.startswith('marketplace.build') for name in sys.modules)
'''
        scripts = Path(__file__).resolve().parents[3]
        before = self._snapshot()
        result = subprocess.run([
            sys.executable, '-B', '-S', '-c', code, str(scripts),
            str(self.source), str(self.tree),
        ], capture_output=True, text=True, cwd=self.folder, timeout=10)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual('', result.stdout)
        self.assertEqual('', result.stderr)
        self.assertEqual(before, self._snapshot())


if __name__ == '__main__':
    unittest.main()
