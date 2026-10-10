---
name: kb-lint
description: Health-check the agent knowledge base — find index drift, broken links, contradictions, stale claims, and duplicates in memory, notes, and skills, then fix or flag them. Use when the user asks to lint or clean up the knowledge base, or before a large reorganization.
---

# KB Lint

The lint pass from Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
pattern: an agent-maintained markdown store drifts unless something checks it. Run from `~/agent-knowledge-base`.

## Checks
1. **Index drift** — every file in `memory/` has one line in `memory/MEMORY.md`, and every line points to a
   file that exists. Every skill folder is listed in `README.md` and linked into `~/.claude/skills/`.
2. **Broken links** — every `[[slug]]` matches a memory's `name:`, and relative paths in markdown resolve.
3. **Contradictions** — two files that say different things about the same topic.
4. **Stale claims** — named files, commands, flags, models, or dates that are no longer true. Verify against
   the filesystem or the repo before flagging.
5. **Duplicates** — memories that cover the same fact.
6. **Gaps** — topics referenced in several places that have no note or memory of their own.
7. **Public-repo hygiene** — secrets, confidential employer details, or personal plans (`AGENTS.md`).

## Output
A table: `check | file | issue | action`, where action is `fixed` or `flagged`.
- Fix mechanical issues directly: index lines, links, exact duplicates.
- Flag judgment calls for the user: contradictions, gaps, and anything that would delete content.
- Remove hygiene problems at once and tell the user.

Then commit and push (`AGENTS.md` → Sync).
