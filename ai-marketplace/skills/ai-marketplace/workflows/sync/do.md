# Synchronize marketplace source

## Overview

Invoking Sync authorizes committing the intended changes and pushing them to the established upstream. Honor any limits the user sets; otherwise proceed without another confirmation or routine joint review.

### Input

- The source checkout and requested synchronization outcome.
- Any explicit limits, such as inspect only, integrate without committing, or do not push.

### Output

- The requested source synchronization, or a safely paused state with the decision or blocker explained.
- A plain-language account of content changes, integration and Git outcomes.

## Workflow

### Step 1: Establish the source checkout and conventions

Select exactly one authoritative source checkout. Confirm that it is a source repository rather than a generated distribution, and establish its current branch and upstream. Ask before modifying anything if the checkout or upstream is unclear.

Read applicable source-repository instructions. Follow their explicit commit-message and integration conventions and any boundaries around protected files; those conventions do not override work preservation.

Honor explicit approval requirements for protected changes. Keep CI, credentials, builder snapshots and generated-distribution publication outside a content sync.

### Step 2: Inspect local and incoming work

Before changing the working tree:

- Record the current revision and inspect modified and untracked files.
- Review local commits not present upstream.
- Fetch from upstream, then inspect incoming commits and their diffs.
- Distinguish the requested work from unrelated pre-existing changes.

Use this inspection to understand both contributors' work. If the user requested inspection only, summarize the state and stop. If fetching fails, report the access or network problem without changing local work.

### Step 3: Preserve and commit intended local work

When the requested outcome includes committing or pushing, determine which pending changes belong to that outcome. Ask when ownership or intent is unclear. Leave unrelated changes untouched and uncommitted.

Review the intended diff, stage only its files and create one commit with a descriptive message. Do not create an empty commit, amend existing commits or stage the whole checkout indiscriminately.

When integrating incoming changes without committing, preserve uncommitted work without including it in a commit. If remaining local work would obstruct integration, use a non-destructive preservation approach and track its restoration; never commit unrelated work merely to make synchronization proceed.

### Step 4: Integrate incoming changes

If upstream has not advanced, no integration is needed. Fast-forward when only upstream advanced.

When local and upstream commits have diverged, use the repository's explicit integration convention. Otherwise, merge upstream into the current branch using the already fetched state; do not let workstation Git configuration silently select rebase. Accept an ordinary merge commit without asking the user.

Apply an explicit repository rebase convention only to local commits that have not been published upstream. Never rewrite shared history.

Restore any temporarily preserved uncommitted work after integration. Handle restoration conflicts with the same preservation and escalation rules as integration conflicts.

### Step 5: Resolve or escalate conflicts

When integration conflicts, inspect the common ancestor and both contributors' versions together with the surrounding domain context. Resolve and stage the combined content only when the intended result is clear. Review the resolved files rather than treating conflict-marker removal as sufficient.

If the intended content is ambiguous, explain the alternatives in plain language and ask the content owner. Preserve both versions and the repository's conflicted state while waiting. Do not choose an entire side merely because it is easier, and do not discard changes to obtain a clean status.

### Step 6: Verify what will be pushed

Check that the outgoing commits contain only the intended changes and preserve incoming work. Inspect any conflict resolutions not already verified.

Run checks required by the repository or requested by the user. Compilation and generated-distribution publication are separate from Sync.

If the user limited Sync to a local result, report it and stop.

### Step 7: Push and report the outcome

Push normally to the established upstream. Never force-push to make synchronization succeed.

If the push is rejected because upstream advanced, return to Step 2, inspect the new incoming work and integrate it before retrying. If rejection concerns authentication, permissions or protected-branch rules, stop and report that blocker rather than repeatedly integrating or attempting other credentials.

Report what content changed, how concurrent work was combined, and whether the source push completed. Mention unresolved conflicts, preserved unrelated changes or remaining blockers when present. Use plain language rather than requiring the user to interpret Git terminology. A successful source push does not establish that CI or generated-distribution publication completed.
