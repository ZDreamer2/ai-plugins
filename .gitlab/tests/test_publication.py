"""Exercise the actual CI build and publisher with disposable local Git remotes."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ai-marketplace/scripts"))

from marketplace import parse_yaml


class PublicationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="zd-plugins-ci-test-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.source = self.base / "source"
        shutil.copytree(
            ROOT, self.source,
            ignore=shutil.ignore_patterns(".git", "@build", "__pycache__", "*.pyc"),
        )
        self.git("init", "--quiet", "--initial-branch=master", cwd=self.source)
        self.git("config", "user.name", "CI test", cwd=self.source)
        self.git("config", "user.email", "test@example.invalid", cwd=self.source)
        self.git("add", "-A", cwd=self.source)
        self.git("commit", "--quiet", "-m", "Source fixture", cwd=self.source)
        self.source_remote = self.base / "source.git"
        self.git("init", "--bare", "--quiet", str(self.source_remote))
        self.git("remote", "add", "origin", str(self.source_remote), cwd=self.source)
        self.git("push", "--quiet", "origin", "HEAD:master", cwd=self.source)
        self.sha = self.git("rev-parse", "HEAD", cwd=self.source).stdout.strip()
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        self.env.update(
            CI_PROJECT_DIR=str(self.source), CI_COMMIT_SHA=self.sha,
            CI_DEFAULT_BRANCH="master", MARKETPLACE_PYTHON=sys.executable,
            PUBLICATION_TOKEN="local-fixture-not-a-credential",
        )
        self.config = parse_yaml((self.source / ".gitlab-ci.yml").read_text())
        build = subprocess.run(
            ["bash", "-euo", "pipefail", "-c",
             "\n".join(self.config["build-distributions"]["script"])],
            cwd=self.source, env=self.env, capture_output=True, text=True,
        )
        self.assertEqual(build.returncode, 0, build.stdout + build.stderr)

    def git(self, *arguments: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *arguments], cwd=cwd, check=True, capture_output=True, text=True,
        )

    def destination(self, host: str) -> Path:
        target = self.base / (host + ".git")
        self.git("init", "--bare", "--quiet", str(target))
        return target

    def publish(self, host: str, target: Path, **overrides: str) -> subprocess.CompletedProcess:
        environment = dict(self.env, AGENT_TREE=host, TARGET_REMOTE=str(target))
        environment.update(overrides)
        return subprocess.run(
            ["bash", ".gitlab/publish.sh"], cwd=self.source, env=environment,
            capture_output=True, text=True,
        )

    def test_pipeline_routes_only_default_branch_to_locked_runner_tag(self) -> None:
        self.assertEqual(self.config["default"]["tags"], ["bc-plugins-publication"])
        self.assertEqual(self.config["workflow"]["rules"], [
            {"if": "$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH"}, {"when": "never"},
        ])
        template = self.config[".publish-template"]
        self.assertEqual(template["resource_group"], "zd-plugins-publication")
        self.assertEqual(template["needs"], [{"job": "build-distributions", "artifacts": True}])
        self.assertEqual(self.config["variables"]["GIT_DEPTH"], "0")
        for host in ("claude", "codex", "pi"):
            job = self.config["publish-" + host]
            self.assertEqual(job["extends"], ".publish-template")
            variables = job["variables"]
            self.assertEqual(variables["AGENT_TREE"], host)
            self.assertTrue(variables["TARGET_REMOTE"].endswith(
                "@g.bt.su/bico/generated/zd-plugins-" + host + ".git",
            ))
            self.assertEqual(variables["PUBLICATION_TOKEN"], "$" + host.upper() + "_BUILD_REPO_TOKEN")

    def test_empty_targets_modes_noop_and_source_only_ci(self) -> None:
        for host in ("claude", "codex", "pi"):
            with self.subTest(host=host):
                target = self.destination(host)
                result = self.publish(host, target)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                first = self.git("--git-dir", str(target), "rev-parse", "master").stdout
                result = self.publish(host, target)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("No changes to publish", result.stdout)
                self.assertEqual(self.git("--git-dir", str(target), "rev-parse", "master").stdout, first)
                paths = self.git("--git-dir", str(target), "ls-tree", "-r", "master").stdout
                self.assertIn("100755 blob", paths)
                self.assertIn("ai-doc/scripts/find-doc.py", paths)
                self.assertNotIn("\t.gitlab", paths)
                self.assertNotIn("\t.github", paths)
                message = self.git("--git-dir", str(target), "log", "-1", "--format=%s", "master").stdout
                self.assertIn(self.sha, message)

    def test_publication_replaces_existing_destination_tree(self) -> None:
        target = self.destination("claude")
        checkout = self.base / "destination-checkout"
        self.git("clone", "--quiet", str(target), str(checkout))
        self.git("config", "user.name", "CI test", cwd=checkout)
        self.git("config", "user.email", "test@example.invalid", cwd=checkout)
        (checkout / "obsolete.txt").write_text("old distribution\n")
        self.git("add", "-A", cwd=checkout)
        self.git("commit", "--quiet", "-m", "Old distribution", cwd=checkout)
        self.git("push", "--quiet", "origin", "HEAD:master", cwd=checkout)
        result = self.publish("claude", target)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        paths = self.git("--git-dir", str(target), "ls-tree", "-r", "--name-only", "master").stdout
        self.assertNotIn("obsolete.txt", paths)
        self.assertIn("ai-doc/scripts/find-doc.py", paths)

    def test_missing_token_and_wrong_provenance_leave_target_empty(self) -> None:
        target = self.destination("claude")
        result = self.publish("claude", target, PUBLICATION_TOKEN="")
        self.assertNotEqual(result.returncode, 0)
        (self.source / "@build/source-revision").write_text("0" * 40)
        result = self.publish("claude", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("--git-dir", str(target), "rev-list", "--all", "--count").stdout.strip(), "0")

    def test_older_pipeline_cannot_publish_after_source_advances(self) -> None:
        target = self.destination("codex")
        newer = self.base / "newer"
        self.git("clone", "--quiet", "--branch", "master", str(self.source_remote), str(newer))
        self.git("config", "user.name", "CI test", cwd=newer)
        self.git("config", "user.email", "test@example.invalid", cwd=newer)
        self.git("commit", "--allow-empty", "--quiet", "-m", "Newer source", cwd=newer)
        self.git("push", "--quiet", "origin", "master", cwd=newer)
        result = self.publish("codex", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing obsolete publication", result.stderr)
        self.assertEqual(self.git("--git-dir", str(target), "rev-list", "--all", "--count").stdout.strip(), "0")

    def test_corrupt_pi_resource_and_leaked_ci_are_rejected(self) -> None:
        target = self.destination("pi")
        (self.source / "@build/pi/ai-doc/scripts/find-doc.py").write_text("corrupt\n")
        result = self.publish("pi", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("--git-dir", str(target), "rev-list", "--all", "--count").stdout.strip(), "0")
        target = self.destination("claude")
        (self.source / "@build/claude/.gitlab-ci.yml").write_text("must not ship\n")
        result = self.publish("claude", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Source CI configuration must not be published", result.stderr)


if __name__ == "__main__":
    unittest.main()
