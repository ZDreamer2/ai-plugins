# Configure local marketplace editing

## Overview

Prepare one workstation for marketplace source editing with agent help, using a simple configuration suitable for domain experts.

### Input

- The employee's agent host, authoritative source repository URL and required plugins.
- The employee's Git author name and email.
- Applicable host, Git, access and marketplace administration instructions.

### Output

- A ready source checkout and fresh agent session with the required plugins.
- Setup and verification outcomes, including any remaining access or host-configuration blockers.

## Workflow

### Step 1: Establish the target and applicable instructions

Identify the employee's agent host and required plugins. Determine the operating system from the environment when platform-specific instructions require it. Collect the authoritative source repository URL and the employee's Git author name and email. Use the request and available local documentation; ask only for missing values that materially affect setup.

Read the applicable host, Git, access and marketplace administration instructions. They own concrete installation, account and credential mechanics. Read source-repository instructions when available. Keep this workflow scoped to local editing rather than central hosting, CI or publication.

### Step 2: Prepare Git and repository access

Follow the applicable instructions to install Git and configure authentication. Perform Git configuration in the employee's user session, preserve other suitable existing configuration, and use the employee's identity and credentials rather than an administrator's.

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

### Step 3: Install the agent and required plugins

Follow the host instructions to install or configure the employee's agent. Install and enable `ai-doc`, `ai-marketplace` and the plugins needed for the employee's work, using their documented distributions.

Connecting a marketplace does not necessarily install its plugins. Distinguish generated distributions used for installation from the authoritative source checkout used for editing.

### Step 4: Create or adopt the source checkout

Always use the current working directory as the checkout parent; do not ask for or select another location. If the checkout is absent, run:

```sh
git clone "<source repository URL>"
```

If the current directory is already the requested checkout, or it already contains that checkout, preserve all existing work and do not clone over, reset or clean it. Inspect it from the checkout directory:

```sh
git remote -v
git branch --show-current
git status
```

Confirm that the remote is the requested authoritative source repository and that the checkout contains marketplace sources rather than a generated distribution. Open that checkout as the agent's project root for subsequent editing sessions.

### Step 5: Verify a fresh editing session

In a fresh agent session opened at the source checkout, verify that applicable repository instructions are available and that `ai-doc`, `ai-marketplace` and the required working plugins are available. Confirm that the agent can orient ordinary source-editing and sharing requests to Build and Sync.

Setup verification does not require source edits, compilation, commits or pushes. Report the checkout path, plugin status, access evidence and remaining blockers. If fresh-session verification cannot be completed, describe the setup as prepared rather than verified.
