# AI-Assisted Coding

## Philosophy
Karpathy school: writing code is agentic everywhere now; the skill is directing agents well —
how to prompt, which tools and connectors to use, how to structure context, and how to verify.
Karpathy's name for the professional version is **agentic engineering**: agents write the code, the human
orchestrates and oversees, with no compromise on quality.

## Lessons from Karpathy (2026)
- **How agents fail now** — conceptual errors, not syntax: wrong assumptions made silently, no clarifying
  questions, no trade-offs, no pushback, sycophancy, bloated code, and edits to unrelated code and comments.
  CLAUDE.md rules help but don't fix it, so review is the backstop. → `AGENTS.md` Agent rules, `reviewer`.
- **Leverage is declarative** — "Don't tell it what to do, give it success criteria and watch it go."
  Tests first; a naive correct version first, then optimize; loop with a browser. → Spec step, `experiment-loop`.
- **Setup** — a few Claude Code sessions plus an IDE to read the code. Agent swarms are premature for
  code you care about.
- **Atrophy** — writing code and reading code are different skills. Keep reading. → `explainer`.
- **Autonomous loops** — autoresearch: one editable file, a fixed budget per run, keep or discard by one
  metric. → `experiment-loop`.
- **Knowledge bases** — LLM Wiki: raw sources, an agent-maintained wiki, a schema file, and a lint pass.
  This repo follows that pattern. → `kb-lint`.
- **Understanding output** — about 80% ASD-STE100 writing → diagrams → interactive HTML → video. Custom,
  throwaway explainers now cost almost nothing. → `explainer`.
- **Visual work** — agents still can't audit visual or interactive output well, so a human checks it. → `demo`.

Sources: [notes from Claude coding (Jan 2026)](https://x.com/karpathy/status/2015883857489522876) ·
[agentic engineering (Feb 2026)](https://x.com/karpathy/status/2019137879310836075) ·
[autoresearch program.md (Mar 2026)](https://github.com/karpathy/autoresearch/blob/master/program.md) ·
[LLM Wiki (Apr 2026)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) ·
[understanding LLM output (Oct 2026)](https://x.com/karpathy/status/2105819303471976479) ·
community rules file based on the Jan post: [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
(no license, so not copied here).

## Setup
- Opus 5.5 for coding; GPT 5.6 Sol for most other tasks. Harness: Claude Code.
- This repo is the single source of agent notes, memory, and skills — updated continuously.

## Core skills (see `skills/`)
- **Code structure / DRY** — `conventions/code-structure.md`.
- **Pull requests** — `conventions/pull-requests.md`: small, focused, proven with screenshots.
- **explainer** — walks through what the agent wrote, with Mermaid diagrams and a decision log.
- **reviewer** — adversarial checks before anything is called done.
- **demo** — spins up the local server/UI/terminal, shows it working, captures screenshots/recordings.
- **learn-org-patterns** — mine the org's codebase and Senior/Staff review comments to learn how
  the team approaches problems, then apply that bar to new work.
- **experiment-loop** — autonomous keep-or-discard experiments against one fixed metric and budget.
- **kb-lint** — health check for this repo: index drift, broken links, contradictions, stale claims.

## Action items
- [x] Personal GitHub repo of agent notes and skills (this repo).
- [ ] Decide on higher-limit subscriptions (OpenAI / Anthropic / Meta) based on actual token usage.
- [ ] Run each skill on real work and refine it from what goes wrong.
