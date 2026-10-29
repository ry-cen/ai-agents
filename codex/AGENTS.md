# Global Codex development workflow

For software development, the primary orchestrator owns acceptance criteria, decomposition, integration, and final verification. Project AGENTS.md files supply repository-specific conventions and validation commands.

The Codex primary chooses Codex agents directly from the task requirements and available evidence. Use Codex-native subagents when they support the selected model and settings; otherwise use T3 delegation with the Codex provider instance from the live catalog. Keep agent selection and delegated work on Codex unless the user explicitly requests another provider. Default to a gpt-6.1-sol worker for implementation with clear acceptance criteria. Use a gpt-6-luna explorer for missing repository knowledge, a gpt-6-luna researcher for external evidence, and a gpt-6-astra planner for unresolved consequential design decisions. Keep trivial work in the primary session. Discovery, planning, and independent review are separate decisions; require only the stages the task needs.

For bounded changes with clear requirements, send the acceptance criteria, scope, known interfaces, and verification commands directly to one gpt-6.1-sol worker; a separate planner brief is optional. Use a gpt-6-astra planner when interface, data-model, compatibility, security, concurrency, or cross-subsystem design decisions remain unresolved; when a brief is needed, include decisions, signatures, tests, and scoped work packages. Before dispatching a planner, provide a focused context pack from existing discovery that still matches the target checkout. When relevant code is unknown or discovery is incomplete, have a gpt-6-luna explorer gather the missing context first: relevant paths, interfaces, tests, constraints, and open questions. If the primary already has this evidence, write the pack directly. Send further broad discovery back to the gpt-6-luna explorer; the planner handles design and targeted source checks. Require independent gpt-6.1-sol review for security, concurrency, migrations, public interfaces, or substantial changes.

Give each agent its acceptance criteria, owned files, relevant interfaces, and only the brief sections needed for its task. Reference shared context by path. Reuse existing exploration findings and investigate further when a specific information gap remains. Return a concise report covering changes, verification, unresolved decisions, and risks.

Workers run checks relevant to their changes. The primary runs integration checks after combining work and verifies the acceptance criteria. Reuse successful check results while their inputs remain unchanged; rerun checks when changes or failures justify them. Run required repository checks before accepting the work.

When review is required, resolve blocking findings with the implementer or planner before accepting the work. Give follow-up reviewers the previous findings, the implementer’s responses, and the new diff. Check unresolved findings and regressions caused by the fixes. Repeat a full review when the design or scope materially changes.

Report changes, agents used, material delegation decisions, validation, findings, and remaining risks.

The primary owns integration and tracks each ticket's acceptance criteria, assignments, verification, and failed implementation attempts. Run independent tickets or work packages concurrently, with at most four subagents. Use non-overlapping assignments or separate Git worktrees for parallel edits; agree shared interfaces before parallel work and integrate dependent changes in order. Subagents do not spawn children or independently merge. After two failed implementation attempts, send the failure evidence and the context pack to the planner for a revised brief; stop automatic retries after three failures and replan with the user. A successful plan or review does not reset implementation failure counts. Commit and push only with user approval.

For specs, requirements, documentation, and Wayfinder map or ticket prose, prefer technical_writer. The primary coordinates planning skills and human approvals; the writer drafts assigned artifacts from established context, while design and implementation stay with the planner and workers.

## Advisor

For a second opinion, use GPT-6-Astra through T3 Code's `delegate_task` when available:
- target `{"providerInstanceId": "codex", "model": "gpt-6-astra", "options": {"reasoningEffort": "medium"}}`
- `mode: "wait"`, `role: "review"`, a title starting `Advisor:`

Discover the live model catalog and tool schema before calling. Give a self-contained question with paths and evidence, and require read-only advice. If T3 delegation is unavailable, continue without an advisor and report the gap. In the primary session, ask at most twice per task: once before committing to an approach on non-trivial work, and once when stuck after a failed attempt. Each agent's definition sets its own limit: planner 1, worker 1 (only when stuck), technical_writer 1, and none for reviewer, explorer and researcher.

## Commits

Do not add AI attribution trailers to git commit messages or generated-by lines to PR descriptions.
