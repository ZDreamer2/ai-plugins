# do.meta.md

Specification for editing [Documentation debugging workflow](do.md). Defines purpose, usage patterns, and constraints.

## do.md goals and principles

- Guides post-session reflection on documentation quality, identifying gaps that caused suboptimal AI behavior
- Frames anomalies and failures as practical data points about documentation gaps, not as AI errors
- Documentation is accountable for AI guidance quality - if AI performed poorly, documentation failed to guide properly
- Follows StartSimple methodology - minimal initial version, expand based on practical evidence

## AiDocFormat

[WorkflowDoc format](../../Formats/WorkflowDoc/WorkflowDoc.format.md)

## MUST read before editing do.md

- [StartSimple methodology](../../Theory/StartSimple.md) - Maintain minimal approach when expanding the workflow; add complexity only when proven gaps surface through real sessions

## do.md typical use context

### 💡 Distinct usage patterns for do.md

#### Direct invocation with specific anomaly

`/ai-doc debug AI created entity files in wrong directory structure, didn't follow CodeUnit patterns`

#### Direct invocation for general session reflection

`/ai-doc debug`

### Role do.md serves during use

- Structured reflection framework for evaluating whether documentation provided sufficient guidance during the session
- Reframes user-observed problems as documentation improvement opportunities rather than AI failures

## do.md underlying theory

### Documentation Accountability

When AI behavior deviates from expectations during a session, root cause analysis defaults to documentation gaps rather than AI capability limitations. This framing makes documentation improvement actionable - each anomaly points to a specific documentation gap that can be addressed.

Prevents dismissing issues as "AI limitations" when better guidance could have prevented them.

### Anomalies as Practical Data Points

Session anomalies are the most valuable validation data for documentation quality. Each anomaly provides:

- Evidence of where documentation guidance was insufficient
- Direction for targeted documentation improvement
- Validation input for the StartSimple iterative cycle (evidence-based expansion)

The distinction matters: "data point" triggers investigation and improvement, while "error/failure" triggers defensiveness and dismissal.
