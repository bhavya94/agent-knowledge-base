---
name: kb-changes-reach-sessions
description: Which knowledge-base changes reach Claude Code sessions that are already running, and how to reload the rest
type: reference
---

Checked against the Claude Code docs and seen in a session on 2026-10-11:
- **Skills** reload live. A running session finds new skills in `~/.claude/skills/` and uses an edited SKILL.md
  the next time it invokes the skill.
- **`AGENTS.md` and `memory/MEMORY.md`** (imported by `~/.claude/CLAUDE.md`) are read once, at session start.
  A running session keeps the old text until it restarts (`claude --resume` keeps the conversation) or runs `/clear`.
- **Plugins** installed with `claude plugin install` need `/reload-plugins` in each running session.
- **Subagents** spawned after a change get the current files.

After a change to `AGENTS.md` or a new plugin, tell the user which running sessions need a reload.
See [[kb-claude-code-only]].
