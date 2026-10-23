"""Exercise GitHub adapters against real local Git remotes without network access."""

import base64
from pathlib import Path
import subprocess
import tarfile

import test_publication
from marketplace import parse_yaml


class GitHubPublicationTests(test_publication.PublicationTests):
    def setUp(self) -> None:
        super().setUp()
        key = self.base / "deploy-key"
        subprocess.run(
            ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(key)],
            check=True, capture_output=True,
        )
        self.key = base64.b64encode(key.read_bytes()).decode()
        self.env.update(
            GITHUB_WORKSPACE=str(self.source), GITHUB_SHA=self.sha,
            GITHUB_REPOSITORY="ZDreamer2/ai-plugins", GITHUB_REF="refs/heads/master",
            SSH_PRIVATE_KEY_B64=self.key,
        )

    def publish(self, host: str, target: Path, **overrides: str) -> subprocess.CompletedProcess:
        environment = dict(
            self.env, AGENT_TREE=host, GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="url." + target.as_uri() + ".insteadOf",
            GIT_CONFIG_VALUE_0="git@github.com:ZDreamer2/ai-plugins-" + host + ".git",
        )
        if "PUBLICATION_TOKEN" in overrides:
            overrides["SSH_PRIVATE_KEY_B64"] = overrides.pop("PUBLICATION_TOKEN")
        environment.update(overrides)
        return subprocess.run(
            ["bash", ".github/publish.sh"], cwd=self.source, env=environment,
            capture_output=True, text=True,
        )

    def test_workflow_boundaries_and_secret_mapping(self) -> None:
        workflow = parse_yaml((self.source / ".github/workflows/publish.yml").read_text())
        # The bundled YAML 1.1 parser reads the unquoted Actions 'on' key as True.
        events = workflow.get("on", workflow.get(True))
        self.assertEqual(events["push"]["branches"], ["master"])
        self.assertEqual(set(events), {"push", "workflow_dispatch"})
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertEqual(workflow["concurrency"], {
            "group": "zd-plugins-publication", "cancel-in-progress": False,
        })
        job = workflow["jobs"]["publish"]
        self.assertEqual(job["if"],
                         "github.repository == 'ZDreamer2/ai-plugins' && github.ref == 'refs/heads/master'")
        steps = job["steps"]
        self.assertFalse(steps[0]["with"]["persist-credentials"])
        publications = [step for step in steps if step.get("run") == "bash .github/publish.sh"]
        self.assertEqual(len(publications), 3)
        for host, step in zip(("claude", "codex", "pi"), publications):
            self.assertEqual(step["env"], {
                "AGENT_TREE": host,
                "SSH_PRIVATE_KEY_B64": "${{ secrets." + host.upper() + "_DEPLOY_KEY_B64 }}",
            })
        sync = self.config["sync-github-source"]
        self.assertEqual(sync["stage"], "sync")
        self.assertEqual(sync["resource_group"], "zd-plugins-github-source")
        build = next(step for step in steps if step.get("name") == "Build and independently validate")
        result = subprocess.run(
            ["bash", "-euo", "pipefail", "-c", build["run"]], cwd=self.source,
            env=self.env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        with tarfile.open(self.source / "marketplace.tar") as archive:
            self.assertEqual(archive.extractfile("./source-revision").read().decode().strip(), self.sha)
            self.assertTrue(archive.getmember("./claude/ai-doc/scripts/find-doc.py").mode & 0o111)
            for host in ("claude", "codex", "pi"):
                self.assertEqual(archive.extractfile("./" + host + "/LICENSE").read(),
                                 (self.source / "LICENSE").read_bytes())
                self.assertIn("./" + host + "/ai-marketplace/scripts/marketplace/_vendor/PyYAML.LICENSE",
                              archive.getnames())

    def test_wrong_repository_ref_host_and_key_are_rejected(self) -> None:
        target = self.destination("claude")
        for override in (
            {"GITHUB_REPOSITORY": "someone/fork"},
            {"GITHUB_REF": "refs/heads/untrusted"},
            {"SSH_PRIVATE_KEY_B64": "not-a-key"},
        ):
            result = self.publish("claude", target, **override)
            self.assertNotEqual(result.returncode, 0)
        result = self.publish("unknown", target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("--git-dir", str(target), "rev-list", "--all", "--count").stdout.strip(), "0")

    def test_source_sync_only_default_branch_and_no_force(self) -> None:
        target = self.destination("github-source")
        environment = dict(
            self.env, CI_COMMIT_BRANCH="master", GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="url." + target.as_uri() + ".insteadOf",
            GIT_CONFIG_VALUE_0="git@github.com:ZDreamer2/ai-plugins.git",
        )

        def sync(**overrides: str) -> subprocess.CompletedProcess:
            return subprocess.run(
                ["bash", ".gitlab/sync-github.sh"], cwd=self.source,
                env=dict(environment, **overrides), capture_output=True, text=True,
            )

        result = sync(CI_COMMIT_BRANCH="feature")
        self.assertNotEqual(result.returncode, 0)
        self.git("tag", "private-tag", cwd=self.source)
        result = sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git("--git-dir", str(target), "rev-parse", "master").stdout.strip(), self.sha)
        self.assertEqual(self.git("--git-dir", str(target), "for-each-ref", "--format=%(refname)").stdout.strip(), "refs/heads/master")
        self.assertEqual(sync().returncode, 0)
        # A destination-only commit must never be silently overwritten.
        newer = self.base / "github-newer"
        self.git("clone", "--quiet", "--branch", "master", str(target), str(newer))
        self.git("config", "user.name", "CI test", cwd=newer)
        self.git("config", "user.email", "test@example.invalid", cwd=newer)
        self.git("commit", "--allow-empty", "--quiet", "-m", "Diverged", cwd=newer)
        self.git("push", "--quiet", "origin", "master", cwd=newer)
        self.assertNotEqual(sync().returncode, 0)
        # An obsolete GitLab job also cannot synchronize.
        self.git("commit", "--allow-empty", "--quiet", "-m", "Source advanced", cwd=self.source)
        self.git("push", "--quiet", "origin", "HEAD:master", cwd=self.source)
        self.git("checkout", "--quiet", self.sha, cwd=self.source)
        result = sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing obsolete source synchronization", result.stderr)
