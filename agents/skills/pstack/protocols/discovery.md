# Discovery

Adapted from pstack skills/how, skills/why, poteto-mode/playbooks/investigation.md (MIT).

Read-only. Produce a cited answer, not a change.

1. Restate the question in one line. If the scope is ambiguous, state your interpretation and proceed; the user can redirect.
2. Stay inside the repository (and the paths the brief names). No wide filesystem crawling; use search before reading whole files.
3. For "how does X work": trace the actual flow from entry point to effect. Name the files, the owners of state, and where a change would land. Cite `file:line` for every claim.
4. For "why": read the commits and PR discussion that introduced the code and each later change. Quote what the authors wrote, mark your own inferences as inferences, and say what the record does not answer.
5. Report: overview, key concepts, where things live, gotchas, and open questions. Push back if the question's premise is wrong.

Done when each claim has a citation or is labeled as inference, and the open questions are listed. If the work continues into code, hand the findings to the next stage as a context pack (paths, interfaces, tests, constraints).
