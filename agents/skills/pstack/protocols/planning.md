# Planning

Adapted from pstack skills/principle-sequence-verifiable-units/SKILL.md, skills/poteto-mode/playbooks/multi-phase-plan.md, skills/poteto-mode/playbooks/feature.md, skills/poteto-mode/playbooks/bug-fix.md, skills/poteto-mode/playbooks/refactoring.md (MIT).

The plan is a checklist the owner can run box by box and the primary can audit from evidence. Planning does not implement.

1. Throughput checkpoint: can this be one small change? If it touches one or two files with an obvious approach, skip the plan and say so.
2. Settle factual questions by inspection or a quick read-only probe before writing. Clarification and approval decisions follow existing instructions: a delegate with an ambiguous brief stops and reports to the primary, and the primary decides whether to ask the user.
3. Split into units that each end in a checkable state. One change per PR or commit, with its own evidence. Order: failing test before the fix, subtraction before the reshape, baseline before the treatment.
4. For each unit list: dependencies, files owned, the one change, the observable result, and the verification command.
5. Mark which units are independent. Independent units may run in parallel with at most four subagents, non-overlapping owned files, or separate worktrees under `<repo>/.claude/worktrees/<name>`. Agree shared interfaces first and integrate dependent units in order.
6. Tests alone may not be enough: include a live check of the real surface where one exists.

Done when every unit has owner, files, result, and verification. Hand back the plan and what stays unproven; execution waits for the primary's dispatch.
