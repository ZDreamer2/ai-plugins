# zd-plugins

Standalone source marketplace containing `ai-doc` (documentation authoring and helpers) and `ai-marketplace` (multi-host marketplace authoring and build tools).

Extracted from bc-plugins commit `0a09ad40c6e8e2964cee4603c67f22aef0b3689e`, preserving tracked payloads and executable modes, without history, shared `@common` resources or installer payloads. The original plugins and their consumers are unchanged.

## Local build and validation

Run from this repository root. Requires Python 3.10+, Git and system timezone data including `Europe/Moscow` (for example, the OS `tzdata` package). PyYAML 6.0.2 is bundled; pip, site packages and the Bico SDK are unnecessary. Versions default to the latest touching Git commit timestamp, or the current time in a checkout without history. Build from a cache-free source tree: the builder copies local files, and `.gitignore` is not a packaging filter. Root `.gitlab-ci.yml`, `.gitlab/` and `.github/` are source-only and excluded from distributions. Some test subprocesses create Python caches despite the outer `-B`; remove those before building.

```sh
out=$(mktemp -d /tmp/zd-plugins-build.XXXXXX)
python3 -B -S ai-marketplace/scripts/build.py --dir . --output-dir "$out"
python3 -B -S ai-marketplace/scripts/validate_pi.py --dir . --tree "$out/pi" --output-dir "$out"
# Inspect $out/{claude,codex,pi} and $out/{codex,pi}-report.md before cleanup.
rm -rf -- "$out"
```

Claude and Codex catalogs use `zd-plugins` with ZDreamer2 identity; Pi packages are `@zdreamer2/pi-plugin-ai-doc` and `@zdreamer2/pi-plugin-ai-marketplace`. Each distribution contains exactly these two plugins. Reports identify literal host constructs, not host acceptance failures. See [host rendering](ai-marketplace/docs/HostRendering.md) and [authoring syntax](ai-marketplace/docs/AuthoringSyntax.md).

## Unit tests

The marketplace package suite includes focused standalone extraction checks. All tests use the standard library and the bundled parser. Logs may be redirected to a temporary directory outside this checkout.

```sh
scripts=ai-marketplace/scripts
python3 -B -S -m unittest discover -s "$scripts/tests" -v
for suite in marketplace/tests marketplace/source/tests marketplace/validation/tests marketplace/build/tests marketplace/build/rendering/tests; do
  python3 -B -S -m unittest discover -s "$scripts/$suite" -t "$scripts" -v || exit 1
done
python3 -B -S -m unittest discover -s ai-marketplace/codebase/tests -v
python3 -B -S -m unittest discover -s ai-doc/scripts/diff_doc/tests -t ai-doc/scripts -v
python3 -B -S -m unittest discover -s .gitlab/tests -v
```

## GitLab publication

The default-branch pipeline builds and validates the three distributions, then publishes each tree to its private GitLab repository:

- Claude: `git@g.bt.su:bico/generated/zd-plugins-claude.git`
- Codex: `git@g.bt.su:bico/generated/zd-plugins-codex.git`
- Pi: `git@g.bt.su:bico/generated/zd-plugins-pi.git`

Protected `master` jobs use runner 6 with tag `bc-plugins-publication`, shared with the trusted private bc-plugins marketplace. The projects share its execution account, not destination repositories or credentials. The pipeline requires Python 3.10+, Git, Bash, rsync and timezone data; no PHP, Docker or pip setup is needed.

Source project 48 holds masked, protected `CLAUDE_BUILD_REPO_TOKEN`, `CODEX_BUILD_REPO_TOKEN` and `PI_BUILD_REPO_TOKEN` variables. Each is a destination-project token with only `write_repository` scope and Maintainer access for protected-branch pushes. Tokens expire on 2027-10-23; renew them in their destination projects and replace the matching protected source variable before expiry. No token belongs in source or runner configuration.

The one-day pipeline artifact contains host trees, construct reports and source/builder revision files. Publication is serialized by `zd-plugins-publication`, rejects mismatched provenance or obsolete source heads, independently validates Pi, replaces destination contents while preserving executable modes, and makes no commit for unchanged trees. Destination commits record source and Python-builder revisions. Distribution repositories do not inherit source CI configuration.

`.gitlab/tests` exercises the actual build/publish scripts using disposable local bare remotes, without network credentials. Verify live publication against the exact source pipeline SHA and compare its artifacts with all three destination trees; a successful local test is not evidence of deployment.

GitHub source synchronization to `ZDreamer2/ai-plugins`, GitHub distribution builds, installed-host acceptance and consumer migration are not configured. GitHub distribution names remain undecided.

No project license has been selected. The vendored parser retains its [PyYAML provenance](ai-marketplace/scripts/marketplace/_vendor/PyYAML.provenance.md) and `PyYAML.LICENSE`. Local builds and tests do not establish installed-host acceptance or publication readiness.
