# Verification

Adapted from pstack skills/principle-prove-it-works/SKILL.md, skills/principle-test-behavior-not-implementation/SKILL.md, skills/principle-sequence-verifiable-units/SKILL.md (MIT).

1. Check the real thing: run the feature, read the actual value, inspect the actual diff. Proxies (file mtimes, self-reports, cached output, "it compiles") do not count. When a check fails, suspect the observation method before the system.
2. Work in verifiable units: known-good state, one change, run the check, proceed. Do not advance on a red unit, even when a tool made the edits.
3. Tests assert what users of the code can observe (return values, errors, readable state, outside effects). A good test fails when behavior breaks and survives an internal refactor. Do not pin private helpers or call order.
4. Script the check when you can, so the comparison reruns identically. Report the command and its actual output.
5. Reuse a passing result while its inputs are unchanged; rerun after changes or failures.
6. Verification checkpoints are independent of commits, pushes, and merges. Passing checks never authorize any of those; existing approval rules govern them.

Done when every acceptance criterion has a command or direct observation with its recorded result, and what was not verified is stated.
