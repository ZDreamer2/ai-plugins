#!/usr/bin/env bash
# Adapt GitHub Actions to the shared, tested publication contract.
set -euo pipefail
: "${GITHUB_WORKSPACE:?}"
: "${GITHUB_SHA:?}"
: "${AGENT_TREE:?}"
test "${GITHUB_REPOSITORY:-}" = ZDreamer2/ai-plugins
test "${GITHUB_REF:-}" = refs/heads/master
case "$AGENT_TREE" in
  claude|codex|pi) ;;
  *) echo 'Unknown distribution tree' >&2; exit 1 ;;
esac
source "$GITHUB_WORKSPACE/.github/ssh.sh"
export CI_PROJECT_DIR="$GITHUB_WORKSPACE" CI_COMMIT_SHA="$GITHUB_SHA" CI_DEFAULT_BRANCH=master
export TARGET_REMOTE="git@github.com:ZDreamer2/ai-plugins-$AGENT_TREE.git"
# The shared helper requires a credential; here it is an SSH key, not a PAT.
export PUBLICATION_TOKEN="$SSH_PRIVATE_KEY_B64"
bash "$GITHUB_WORKSPACE/.gitlab/publish.sh"
