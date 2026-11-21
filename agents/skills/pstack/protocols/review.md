# Review

Adapted from pstack skills/interrogate, skills/blast-radius (MIT).

The primary dispatches an independent Sol reviewer per `~/.claude/CLAUDE.md` routing, with the exact checkout, base, head, intent, and verify commands. The reviewer is read-only (see `reviewer.md`): it returns findings, never patches, and runs only the verify commands it is given or the repo documents.

Reviewer approach:
1. Restate the intent in your own words from the brief; ask the primary if it is unclear.
2. Try to break the change: edge cases, error paths, callers outside the diff, formats other code reads, timing, and anything the diff does not spell out.
3. Find the one fact the change is safe because of, and say how far you got it: claimed, cited at `file:line`, walked step by step, or shown by an assigned or existing run. If unproven, write "unproven".
4. Report each finding with severity: **blocking** (breaks the intent), **should-fix** (real risk or defect), **nit** (optional). Every finding cites an exact `file:line` or the run evidence, plus how it breaks the intent.
5. List **dropped** items (checked and cleared, or unsupported by evidence) separately from **verified** findings. Omit style preferences and risks that need a future change to matter.

Done when each acceptance criterion is checked against the code and the verdict names the exact version reviewed. "No findings" is valid.
