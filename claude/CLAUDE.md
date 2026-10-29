# Global Claude Code development workflow

For software development, the primary orchestrator owns acceptance criteria, decomposition, integration, and final verification. Project CLAUDE.md files supply repository-specific conventions and validation commands.

The primary chooses agents directly from the task requirements and available evidence. Default to a sonnet worker for implementation with clear acceptance criteria. Use a haiku explorer for missing repository knowledge, a haiku researcher for external evidence, and an opus planner for unresolved consequential design decisions. Keep trivial work in the primary session. Discovery, planning, and independent review are separate decisions; require only the stages the task needs.

For bounded changes with clear requirements, send the acceptance criteria, scope, known interfaces, and verification commands directly to one sonnet worker; a separate planner brief is optional. Use an opus planner when interface, data-model, compatibility, security, concurrency, or cross-subsystem design decisions remain unresolved; when a brief is needed, include decisions, signatures, tests, and scoped work packages. Before dispatching a planner, provide a focused context pack from existing discovery that still matches the target checkout. When relevant code is unknown or discovery is incomplete, have a haiku explorer gather the missing context first: relevant paths, interfaces, tests, constraints, and open questions. If the primary already has this evidence, write the pack directly. Send further broad discovery back to the haiku explorer; the planner handles design and targeted source checks. Require independent opus review for security, concurrency, migrations, public interfaces, or substantial changes.

Give each agent its acceptance criteria, owned files, relevant interfaces, and only the brief sections needed for its task. Reference shared context by path. Reuse existing exploration findings and investigate further when a specific information gap remains. Return a concise report covering changes, verification, unresolved decisions, and risks.

Workers run checks relevant to their changes. The primary runs integration checks after combining work and verifies the acceptance criteria. Reuse successful check results while their inputs remain unchanged; rerun checks when changes or failures justify them. Run required repository checks before accepting the work.

When review is required, resolve blocking findings with the implementer or planner before accepting the work. Give follow-up reviewers the previous findings, the implementer’s responses, and the new diff. Check unresolved findings and regressions caused by the fixes. Repeat a full review when the design or scope materially changes.

Report changes, agents used, material delegation decisions, validation, findings, and remaining risks.

The primary owns integration and tracks each ticket's acceptance criteria, assignments, verification, and failed implementation attempts. Run independent tickets or work packages concurrently, with at most four subagents. Use non-overlapping assignments or separate Git worktrees for parallel edits; agree shared interfaces before parallel work and integrate dependent changes in order. Subagents do not spawn children or independently merge. After two failed implementation attempts, send the failure evidence and the context pack to the planner for a revised brief; stop automatic retries after three failures and replan with the user. A successful plan or review does not reset implementation failure counts. Commit and push only with user approval.

For specs, requirements, documentation, and Wayfinder map or ticket prose, prefer technical-writer. The primary coordinates planning skills and human approvals; the writer drafts assigned artifacts from established context, while design and implementation stay with the planner and workers.

## Advisor

Claude Code's built-in advisor is off. The advisor is Codex GPT-6-Astra, reached through T3 Code's `delegate_task`:
- target `{"providerInstanceId": "codex", "model": "gpt-6-astra", "options": {"reasoningEffort": "medium"}}`
- `mode: "wait"`, `role: "review"`, a title starting `Advisor:`

When T3 Code isn't available, run `~/.claude/bin/codex-advise --role primary "<question>" [files...]` instead.

It does not see the conversation, so write a self-contained question with paths and evidence, and tell it not to edit anything. In the primary session, ask it at most twice per task: once before committing to an approach on non-trivial work, and once when stuck after a failed attempt. Each agent's definition sets its own limit: planner 1, worker 1 (only when stuck), technical-writer 1, and none for reviewer, explorer and researcher.

## Commits

Do not add a `Co-Authored-By: Claude` (or any Claude/Anthropic attribution) trailer to git commit messages, and do not add "Generated with Claude Code" lines to PR descriptions.
