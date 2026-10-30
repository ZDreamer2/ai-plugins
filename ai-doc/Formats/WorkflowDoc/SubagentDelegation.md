# Subagent Delegation

When delegated work is stable, record its prompt in the workflow so it can be formulated and reviewed once, then reused consistently. Use placeholders for values that vary between executions.

- Use ${AGENT_FORK} when the prompt relies on the workflow's current context.
- Use ${AGENT_SUBAGENT_TOOL} when the prompt is self-contained; the prompt MUST provide all required context.
- State the delegated task and expected output clearly.
- State how the parent uses the result when later work depends on it.
