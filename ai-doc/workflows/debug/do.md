# DebugDocs Workflow Documentation

## Overview

Evaluates documentation effectiveness using actual session evidence.

From the [AiDoc core philosophy](../../Theory/AiDocBaseFormat.md#core-philosophy):
> "When genuine gaps surface through actual usage, the user will explicitly request additions."

This workflow implements that cycle: evidence-based documentation refinement.

### Input
- Optional: User description of specific session anomaly

### Output
- Documentation quality feedback with improvement direction where gaps are found

## Workflow

### Step 1: Establish data points

IF user describes specific anomaly THEN frame the observation:
- Data point: What actually happened during the session
- Desired outcome: How it should have gone
- Documentation gap: Why current guidance led to data point instead of desired outcome

IF no specific anomaly (general reflection) THEN reflect on the session as documentation consumer:
- Which documentation was loaded and used during this session
- Where documentation provided clear, sufficient guidance
- Where guidance was missing, unclear, or insufficient

All observations are data points about documentation quality, not errors or failures.

### Step 2: Investigate documentation gap

Focus on documentation system, not AI execution capability.

Problem location is uncertain - the gap might be in:
- The specific document referenced during the session
- Base format or positioning within the document
- Missing documentation that should exist
- Validation structure or constraints
- Cross-document references or loading order

### Step 3: Propose documentation improvement

Suggest specific, actionable changes to address the identified gap.
