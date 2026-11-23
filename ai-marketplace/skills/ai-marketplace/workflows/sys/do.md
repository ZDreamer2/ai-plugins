# Configure marketplace systems

## Goal

Route the configuration request to the workflow that owns its central delivery or local editing target.

Use the request and conversation to establish the marketplace context. Clarify only missing details that materially affect the work.

## Scenarios

### Central repository

`sys configure-central` sets up source hosting, automated builds and generated-distribution publication.

Follow [Central repository configuration](configure/do.md).

### Local editing

`sys configure-local` prepares a workstation and one authoritative source checkout for marketplace editing with agent help.

Follow [Local editing configuration](local/do.md).
