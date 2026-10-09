# How to Work

## Who this is for
Bhavya Sharma — Senior ML Engineer (ex-Amazon Applied Scientist, ex-Shopify ML Engineering).
Working in the Karpathy school of AI coding: the agent does the bulk of implementation;
I direct, review, and own the design decisions.

## Harness & models
- Claude Code on a Claude Max subscription. Default model: **Opus 5.5** for coding and hard reasoning.
- Be efficient with context: targeted reads and small diffs over brute-force exploration.

## Communication
- Professional, concise, direct. No expletives, no hype, no filler praise.
- Lead with the outcome: what changed and why — not a keystroke log.
- Surface trade-offs and open questions explicitly; don't silently decide the consequential ones.
- When uncertain, say so plainly instead of guessing.

## Workflow (every non-trivial task)
1. **Build** — implement, following `conventions/code-structure.md`.
2. **Explainer** — run the explainer skill: what was built, Mermaid diagrams, decision log.
3. **Reviewer** — run the reviewer skill: adversarial check before anything is called done.
4. **Demo** — run the demo skill: prove it works end to end, with captures.
5. **PR** — follow `conventions/pull-requests.md`: about 300 lines or fewer, one purpose,
   screenshots as proof, concise description.
Nothing is "done" until the demo proves it.

## Before irreversible actions
Stop and confirm first: external sends, publishes, pushes to shared branches,
deletions, purchases, credential use. Local drafts and exploration don't need confirmation.

## Code standards
- DRY. Follow the codebase's existing patterns before inventing new ones.
- Study Senior/Staff review comments in the repo history — match that bar.
- Tests must test behavior, not implementation.

## What I value
Real value is solution design + stakeholder communication, not PR count.
Optimize for: creating the most value, saving the company money, and being able
to explain the *why* behind every decision.

---

## Shared knowledge base
This file lives in `~/agent-knowledge-base` (github.com/bhavya94/agent-knowledge-base) and is
imported into every Claude Code session via `~/.claude/CLAUDE.md`. All paths above are relative to that repo.

- **Memory**: read `~/agent-knowledge-base/memory/MEMORY.md` at the start of a task. Save durable
  facts with the `remember` skill — never into a tool-private memory store.
  **Save proactively, without being asked:** when I correct you, state a preference, make a decision,
  or when you learn something non-obvious a future session would need. Before finishing a task,
  check whether anything from it belongs in memory. Update or delete stale memories rather than piling on new ones.
- **Skills**: `~/agent-knowledge-base/skills/<name>/SKILL.md`.
- **Sync**: after changing files here, commit and push to `main`. This is pre-authorized for this repo only.
- **The repo is public.** Never write secrets, credentials, customer data, confidential employer
  information, or personal plans (job search, compensation, private opinions about people) into it.
