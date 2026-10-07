---
name: explainer
description: Write up what was just built — summary, Mermaid diagrams, and a decision log. Step 2 of the Build → Explainer → Reviewer → Demo workflow; run after implementing any non-trivial change.
---

# Explainer

Produce `docs/explainers/<YYYY-MM-DD>-<topic>.md` in the project (or the location the project already
uses). Audience: a senior engineer or stakeholder who wasn't in the session.

## Sections
1. **Summary** — 3–5 sentences: the problem, what was built, the outcome.
2. **How it works** — at least one Mermaid diagram of the real mechanism (data flow, sequence, or
   component diagram). Show the actual components and calls, not a generic box chart.
3. **Decision log** — table of `Decision | Options considered | Chosen | Why`. Include the trade-offs
   that were rejected and what would make us revisit.
4. **Cost & risk** — runtime/infra cost implications, failure modes, rollback path.
5. **Open questions** — anything the user must decide.

## Rules
- Every claim must be traceable to the code (cite `path:line`).
- Explain the *why*, not a changelog of edits.
