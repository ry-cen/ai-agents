---
name: pstack
description: >-
  Staged engineering workflow (discover, architect, plan, implement, review, verify, hand off) for substantive engineering: features, bug fixes, refactors, migrations, multi-file or cross-module changes, and design decisions. Also for "pstack", "/pstack", "pstack workflow". Not for trivial or mechanical edits (typos, renames, formatting, one-line config) or read-only Q&A.
---

# pstack

Adapted staged workflow. Protocols are short guidance files; read only the ones your stage needs.

## Role check (first)

- Only the primary coordinator (the Claude Opus session that owns the task) selects stages automatically for substantive engineering. An explicit user request can select pstack for smaller work.
- Opt-out wins: "no pstack", "pstack off", or a project instruction saying so means do not use it.
- A delegated child (Sonnet worker, Codex Sol reviewer, Codex Astra advisor, Opus planner, haiku explorer or researcher, technical-writer) reads only the protocol that matches its brief. It never runs orchestrator steps and never spawns workers or reviewers or delegates tasks; advisor calls are allowed exactly as that child's own role file permits. Its brief wins over pstack. Astra gives advice only; Sol reviews only the exact assigned version.

## Precedence

Repo and user instructions, approval rules, and `~/.claude/CLAUDE.md` routing win over this skill. A pstack recommendation never authorizes an action: commit, push, merge, deploy, and delegation all stay under the existing approval rules.

## Stages

Use only the stages the task needs; skip one when its output already exists.

| Task type | Stages |
| --- | --- |
| Read-only question, how/why | Discover |
| Bug fix | Discover, Plan (small), Implement, Review, Verify |
| Feature or refactor | Discover, Architect, Plan, Implement, Review, Verify |
| Migration or cross-module change | all stages; Architect via the Opus planner |
| Pausing mid-task | Handoff |

| Stage | Read | Who |
| --- | --- | --- |
| Discover | [protocols/discovery.md](protocols/discovery.md) | primary, or haiku explorer/researcher |
| Architect | [protocols/architecture.md](protocols/architecture.md) | Opus planner when decisions are unresolved |
| Plan | [protocols/planning.md](protocols/planning.md) | primary |
| Implement | the worker brief; [protocols/verification.md](protocols/verification.md) | Sonnet worker, per "Implementer and reviewer" in `~/.claude/CLAUDE.md` |
| Independent review | [protocols/review.md](protocols/review.md) | Sol reviewer, dispatched by the primary per the same routing |
| Verify | [protocols/verification.md](protocols/verification.md) | worker runs checks; primary confirms acceptance criteria |
| Handoff | [protocols/handoff.md](protocols/handoff.md) | whoever is pausing |

Cross-cutting guidance: [principles.md](principles.md).

## Roles

Roles and model routing are defined only in `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`. In short: Opus coordinates and plans, Sonnet 5.5 implements, GPT-6.2 Astra advises, GPT-6.2 Sol reviews, haiku explores and researches. Do not restate or override model IDs here.

## Not included

Upstream autonomy rules, scripts, transcript-reading skills, setup and rules-file writes, multi-vendor panels, and Cursor-only features are intentionally left out. See [PROVENANCE.md](PROVENANCE.md).

Adapted from pstack by Lauren Tan (MIT); license in [LICENSE-pstack](LICENSE-pstack).
