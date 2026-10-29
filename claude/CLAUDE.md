# Global Claude Code development workflow

For software development, the primary orchestrator owns acceptance criteria, decomposition, integration, and final verification. Project CLAUDE.md files supply repository-specific conventions and validation commands.

The primary chooses agents directly from the task requirements and available evidence. Default to a Codex gpt-6.1-sol worker (see Implementer and reviewer) for implementation with clear acceptance criteria. Use a haiku explorer for missing repository knowledge, a haiku researcher for external evidence, and an opus planner for unresolved consequential design decisions. Keep trivial work in the primary session. Discovery and planning are separate decisions; require only the stages the task needs. Independent review is the default for code changes.

For bounded changes with clear requirements, send the acceptance criteria, scope, known interfaces, and verification commands directly to one gpt-6.1-sol worker; a separate planner brief is optional. Use an opus planner when interface, data-model, compatibility, security, concurrency, or cross-subsystem design decisions remain unresolved; when a brief is needed, include decisions, signatures, tests, and scoped work packages. Before dispatching a planner, provide a focused context pack from existing discovery that still matches the target checkout. When relevant code is unknown or discovery is incomplete, have a haiku explorer gather the missing context first: relevant paths, interfaces, tests, constraints, and open questions. If the primary already has this evidence, write the pack directly. Send further broad discovery back to the haiku explorer; the planner handles design and targeted source checks. Require independent gpt-6.1-sol review (see Implementer and reviewer) for every code change, whether a worker or the primary made it. Skip review only for trivial or mechanical edits: typos, renames, formatting, comment- or docs-only changes, and one-line config tweaks. Security, concurrency, migrations, and public interfaces always get review, however small the diff.

Give each agent its acceptance criteria, owned files, relevant interfaces, and only the brief sections needed for its task. Reference shared context by path. Reuse existing exploration findings and investigate further when a specific information gap remains. Return a concise report covering changes, verification, unresolved decisions, and risks.

Workers run checks relevant to their changes. The primary runs integration checks after combining work and verifies the acceptance criteria. Reuse successful check results while their inputs remain unchanged; rerun checks when changes or failures justify them. Run required repository checks before accepting the work.

When review is required, loop until the reviewer approves. On `changes-requested`, send the blocking and should-fix findings back: implementation fixes to the implementer, design problems to the planner. Then start a new review with the previous findings, the implementer’s responses, and the new diff. The follow-up reviewer checks that each finding was resolved and looks for regressions the fixes caused. Repeat until the verdict is `approve`. Accept the work only on approval; nits stay optional. The primary may decline a should-fix finding only with a stated reason, and that reason goes to the next reviewer. Repeat a full review when the design or scope materially changes. If three review rounds pass without approval, or the same finding keeps coming back, stop the loop and take the findings and attempts to the planner, or to the user if the planner has already been involved.

Report changes, agents used, material delegation decisions, validation, findings, and remaining risks.

The primary owns integration and tracks each ticket's acceptance criteria, assignments, verification, and failed implementation attempts. Run independent tickets or work packages concurrently, with at most four subagents. Use non-overlapping assignments or separate Git worktrees for parallel edits; agree shared interfaces before parallel work and integrate dependent changes in order. Subagents do not spawn children or independently merge. After two failed implementation attempts, send the failure evidence and the context pack to the planner for a revised brief; stop automatic retries after three failures and replan with the user. A successful plan or review does not reset implementation failure counts. Commit and push only with user approval.

Create Git worktrees inside the repository at `<repo>/.claude/worktrees/<name>`, never as sibling directories such as `../<repo>-<name>` or under `/tmp`. Whoever creates a worktree removes it once its branch is merged, or its work is abandoned with user approval: `git worktree remove <path>`, delete the local branch, then `git worktree prune`. Before ending a task, check `git worktree list` and remove any worktree you created that is no longer needed.

For specs, requirements, documentation, and Wayfinder map or ticket prose, prefer technical-writer. The primary coordinates planning skills and human approvals; the writer drafts assigned artifacts from established context, while design and implementation stay with the planner and workers.

## Implementer and reviewer

Implementation and independent review run on Codex GPT-6.1-Sol through T3 Code's `delegate_task`, not on the Claude `worker` and `reviewer` agents:
- worker: target `{"providerInstanceId": "codex", "model": "gpt-6.1-sol", "options": {"reasoningEffort": "medium"}}`, `role: "worker"`, a title starting `Worker:`
- reviewer: target `{"providerInstanceId": "codex", "model": "gpt-6.1-sol", "options": {"reasoningEffort": "high"}}`, `role: "review"`, a title starting `Review:`

The child does not see the conversation or load Claude agent files, so the task must stand on its own: tell it to follow the role instructions in the body of `~/.claude/agents/worker.md` or `~/.claude/agents/reviewer.md` (skipping the advisor section), then give the acceptance criteria, owned files, interfaces, context-pack paths, and verification commands. Use `isolation: "worktree"` for parallel edits that could overlap. Each new review or re-review is a new `delegate_task`.

When T3 Code isn't available, fall back to the Claude `worker` (sonnet) and `reviewer` (opus) agents.

## Advisor

Claude Code's built-in advisor is off. The advisor is Codex GPT-6-Astra, reached through T3 Code's `delegate_task`:
- target `{"providerInstanceId": "codex", "model": "gpt-6-astra", "options": {"reasoningEffort": "medium"}}`
- `mode: "wait"`, `role: "review"`, a title starting `Advisor:`

When T3 Code isn't available, run `~/.claude/bin/codex-advise --role primary "<question>" [files...]` instead.

It does not see the conversation, so write a self-contained question with paths and evidence, and tell it not to edit anything. Use it freely in the primary session, up to about five calls per task, whenever a second opinion could change a decision: before committing to an approach on non-trivial work, at design forks or tradeoffs, when stuck after a failed attempt, when a delegated result looks off, and before accepting substantial or risky work. Skip it for trivial or mechanical work. Each agent's definition sets its own limit: planner 2, worker 2 (Codex worker per `~/.codex/AGENTS.md`, or the fallback Claude worker), technical-writer 2, and none for reviewer, explorer and researcher.

## Commits

Do not add a `Co-Authored-By: Claude` (or any Claude/Anthropic attribution) trailer to git commit messages, and do not add "Generated with Claude Code" lines to PR descriptions.
