---
name: reflective-qa-project
description: reflective-qa — reflection agent on QASPER, approved 2026-10-09; milestones M0–M4, scope limits, and where it lives
type: project
---

`reflective-qa` is a reflection agent for grounded QA on QASPER (dev split, text-only questions), local at
`~/reflective-qa`. Approved 2026-10-09 as practice for Agentic AI Module 2. It starts roadmap Phases 0–1
early and stops at M4.

- **M0** setup + data loading + price check. **M1** baselines: BM25 evidence recall@k, one-shot answers
  (Sonnet 5.5 strong, Haiku 5.5 weak), closed-book run, code checks, answer-F1 by type.
  Models (decided 2026-10-10): Sonnet 5.5 strong writer and separate critic; Haiku 5.5 weak writer, made weak
  with fewer paragraphs (k = 5). Retrieval: BM25, k = 20 (PR #6).
  **M2** error analysis: Bhavya reads ~100 outputs, finds failure modes, labels Pass/Fail per mode.
  **M3** critic = code checks + one binary LLM check per M2 failure mode; writer revises on failed checks.
  **M4** experiment: one-shot vs self-critique vs code-feedback vs separate critic (± code feedback).
- Critic criteria come from M2 error analysis, never invented up front (roadmap: criteria drift).
- QASPER test split stays untouched. DSPy/GEPA, MLflow, tool-using critics and sentinels are deferred to
  later roadmap phases.
- Public repo: github.com/bhavya94/reflective-qa (created 2026-10-09, approved by Bhavya). PRs follow
  `conventions/pull-requests.md`; a milestone too big for one PR becomes a stack. M0 is on `main` as of
  2026-10-10: #2, then #5 (#3 and #4 had merged into their stack bases, so #5 re-landed them). #1 was closed
  as superseded. Branches auto-delete on merge. M1 code (retrieval #6, scoring #7, answering #8, batch runner #9) is on
  `main` as of 2026-10-11, 36 tests. Budget: $20 of API credits for M1–M4, so runs use a seeded 200-question
  sample and `baselines run` needs `--max-dollars`. M1 baselines ran 2026-10-11 (PR #11): Sonnet 5.5 k=20 answer-F1
  0.512, closed-book 0.274, Haiku 5.5 k=5 0.425. Spent $1.25 of $20 (track with `report` / row `cost`). Pilot found
  a bracketed-citation bug (fixed, #10). Leads for M2: yes/no over-abstention, Haiku over-abstains (29.5%), long answers.
  Next: M2 error analysis by Bhavya, with a labeling tool.
- Model access: Anthropic API key, decided by Bhavya 2026-10-10. Bhavya puts the key in `~/reflective-qa/.env`
  (git-ignored); agents never handle or print it. Never route project calls through Max subscription credentials
  (Anthropic's credential policy). Get Bhavya's approval on estimated cost before any paid run.

**Why:** Turns course practice into the first slice of `learning/roadmap.md` without skipping the
roadmap's error-analysis-first order.
**How to apply:** When working in `~/reflective-qa` or planning roadmap Phases 0–3. See [[user-profile]],
[[no-employer-trade-secrets]].
