---
name: explainer
description: Write up what was just built — summary, Mermaid diagrams, and a decision log. Step 2 of the Build → Explainer → Reviewer → Demo workflow; run after implementing any non-trivial change.
---

# Explainer

Produce `~/agent-knowledge-base/projects/<repo>/explainers/<YYYY-MM-DD>-<topic>.md`, never in the project
repo (`conventions/pull-requests.md`). The knowledge base is public: for a private or employer repo, post the
explainer as a PR comment instead. Audience: a senior engineer or stakeholder who wasn't in the session.
Start with a line linking the PR and the commit the explainer describes.

## Sections
1. **Summary** — 3–5 sentences: the problem, what was built, the outcome.
2. **How it works** — at least one Mermaid diagram of the real mechanism (data flow, sequence, or
   component diagram). Show the actual components and calls, not a generic box chart.
3. **Decision log** — table of `Decision | Options considered | Chosen | Why`. Include the trade-offs
   that were rejected and what would make us revisit.
4. **Cost & risk** — runtime/infra cost implications, failure modes, rollback path.
5. **Open questions** — anything the user must decide.

## Format
Pick the richest format the change deserves. Each step is easier to understand than the one before
(Karpathy's ladder, `notes/ai-coding.md`):
1. **Text** — always, at about 80% of ASD-STE100 (see `AGENTS.md` → Communication).
2. **Diagrams** — always at least one Mermaid diagram (section 2).
3. **Interactive HTML** — for non-trivial changes or stakeholder audiences: one self-contained page next to
   the explainer (`<YYYY-MM-DD>-<topic>.html`) with clickable diagrams, before/after comparisons, or a
   walk-through of real data. The same public/private rule applies. Share it elsewhere only when the user asks.
4. **Video** — opt-in, for large design changes or teaching: a short Manim (3Blue1Brown-style) explainer
   with narration from a local text-to-speech model. Ask before spending the time.

## Rules
- Every claim must be traceable to the code. Draft with `path:line`; once the PR's commit is pushed, convert
  to commit-pinned links with `~/agent-knowledge-base/scripts/explainer-permalinks.py`.
- Link other PRs with full URLs: a bare `#4` in the knowledge base points at the knowledge base's own #4.
- Explain the *why*, not a changelog of edits.
