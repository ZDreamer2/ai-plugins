#!/usr/bin/env bash
# Publish a same-run tree. External marketplaces pass the tooling directory
# carried in their build artifact; ZD and its GitHub mirror use their checkout.
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
builder_revision=$(< "$artifact/builder-revision")
[[ "$builder_revision" =~ ^[0-9a-f]{40}([0-9a-f]{24})?$ ]] || {
  echo 'Invalid artifact builder revision' >&2; exit 1;
}
tooling_dir=${1:-$CI_PROJECT_DIR}
if [ "$tooling_dir" = "$CI_PROJECT_DIR" ]; then
  test "$builder_revision" = "$CI_COMMIT_SHA"
else
  test "$builder_revision" = "$(< "$tooling_dir/revision")"
fi
test "$(< "$artifact/builder-kind")" = python
test "$(git -C "$CI_PROJECT_DIR" rev-parse HEAD)" = "$CI_COMMIT_SHA"
for name in .gitlab-ci.yml .gitlab .github; do
  test ! -e "$tree/$name" || {
    echo 'Source CI configuration must not be published' >&2; exit 1;
  }
done

# The caller holds its platform's publication lock for this entire invocation.
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
  "$MARKETPLACE_PYTHON" -B -S "$tooling_dir/ai-marketplace/scripts/validate_pi.py" \
    --dir "$CI_PROJECT_DIR" --tree "$tree"
fi

work=$(mktemp -d "${TMPDIR:-/tmp}/marketplace-publish.XXXXXX")
trap 'rm -rf -- "$work"' EXIT
git clone --quiet "$TARGET_REMOTE" "$work/repository"
rsync -a --delete --exclude='/.git/' "$tree/" "$work/repository/"
git -C "$work/repository" config user.name "${PUBLICATION_AUTHOR_NAME:-zd-plugins CI}"
git -C "$work/repository" config user.email "${PUBLICATION_AUTHOR_EMAIL:-ci@zd-plugins.invalid}"
git -C "$work/repository" add -A
if git -C "$work/repository" diff --cached --quiet; then
  echo "No changes to publish for $AGENT_TREE"
  exit 0
fi
git -C "$work/repository" commit --quiet \
  -m "Publish $AGENT_TREE from source $CI_COMMIT_SHA; python builder $builder_revision"
require_current_source
git -C "$work/repository" push --quiet origin HEAD:master
echo "Published $AGENT_TREE from $CI_COMMIT_SHA"
