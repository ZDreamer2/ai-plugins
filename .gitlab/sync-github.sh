#!/usr/bin/env bash
# Synchronize only the trusted source branch, without force or unrelated refs.
set -euo pipefail
: "${CI_PROJECT_DIR:?}"
: "${CI_COMMIT_SHA:?}"
: "${CI_DEFAULT_BRANCH:?}"
test "$CI_DEFAULT_BRANCH" = master
test "${CI_COMMIT_BRANCH:-}" = "$CI_DEFAULT_BRANCH"
[[ "$CI_COMMIT_SHA" =~ ^[0-9a-f]{40}$ ]]
test "$(git -C "$CI_PROJECT_DIR" rev-parse HEAD)" = "$CI_COMMIT_SHA"
source "$CI_PROJECT_DIR/.github/ssh.sh"
source_head=$(git -C "$CI_PROJECT_DIR" ls-remote --exit-code origin "refs/heads/$CI_DEFAULT_BRANCH" | cut -f1)
test "$source_head" = "$CI_COMMIT_SHA" || {
  echo 'Refusing obsolete source synchronization' >&2; exit 1;
}
git -C "$CI_PROJECT_DIR" push --quiet git@github.com:ZDreamer2/ai-plugins.git "$CI_COMMIT_SHA:refs/heads/master"
echo "Synchronized source $CI_COMMIT_SHA to GitHub"
