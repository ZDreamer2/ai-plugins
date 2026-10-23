#!/usr/bin/env bash
# Publish the same-pipeline tree to one private GitLab distribution repository.
set -euo pipefail

: "${CI_PROJECT_DIR:?CI_PROJECT_DIR is required}"
: "${CI_COMMIT_SHA:?CI_COMMIT_SHA is required}"
: "${CI_DEFAULT_BRANCH:?CI_DEFAULT_BRANCH is required}"
: "${PUBLICATION_TOKEN:?A destination-scoped publication token is required}"
: "${TARGET_REMOTE:?TARGET_REMOTE is required}"
: "${AGENT_TREE:?AGENT_TREE is required}"
MARKETPLACE_PYTHON=${MARKETPLACE_PYTHON:-python3}

case "$AGENT_TREE" in
  claude|codex|pi) ;;
  *) echo 'Unknown distribution tree' >&2; exit 1 ;;
esac
[[ "$CI_COMMIT_SHA" =~ ^[0-9a-f]{40}([0-9a-f]{24})?$ ]] || {
  echo 'Invalid source revision' >&2; exit 1;
}

artifact="$CI_PROJECT_DIR/@build"
tree="$artifact/$AGENT_TREE"
test -d "$tree"
test "$(< "$artifact/source-revision")" = "$CI_COMMIT_SHA"
test "$(< "$artifact/builder-revision")" = "$CI_COMMIT_SHA"
test "$(< "$artifact/builder-kind")" = python
test "$(git -C "$CI_PROJECT_DIR" rev-parse HEAD)" = "$CI_COMMIT_SHA"
for name in .gitlab-ci.yml .gitlab .github; do
  test ! -e "$tree/$name" || {
    echo 'Source CI configuration must not be published' >&2; exit 1;
  }
done

# GitLab holds the shared resource-group lock for this entire job.
require_current_source() {
  local source_head
  source_head=$(git -C "$CI_PROJECT_DIR" ls-remote --exit-code origin "refs/heads/$CI_DEFAULT_BRANCH" | cut -f1)
  test "$source_head" = "$CI_COMMIT_SHA" || {
    echo 'Refusing obsolete publication: source default branch has advanced' >&2
    exit 1
  }
}
require_current_source

if [ "$AGENT_TREE" = pi ]; then
  "$MARKETPLACE_PYTHON" -B -S -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'
  "$MARKETPLACE_PYTHON" -B -S "$CI_PROJECT_DIR/ai-marketplace/scripts/validate_pi.py" \
    --dir "$CI_PROJECT_DIR" --tree "$tree"
fi

work=$(mktemp -d "${TMPDIR:-/tmp}/zd-plugins-publish.XXXXXX")
trap 'rm -rf -- "$work"' EXIT
git clone --quiet "$TARGET_REMOTE" "$work/repository"
rsync -a --delete --exclude='/.git/' "$tree/" "$work/repository/"
git -C "$work/repository" config user.name 'zd-plugins CI'
git -C "$work/repository" config user.email 'ci@zd-plugins.invalid'
git -C "$work/repository" add -A
if git -C "$work/repository" diff --cached --quiet; then
  echo "No changes to publish for $AGENT_TREE"
  exit 0
fi
git -C "$work/repository" commit --quiet \
  -m "Publish $AGENT_TREE from source $CI_COMMIT_SHA; python builder $CI_COMMIT_SHA"
require_current_source
git -C "$work/repository" push --quiet origin HEAD:master
echo "Published $AGENT_TREE from $CI_COMMIT_SHA"
