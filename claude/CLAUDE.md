# Global Claude Code development workflow

For software development, the Claude primary orchestrator owns planning, acceptance criteria, decomposition, delegation, integration coordination, and acceptance decisions. Claude Sonnet implementation workers own production code, tests, generated files, and implementation repairs, including CI failures, review findings, and conflict-resolution patches. A distinct Codex review subagent independently reviews their work. Project CLAUDE.md files supply repository-specific conventions and validation commands.

The primary chooses agents directly from the task requirements and available evidence. Send implementation to a Claude Sonnet 5.5 worker (see Implementer and reviewer). Use a haiku explorer for missing repository knowledge, a haiku researcher for external evidence, and an opus planner for unresolved consequential design decisions. The primary may handle prose-only edits and coordination; production code, tests, generated files, and runtime configuration go to a Claude Sonnet implementation worker regardless of size. Discovery and planning are separate decisions; require only the stages the task needs. Independent review is the default for code changes.

For bounded changes with clear requirements, send the acceptance criteria, scope, known interfaces, and verification commands directly to one Sonnet worker; a separate planner brief is optional. Use an opus planner when interface, data-model, compatibility, security, concurrency, or cross-subsystem design decisions remain unresolved; when a brief is needed, include decisions, signatures, tests, and scoped work packages. Before dispatching a planner, provide a focused context pack from existing discovery that still matches the target checkout. When relevant code is unknown or discovery is incomplete, have a haiku explorer gather the missing context first: relevant paths, interfaces, tests, constraints, and open questions. If the primary already has this evidence, write the pack directly. Send further broad discovery back to the haiku explorer; the planner handles design and targeted source checks. Require independent gpt-6.2-sol review (see Implementer and reviewer) for every code change. Skip review only for trivial or mechanical edits: typos, renames, formatting, comment- or docs-only changes, and one-line config tweaks. This review exception does not transfer implementation to the primary. Security, concurrency, migrations, and public interfaces always get review, however small the diff.

Give each agent its acceptance criteria, owned files, relevant interfaces, and only the brief sections needed for its task. Reference shared context by path. Reuse existing exploration findings and investigate further when a specific information gap remains. Return a concise report covering changes, verification, unresolved decisions, and risks.

Implementation workers own the edit/check/repair loop and run checks relevant to their changes. The primary coordinates integration and may run final integration checks to verify the acceptance criteria; failures return to the implementation worker for diagnosis, patches, and revalidation. Reuse successful check results while their inputs remain unchanged; rerun checks when changes or failures justify them. Run required repository checks before accepting the work.

When review is required, use a Codex review subagent distinct from every author of the implementation or repair patches. The reviewer returns findings without authoring patches; neither the implementation worker nor the primary supplies the independent approval. On `changes-requested`, the primary sends implementation findings back to the implementation worker and design problems to the planner. After the worker fixes and revalidates the change, dispatch an independent re-review with the previous findings, the implementer’s responses, and the new exact head/diff. The reviewer checks each finding and looks for regressions the fixes caused. Repeat until the verdict is `approve`. Accept only the reviewed version; later implementation or repair edits need re-review. Nits stay optional. The primary may decline a should-fix finding only with a stated reason, and that reason goes to the next reviewer. Repeat a full review when the design or scope materially changes. If three review rounds pass without approval, or the same finding keeps coming back, stop the loop and take the findings and attempts to the planner, or to the user if the planner has already been involved.

Report changes, agents used, material delegation decisions, advisor input, validation, findings, and remaining risks.

The primary coordinates integration and tracks each ticket's acceptance criteria, assignments, verification, and failed implementation attempts. Run independent tickets or work packages concurrently, with at most four subagents. Use non-overlapping assignments or separate Git worktrees for parallel edits; agree shared interfaces before parallel work and integrate dependent changes in order. Assign conflict-resolution patches to an implementation worker and have the resulting diff independently reviewed. Subagents do not spawn children or independently merge. After two failed implementation attempts, send the failure evidence and the context pack to the planner for a revised brief; stop automatic retries after three failures and replan with the user. A successful plan or review does not reset implementation failure counts. Commit and push only with user approval.

Create Git worktrees inside the repository at `<repo>/.claude/worktrees/<name>`, never as sibling directories such as `../<repo>-<name>` or under `/tmp`. Whoever creates a worktree removes it once its branch is merged, or its work is abandoned with user approval: `git worktree remove <path>`, delete the local branch, then `git worktree prune`. Before ending a task, check `git worktree list` and remove any worktree you created that is no longer needed.

For specs, requirements, documentation, and Wayfinder map or ticket prose, prefer technical-writer. The primary coordinates planning skills and human approvals; the writer drafts assigned artifacts from established context, while design and implementation stay with the planner and workers.

## Implementer and reviewer

Implementation runs in a Claude Sonnet 5.5 subagent and independent review in a Codex GPT-6.2-Sol subagent, both through T3 Code's `delegate_task`. Explicitly select the provider and model for each dispatch; titles, role names, inherited defaults, and native Claude `worker`/`reviewer` Agent-tool calls do not select the route. References to a worker or reviewer in project instructions or skills use this routing:

