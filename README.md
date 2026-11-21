# ai-agents

Private storage for my AI agent files: agent definitions, prompts, skills, and related configuration.

This repo is the source of truth. The live config locations are symlinks into it, so edits here take effect immediately (and edits made by the tools land here).

| Repo path | Live location |
| --- | --- |
| `claude/CLAUDE.md`, `statusline-command.sh`, `agents/`, `bin/`, `skills/`, `commands/`, `hooks/` | `~/.claude/` |
| `codex/AGENTS.md`, `rules/`, `prompts/` | `~/.codex/` |
| `agents/skills/`, `agents/.skill-lock.json` | `~/.agents/` (shared skills) |

The repo can be cloned anywhere; `$AI_AGENTS` below stands for the clone path on each machine. Only the entries above are symlinked into the repo. Credentials, sessions, history, caches, plugins and databases stay local, along with machine-specific config (`~/.claude/settings.json`, `~/.codex/config.toml`), which is gitignored because each machine's setup differs. Where `~/.claude`, `~/.codex` and `~/.agents` themselves live (real folders, or links into another tool's managed directory) is up to each machine.

To set up a machine, back up the existing entries, then link each one:

```sh
AI_AGENTS=~/path/to/ai-agents
for i in CLAUDE.md statusline-command.sh agents bin skills commands hooks; do ln -s "$AI_AGENTS/claude/$i" ~/.claude/$i; done
for i in AGENTS.md rules prompts; do ln -s "$AI_AGENTS/codex/$i" ~/.codex/$i; done
for i in skills .skill-lock.json; do ln -s "$AI_AGENTS/agents/$i" ~/.agents/$i; done
```

New files inside a linked folder (a new agent, skill, command, hook or prompt) land here automatically. To track a new top-level item, move it into the repo and symlink it back:

```sh
mv ~/.claude/<item> "$AI_AGENTS/claude/<item>"
ln -s "$AI_AGENTS/claude/<item>" ~/.claude/<item>
```

If a tool rewrites a linked file (such as `CLAUDE.md`) by replacing it, the link becomes a plain file and edits stop showing in `git status`. Move it back into the repo and relink it.

The pstack workflow skill lives in `agents/skills/pstack` and is linked into Claude via `claude/skills/pstack` (Codex finds it through `~/.agents/skills`). Opt out with "no pstack" or "pstack off". To roll back, revert the whole pstack change (all its commits), or remove `agents/skills/pstack`, the `claude/skills/pstack` symlink, and the pstack sections in `claude/CLAUDE.md` and `codex/AGENTS.md` together; live sessions pick changes up only after the live checkout is updated.
