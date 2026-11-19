"""Render Markdown with native Jinja includes and marketplace link rules."""

import posixpath
from pathlib import Path
import sys

from marketplace.source import SourceInventory

from ._editing_context import source_frontmatter
from ._links import rebase_links
from ._placeholders import reject_legacy_includes

# The publication builder starts with -S; never depend on site packages.
_vendor = str(Path(__file__).resolve().parents[3] / '_vendor')
sys.path.insert(0, _vendor)
try:
    from jinja2 import BaseLoader, StrictUndefined, TemplateError, TemplateNotFound, nodes
    from jinja2.sandbox import ImmutableSandboxedEnvironment
finally:
    sys.path.remove(_vendor)


class Environment(ImmutableSandboxedEnvironment):
    """Keep includes relative to their declaring document."""

    def join_path(self, template: str, parent: str) -> str:
        if template.startswith('/') or not template.endswith('.md') or '\\' in template:
            raise ValueError(f"{parent}: include must name a relative Markdown path: {template!r}")
        path = posixpath.normpath(posixpath.join(posixpath.dirname(parent), template))
        if path == '..' or path.startswith('../'):
            raise ValueError(f"{parent}: include leaves the marketplace source: {template!r}")
        return path


class Loader(BaseLoader):
    """Read and rebase static fragments in the context of one output."""

    def __init__(
        self, body: str, output: str, root: str | None, inventory: SourceInventory,
        published: frozenset[str] | None,
    ) -> None:
        self.body = body
        self.output = output
        self.root = root or '.'
        self.inventory = inventory
        self.published = published
        self.sources: dict[str, str] = {}

    def get_source(self, environment: Environment, template: str) -> tuple[str, str, None]:
        path = self.inventory.directory / template
        if template == self.output:
            return self.body, str(path), None
        if template in self.sources:
            return self.sources[template], str(path), None
        if not path.resolve().is_relative_to(self.inventory.directory.resolve()) or not path.is_file():
            raise TemplateNotFound(template)
        text = path.read_bytes().decode('utf-8', 'surrogateescape')
        header, text, templated = source_frontmatter(text, template)
        if header:
            raise ValueError(f"{template}: included fragments cannot set runtime frontmatter")
        reject_legacy_includes(text, template)

        def validate(target: str) -> None:
            candidate = self.inventory.directory / target
            exists = (target in self.published if self.published is not None else candidate.is_file())
            if (not target.startswith(self.root + '/') or not exists
                    or not candidate.resolve().is_relative_to(self.inventory.directory.resolve())):
                raise ValueError(f"{template}: link target {target!r} is not published in plugin {self.root!r}")

        external = self.root != '.' and not template.startswith(self.root + '/')
        text = rebase_links(text, template, self.output, validate if external else None)
        if not templated:
            # A literal can contain any delimiters, including an endraw tag.
            text = '{{ ' + repr(text) + ' }}'
        self.sources[template] = text
        return text, str(path), None


def compose(
    body: str, logical_path: str, host: str, inventory: SourceInventory,
    root: str | None, published: frozenset[str] | None,
) -> str:
    """Preflight literal includes in all branches, then let Jinja render them."""
    loader = Loader(body, logical_path, root, inventory, published)
    env = Environment(
        loader=loader, undefined=StrictUndefined, autoescape=False,
        trim_blocks=True, keep_trailing_newline=True,
        extensions=(),
    )
    # Do not expose Jinja's utility constructors in marketplace documents.
    env.globals.clear()
    checked: set[str] = set()

    def visit(name: str, chain: tuple[str, ...]) -> None:
        if name in chain:
            raise ValueError('Include cycle: ' + ' -> '.join((*chain, name)))
        if name in checked:
            return
        text, filename, _ = loader.get_source(env, name)
        ast = env.parse(text, name=name, filename=filename)
        for node in ast.find_all((nodes.Extends, nodes.Import, nodes.FromImport)):
            raise ValueError(f'{name}:{node.lineno}: use literal Markdown includes instead')
        for node in ast.find_all((nodes.Name, nodes.NSRef)):
            if node.name == 'build' and getattr(node, 'ctx', None) != 'load':
                raise ValueError(f'{name}:{node.lineno}: build is reserved')
        for node in ast.find_all(nodes.Macro):
            if node.name == 'build':
                raise ValueError(f'{name}:{node.lineno}: build is reserved')
        for node in ast.find_all(nodes.Include):
            if (node.ignore_missing or not node.with_context
                    or not isinstance(node.template, nodes.Const)
                    or not isinstance(node.template.value, str)):
                raise ValueError(f'{name}:{node.lineno}: expected a required literal include path with context')
            target = env.join_path(node.template.value, name)
            try:
                visit(target, (*chain, name))
            except TemplateNotFound as error:
                raise ValueError(f'{name}:{node.lineno}: missing include {target!r}') from error
        checked.add(name)

    try:
        visit(logical_path, ())
        return env.get_template(logical_path).render(build={'host': host})
    except TemplateError as error:
        location = getattr(error, 'name', None) or logical_path
        line = getattr(error, 'lineno', None)
        raise ValueError(f"{location}{f':{line}' if line else ''}: {error}") from error