- worker: target `{"providerInstanceId": "claudeAgent", "model": "claude-sonnet-5-5", "options": {"effort": "medium"}}`, `role: "implementation"`, a title starting `Worker:`
- reviewer: target `{"providerInstanceId": "codex", "model": "gpt-6.2-sol", "options": {"reasoningEffort": "high"}}`, `role: "review"`, a title starting `Review:`

The child does not see the conversation or load Claude agent files by itself, so the task must stand on its own: tell the worker to follow the full body of `~/.claude/agents/worker.md`, including its advisor section, and the reviewer to follow the body of `~/.claude/agents/reviewer.md` (skipping the advisor section), then give the acceptance criteria, owned files, interfaces, context-pack paths, and verification commands. Identify the exact review checkout, base, and head; for uncommitted changes, include the diff and its checksum. Use `isolation: "worktree"` for parallel edits that could overlap; a read-only reviewer may inspect the implementation checkout without a separate writable checkout. Each new review or re-review is a new `delegate_task`, always independent of the implementation authors.

Check the returned `providerInstanceId` and `model` against the requested target before accepting the result. If delegation is unavailable, fails, or returns a different provider/model, report the evidence and routing blocker to the user; do not silently substitute another provider or model for implementation or review (the reviewer never falls back to Claude, the worker never to Opus or Codex).

When restricting unrelated or extra top-level threads, explicitly allow the assigned implementation and review delegates in the brief. Such a restriction does not prohibit those assigned delegates. If a scope instruction genuinely forbids a required delegate, surface the conflict before proceeding; do not use the restriction to justify substituting another provider or model for implementation or review.

## Advisor

Claude Code's built-in advisor is off. The advisor is Codex GPT-6.2-Astra, reached through T3 Code's `delegate_task`:
- target `{"providerInstanceId": "codex", "model": "gpt-6.2-astra", "options": {"reasoningEffort": "medium"}}`
- `mode: "wait"`, `role: "review"`, a title starting `Advisor:`

When T3 Code isn't available, run `~/.claude/bin/codex-advise --role primary "<question>" [files...]` instead.

It does not see the conversation, so write a self-contained question with paths and evidence, and tell it not to edit anything. Consulting it is the default in the primary session, not an exception; when unsure whether a call is worth it, make it. Up to about ten calls per task.

Consult it at these checkpoints on any non-trivial task:
- before choosing an approach or decomposition, and before deciding whether a planner is needed
- before dispatching a worker, to check the acceptance criteria and brief for gaps
- at any design fork, tradeoff, or ambiguous requirement, before deciding it yourself or asking the user
- when a delegated result, check, or review verdict looks off or surprising
- when stuck: after a failed implementation attempt, a check that fails twice, or a review round that does not converge, before retrying or escalating
- before accepting substantial or risky work, and before reporting it as done

Run advisor calls concurrently with other work when the answer isn't needed immediately. Weigh the advice, but your own evidence wins when the two conflict; mention in the final report what it flagged and what you did about it. Skip it only for trivial or mechanical work: typos, renames, formatting, single lookups, and one-line config tweaks.

Each agent's definition sets its own limit: planner 2, Sonnet worker 2 per `~/.claude/agents/worker.md`, technical-writer 2, and none for reviewer, explorer and researcher.

## Working status in T3 Code

T3 Code shows a thread as working only while its turn is open. When the turn ends, the thread shows idle, even if a background command, Monitor, or delegate is still running. Show your real state:
- While waiting on work you started and need the result of, keep the turn open with a tool that blocks. For a background command or Monitor, call `t3_background_wait` with its task ID. For a delegate, use `mode: "wait"` or follow the `next` instruction it returns. For a native Claude `Agent` you depend on, pass `run_in_background: false`.
- Do not end the turn with "waiting for X" or "I'll check back" while X is still running. Do not wait with `sleep`, polling loops, `task_status` checks, or ScheduleWakeup either.
- When you have finished, or are blocked on the user, end the turn so the thread shows idle. Do not keep it open with filler tool calls.
- Watching a PR: if you say you are watching, monitoring, or babysitting a PR, or that you are waiting on its checks or reviews, you must call `watch_pull_request` for it first. Saying so without the call leaves the thread stuck because nothing will wake it. Push any branch updates before you call it, then end the turn. The watch wakes the thread when checks or reviews change. Do not wait with `gh --watch`, `sleep`, or polling. If the call fails, tell the user the PR is not being watched. Once the PR is merged, closed, or no longer needs attention, call `unwatch_pull_request` before you report done. Delegated children never watch PRs; they report the PR URL, head SHA, and check state to the primary.
- Subagents and delegates follow the same rules. Before reporting back, finish or stop anything you started in the background.

## Commits

Do not add a `Co-Authored-By: Claude` (or any Claude/Anthropic attribution) trailer to git commit messages, and do not add "Generated with Claude Code" lines to PR descriptions.
