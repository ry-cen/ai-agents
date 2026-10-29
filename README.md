# ai-agents

Private storage for my AI agent files: agent definitions, prompts, skills, and related configuration.

This repo is the source of truth. The live config locations are symlinks into it, so edits here take effect immediately (and edits made by the tools land here).

| Repo path | Live location |
| --- | --- |
| `claude/CLAUDE.md`, `settings.json`, `statusline-command.sh`, `agents/`, `bin/`, `skills/`, `commands/`, `hooks/` | `~/.claude/` |
| `codex/AGENTS.md`, `config.toml`, `agents/`, `rules/`, `prompts/` | `~/.codex/` |
| `agents/skills/`, `agents/.skill-lock.json` | `~/.agents/` (shared skills) |

`~/.claude`, `~/.codex` and `~/.agents/*` point into `~/.t3/agents/` (managed by T3 Code). Only the entries above are symlinked from there into this repo; credentials, sessions, history, caches, plugins and databases stay in the real folders.

New files inside a linked folder (a new agent, skill, command, hook or prompt) land here automatically. To track a new top-level item, move it into the repo and symlink it back:

```sh
mv ~/.claude/<item> ~/projects/ai-agents/claude/<item>
ln -s ~/projects/ai-agents/claude/<item> ~/.claude/<item>
```

If a tool rewrites a linked file (such as `settings.json`) by replacing it, the link becomes a plain file and edits stop showing in `git status`. Move it back into the repo and relink it.
