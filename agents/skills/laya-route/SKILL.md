---
name: laya-route
description: Consult the local Laya decision model before meaningful Codex software-development delegation, architectural escalation, or retry decisions. Select native Codex agents and record outcomes.
---

Use at task boundaries, not for individual shell commands. Sanitize task descriptions: include acceptance criteria and needed capabilities, omit secrets and unnecessary source code.

1. Call the `laya_router` MCP tool `route_task` with a concise task description. Reuse its opaque `task_id` for the same work and retries. Set `risk="high"` for security-sensitive behavior, concurrency, significant architecture, and important database/distributed-system decisions. Substantial completed implementations also require an architect review before completion.
2. Inspect `recommendation`, `confidence`, `selected_agent`, `reason`, and the typed `factors`. Probabilities are advisory and have not been calibrated for your repository. Low-confidence or unavailable inference returns control to you. Apply the role criteria below to select the actual agent; disclose material overrides.
3. Delegate with native Codex agent tools using the installed custom agent by name. Use a fresh child context when required for its model and configuration. Give one bounded assignment, acceptance criteria, and exclusive file ownership. `orchestrator` means keep/decompose work in the primary session, not spawn another orchestrator.
4. Call `record_outcome(task_id, actual_agent, "started", "pending")` and retain its returned `attempt_id`. After completion, record the terminal outcome and validation with that same `attempt_id`; delivery retries are deduplicated. Use a new attempt ID for a new execution. Use `escalation=true` when escalating. Read-only research may use `not_applicable`; implementations and technical-writing deliverables need passed validation before success. For writing, check scope, acceptance-criteria coverage, terminology, dependencies, and references. A successful architect review does not reset implementation failure counts.
5. After two failed attempts at the same work, consult Astra. After three failures, stop automatic retries and replan with new evidence. Keep the same task ID while retrying; renaming a task does not reset the retry budget.

| Agent | Use |
|---|---|
| explorer | Simple repository searches, file/function discovery, dependency and execution-path inspection. |
| researcher | External documentation and evidence, source-backed technology comparisons. |
| technical_writer | Specs, acceptance criteria, documentation, Wayfinder map/decision-ticket prose; use established decisions and document ownership. |
| worker | Scoped implementation, tests, ordinary debugging. |
| architect | Significant design decisions, difficult tradeoffs, repeated failures, high-risk or substantial feature review. Ask for actionable findings with file/line evidence and fixes. |
| orchestrator | Ambiguous or multipart requests, decomposition, coordination, integration, and final verification. |

The primary coordinates Matt Pocock Wayfinder and any skill that delegates; assign its prose/artifact drafting to technical_writer. Keep architecture decisions with architect, external evidence with researcher, and prototypes/implementation with worker.

Run independent assignments concurrently, with at most four children. For overlapping coding work, use isolated Git worktrees when appropriate and retain integration ownership. Children return results to the primary and do not delegate. Get user approval before committing or pushing. Laya never grants permissions or overrides sandbox/approval controls.

If MCP is unavailable, run:

```sh
/Users/raian/.codex/laya-routing/.venv/bin/python /Users/raian/.codex/laya-routing/router.py route --task-id TASK_ID <<'TASK'
Sanitized task description
TASK
```

The equivalent CLI `record TASK_ID ROLE OUTCOME VALIDATION [--escalation] [--attempt-id ID]` records lifecycle events. Supply the returned attempt ID for terminal outcomes. If the sandbox prevents logging or execution, continue with explicit orchestrator judgment and report the unavailable router/logging; do not broaden permissions automatically. If `retry_allowed=false`, stop and replan regardless of inference status; unknown/corrupt retry history must be resolved before automatic retries.

Routing and lifecycle recording are prompt-driven. This skill does not intercept or enforce native spawn calls, and the router never runs coding agents itself.
