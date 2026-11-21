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
| protocols/discovery.md | skills/how, skills/why, skills/poteto-mode/playbooks/investigation.md |
| protocols/architecture.md | skills/architect, skills/principle-model-the-domain, principle-foundational-thinking, principle-boundary-discipline |
| protocols/planning.md | skills/principle-sequence-verifiable-units, poteto-mode/playbooks/{multi-phase-plan,feature,bug-fix,refactoring}.md |
| protocols/review.md | skills/interrogate, skills/blast-radius |
| protocols/verification.md | skills/principle-prove-it-works, principle-test-behavior-not-implementation, principle-sequence-verifiable-units |
| protocols/handoff.md | skills/poteto-mode/playbooks/pause-safely.md |
| principles.md | the principle-* skills named in each entry |
| SKILL.md stage router | skills/poteto-mode/SKILL.md (structure only; rewritten for this repo's routing) |

## Not adapted

- Autonomy rules in poteto-mode ("use any MCP tool", never ask, fully autonomous overrides): conflict with this repo's approval rules.
- poteto-mode/worker.md and its PR rules: this repo has its own worker and reviewer roles.
- recall, reflect, automate-me, session-pickup: read transcripts and session logs.
- setup-pstack and rules-file writes, upstream model slugs and panels: would change model routing and files outside this repo.
- All scripts (watch-pr, bootstrap, statechart, worktree-audit, logging): not executed or copied.
- automations/benny, make-bot-ui: unrelated automation.
- Cursor-only features, arena/swarm multi-vendor panels, cursor-team-kit references: not available or not wanted here.
- agents/poteto-agent and comment-sicko: personas for the upstream plugin.
- Remaining skills not needed for this workflow.

## Refreshing

Re-review a newer pinned upstream commit by hand, update the files above, and update the pinned SHAs and date here.
