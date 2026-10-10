---
name: kb-claude-code-only
description: The knowledge base targets Claude Code only — don't wire it into Codex, Gemini, Cursor, or other agents
type: feedback
---

The knowledge base (AGENTS.md, memory, skills) only needs to work in Claude Code. Don't link it into
Codex, Gemini CLI, Cursor, or other tools, and don't rewrite it to be tool-neutral.

**Why:** On 2026-10-09 the user declined connecting Codex and Gemini: "it's okay if it just works for Claude."
**How to apply:** Claude-specific references (`~/.claude/skills`, subagents, Artifacts) are fine in skills
and AGENTS.md. Don't offer cross-tool setup again unless the user asks. See [[user-profile]].
