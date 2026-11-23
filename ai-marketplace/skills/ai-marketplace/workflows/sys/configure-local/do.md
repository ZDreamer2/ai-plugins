# Configure local marketplace editing

## Overview

Prepare an existing marketplace source checkout and the current agent session for source editing by a developer or domain expert.

### Input

- An agent session whose current working directory is the root of an existing authoritative source checkout.
- The employee's Git author name and email.
- Applicable host, Git, access and marketplace administration instructions.

### Output

- A verified source checkout and current agent session ready for marketplace source editing.
- Setup and verification outcomes, including any remaining access blockers.

## Workflow

### Step 1: Verify the checkout and applicable instructions

Confirm that the current working directory is the source checkout root and that it contains marketplace sources rather than a generated distribution. Inspect its state:

```sh
git rev-parse --show-toplevel
git remote -v
git branch --show-current
git status
```

Confirm that the remote is the expected authoritative source repository. Preserve all existing work and configuration; do not clone, reset, clean or select another checkout. If the agent is not rooted at the existing source checkout, report the unmet prerequisite and ask the user to reopen the agent there.

Read the applicable host, Git, access, marketplace administration and source-repository instructions. They own concrete account and credential mechanics. Ask only for missing values that materially affect setup. Keep this workflow scoped to local editing rather than central hosting, CI or publication.

### Step 2: Prepare Git and repository access

Follow the applicable instructions to install Git if needed and configure authentication. Perform Git configuration in the employee's user session, preserve other suitable existing configuration, and use the employee's identity and credentials rather than an administrator's.

Check the installation:

```sh
git --version
```

If the Git author identity is missing or belongs to someone else, set it with the collected values:

```sh
git config --global user.name "<employee Git author name>"
git config --global user.email "<employee Git email>"
```

Verify the effective identity:

```sh
git config --global --get user.name
git config --global --get user.email
```

Verify authentication and repository access with non-mutating checks. A successful read does not establish write access; use hosting permissions or other non-mutating evidence for the required write access. Do not use a test commit or push. Report missing access instead of substituting unrelated credentials.

### Step 3: Verify editing readiness

Verify that applicable source-repository instructions are available in the current session. Confirm that the agent can orient ordinary source-editing and sharing requests to Build and Sync.

Setup verification does not require source edits, compilation, commits or pushes. Report the checkout path, remote, Git identity and access evidence, and remaining blockers. If any of these cannot be verified in the current session, describe the setup as prepared rather than verified.
