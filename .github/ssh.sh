#!/usr/bin/env bash
# Source from a short-lived CI shell; the key is base64-encoded for masked storage.
: "${SSH_PRIVATE_KEY_B64:?A repository-scoped deploy key is required}"
ssh_dir=$(mktemp -d "${TMPDIR:-/tmp}/zd-plugins-ssh.XXXXXX")
trap 'rm -rf -- "$ssh_dir"' EXIT
(umask 077; printf '%s' "$SSH_PRIVATE_KEY_B64" | base64 --decode > "$ssh_dir/key")
ssh-keygen -y -P '' -f "$ssh_dir/key" > /dev/null
ssh_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export GIT_SSH_COMMAND="ssh -F /dev/null -i '$ssh_dir/key' -o IdentitiesOnly=yes -o BatchMode=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile='$ssh_root/github_known_hosts' -o GlobalKnownHostsFile=/dev/null"
