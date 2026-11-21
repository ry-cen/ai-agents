# Handoff

Adapted from pstack poteto-mode/playbooks/pause-safely.md (MIT).

Use when stopping mid-task or when the user asks to pause. If the user said keep going, do not pause.

1. Stop at a safe boundary: finish the current atomic step or back it out. Start nothing new and stop any work you started.
2. Take no irreversible action to pause. Do not commit, push, or open a PR unless the assignment or user already allows it.
3. Write the checkpoint a cold-start agent can resume from: intent, progress and what is verified, current state (branch, dirty files), next steps, key files, gotchas, and open decisions.
4. Default location: your final response. Write a resume file only when the assignment permits writing one.
5. Do not read transcripts or session logs to rebuild state; use the repo, the plan, and the brief.

Done when the first action on resume is stated and everything on disk versus only in your head is distinguished (paths, no diff dumps).
