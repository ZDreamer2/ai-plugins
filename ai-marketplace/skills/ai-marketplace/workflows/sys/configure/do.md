# Configure a marketplace repository

## Overview

Set up source hosting, automated builds and publication using the Python converter bundled with ai-marketplace.

### Input

- The source marketplace checkout and requested GitLab/GitHub delivery arrangement.
- Operator authorization and access for remote configuration and publication.

### Output

- Configured repositories and pipelines delivering the requested host distributions.
- Marketplace documentation with actual locations, installation instructions and credential-maintenance responsibilities.
- Verification results and any configuration still blocked or inactive.

## Workflow

### Step 1: Establish the repository layout

Identify the authoritative source, publishing branch, supported hosts, visibility and destination repositories. Clarify missing choices before creating remote resources or enabling publication; report missing access rather than substituting unrelated credentials.

Keep source synchronization separate from generated-tree publication. For example, GitLab can build its distributions while also synchronizing source to GitHub, where Actions builds separate distributions. Mirroring a Claude build to GitHub is not that source-and-build arrangement. Implement only the requested paths.

### Step 2: Build with the bundled converter

Resolve these paths from this document to absolute paths:

- `../../../../../scripts/build.py` -> `BUILD_SCRIPT`
- `../../../../../scripts/validate_pi.py` -> `PI_VALIDATOR`

Set `SOURCE` to the absolute source-marketplace directory. Run:

```sh
OUTPUT="$SOURCE/@build"
python3 -B -S "$BUILD_SCRIPT" --dir "$SOURCE" --output-dir "$OUTPUT"
python3 -B -S "$PI_VALIDATOR" --dir "$SOURCE" --tree "$OUTPUT/pi" --output-dir "$OUTPUT"
```

The converter discovers `ai-plugin.yml` manifests and produces:

| Output | Publication destination |
|---|---|
| `@build/claude/` | Claude distribution repository or selected distribution location |
| `@build/codex/` | Codex distribution repository or selected distribution location |
| `@build/pi/` | Pi distribution repository or selected distribution location |

Reports beside those trees are build evidence, not distribution payload. Check plugin inventory and generated identities before wiring publication. Marketplace/package names come from the renderer and validator, not automatically from the repository name; the CLI has no identity-override flags. Adapt those implementations together if the target marketplace needs different identities. See [host rendering](../../../../../docs/HostRendering.md) for metadata and host behavior.

The toolchain needs Python 3.10+, Git for commit-derived versions, and `Europe/Moscow` timezone data. PyYAML is bundled. CI needs the complete converter `scripts/` directory, not just its entry-point files: retain it in source or obtain a pinned builder checkout. Resolve script paths in that CI environment rather than copying local installed-plugin paths.

Use a clean source checkout. `.gitignore` does not filter the build payload. Root `.gitlab-ci.yml`, `.gitlab/` and `.github/` are excluded, but local caches and other unrelated files can still be copied.

### Step 3: Configure the GitLab delivery path

If GitLab builds or publishes distributions:

- Create or reuse the source project and requested distribution repositories. Set their visibility and default branches, and establish branch protection before supplying publication credentials.
- Add source-project `.gitlab-ci.yml` with a build job running the converter and validator commands above. Pass the actual source root and make all three generated trees available as job artifacts.
- Select an eligible runner with Python, Git, Bash, rsync and timezone data if using Git/rsync publication. Its tags and protected-ref access MUST match the jobs. Confirm authorization before sharing another project's runner account.
- Configure publication jobs to consume that build job's artifacts. Map each host tree to its intended destination and branch; publish the tree contents, not the enclosing `@build` directory or source checkout.
- Supply destination-scoped write credentials through masked/protected CI variables, with roles compatible with destination branch protection. Do not put credentials in source or reuse unrelated project secrets.
- Restrict publication to the agreed refs. Record source and builder revisions with the artifact and destination commit; serialize writes per destination and reject obsolete jobs. Preserve executable modes, remove stale destination files, and skip commits for unchanged trees.

Use the server version's [GitLab CI documentation](https://docs.gitlab.com/ci/) and [REST API reference](https://docs.gitlab.com/api/) for configuration syntax and remote administration. Existing source CI can be adapted, but its destinations, refs and credentials are marketplace-specific.

### Step 4: Configure the GitHub delivery path

If GitHub receives source, configure synchronization from the authoritative repository to the intended GitHub branch, preserving source rather than replacing it with a generated tree. Establish which side owns edits.

If GitHub builds distributions:

- Add an Actions workflow under `.github/workflows/`, triggered by the agreed source updates.
- Check out source and any separately pinned builder, provision the converter's dependencies, and run the same build and validation commands as Step 2.
- Publish each selected host tree to its agreed destination using credentials and branch policies that permit those writes. Do not assume the source repository's `GITHUB_TOKEN` has cross-repository write access.
- Preserve the same revision, stale-job, file-mode and replacement safeguards as the GitLab path.

Verify the source-sync mechanism actually triggers Actions. Pushes made with a workflow's `GITHUB_TOKEN` generally do not trigger another workflow; use an appropriately authorized authentication or explicit dispatch mechanism when needed. Consult [GitHub Actions documentation](https://docs.github.com/en/actions) for current permissions and event behavior.

If GitHub only receives generated distributions, configure that publication path instead of adding an unnecessary source build.

### Step 5: Activate and verify delivery

After authorization to activate publication, run an eligible source pipeline. Check the jobs used the expected source/builder revisions and that each destination matches its host artifact: file inventory, bytes, executable modes, generated metadata and bundled resources. Source CI configuration, caches and credentials MUST NOT leak into generated repositories.

Check installation and update endpoints for the selected hosts. Report local build success, live publication and installed-host testing separately; if activation is deferred or access is missing, describe the setup as prepared rather than operational.

Document repository URLs, publishing refs, consumer commands, credential ownership/expiry and renewal instructions in the configured marketplace. Include the verified pipeline/revisions and any remaining work in the finish report, without recording secret values.
