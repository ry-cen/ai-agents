# Provenance

This skill adapts guidance from pstack, a Cursor plugin.

- Marketplace: https://cursor.com/marketplace/cursor/pstack
- Source: https://github.com/cursor/plugins/tree/main/pstack
- Pinned cursor/plugins commit: d42aff08aa58965d2735c4ead61a9af82b89d0d0
- Last pstack-touching commit: 0b46ec399d55f2829e88822998f53b84944837d3
- Plugin version: 0.15.46
- Reviewed: 2026-11-20
- License: MIT, copyright (c) 2026 Lauren Tan (see [LICENSE-pstack](LICENSE-pstack))

Nothing from upstream is executed or installed. The files here are original rewrites of read-only reference material; no upstream scripts were copied.

## Mapping

| Our file | Upstream source (under pstack/) |
| --- | --- |
| protocols/discovery.md | skills/how/SKILL.md, skills/why/SKILL.md, skills/poteto-mode/playbooks/investigation.md |
| protocols/architecture.md | skills/architect/SKILL.md, skills/principle-model-the-domain/SKILL.md, skills/principle-foundational-thinking/SKILL.md, skills/principle-boundary-discipline/SKILL.md |
| protocols/planning.md | skills/principle-sequence-verifiable-units/SKILL.md, skills/poteto-mode/playbooks/multi-phase-plan.md, skills/poteto-mode/playbooks/feature.md, skills/poteto-mode/playbooks/bug-fix.md, skills/poteto-mode/playbooks/refactoring.md |
| protocols/review.md | skills/interrogate/SKILL.md, skills/blast-radius/SKILL.md |
| protocols/verification.md | skills/principle-prove-it-works/SKILL.md, skills/principle-test-behavior-not-implementation/SKILL.md, skills/principle-sequence-verifiable-units/SKILL.md |
| protocols/handoff.md | skills/poteto-mode/playbooks/pause-safely.md |
| principles.md | skills/principle-*/SKILL.md for the principles named in each entry |
| SKILL.md stage router | skills/poteto-mode/SKILL.md (structure only; rewritten for this repo's routing) |

## Not adapted

- Autonomy rules in skills/poteto-mode/SKILL.md ("use any MCP tool", never ask, fully autonomous overrides): conflict with this repo's approval rules.
- skills/poteto-mode/worker.md and its PR rules: this repo has its own worker and reviewer roles.
- skills/recall/SKILL.md, skills/reflect/SKILL.md, skills/automate-me/SKILL.md, skills/poteto-mode/playbooks/session-pickup.md: read transcripts and session logs.
- skills/setup-pstack/SKILL.md and rules-file writes, upstream model slugs and panels: would change model routing and files outside this repo.
- All scripts (watch-pr, bootstrap, statechart, worktree-audit, logging): not executed or copied.
- automations/benny, skills/make-bot-ui/SKILL.md: unrelated automation.
- Cursor-only features, arena/swarm multi-vendor panels, cursor-team-kit references: not available or not wanted here.
- agents/poteto-agent.md and agents/comment-sicko.md personas: personas for the upstream plugin.
- Remaining skills not needed for this workflow.

## Refreshing

Re-review a newer pinned upstream commit by hand, update the files above, and update the pinned SHAs and date here.
