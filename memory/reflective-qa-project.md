---
name: reflective-qa-project
description: reflective-qa — reflection agent on QASPER, approved 2026-10-09; milestones M0–M4, scope limits, and where it lives
type: project
---

`reflective-qa` is a reflection agent for grounded QA on QASPER (dev split, text-only questions), local at
`~/reflective-qa`. Approved 2026-10-09 as practice for Agentic AI Module 2. It starts roadmap Phases 0–1
early and stops at M4.

- **M0** setup + data loading + price check. **M1** baselines: BM25 evidence recall@k, one-shot answers
  (Sonnet 5.5 strong, Haiku 4.5 weak), closed-book run, code checks, answer-F1 by type.
  **M2** error analysis: Bhavya reads ~100 outputs, finds failure modes, labels Pass/Fail per mode.
  **M3** critic = code checks + one binary LLM check per M2 failure mode; writer revises on failed checks.
  **M4** experiment: one-shot vs self-critique vs code-feedback vs separate critic (± code feedback).
- Critic criteria come from M2 error analysis, never invented up front (roadmap: criteria drift).
- QASPER test split stays untouched. DSPy/GEPA, MLflow, tool-using critics and sentinels are deferred to
  later roadmap phases.
- Public repo: github.com/bhavya94/reflective-qa (created 2026-10-09, approved by Bhavya). PRs follow
  `conventions/pull-requests.md`; a milestone too big for one PR becomes a stack. M0 is on `main` as of
  2026-10-10: #2, then #5 (#3 and #4 had merged into their stack bases, so #5 re-landed them). #1 was closed
  as superseded. Branches auto-delete on merge. Next: M1, blocked on the model-access decision.
- Model access: Anthropic API key only. Never route project calls through Max subscription credentials
  (Anthropic's credential policy); `claude -p` is allowed but not reproducible. Key decision still open as of 2026-10-09.

**Why:** Turns course practice into the first slice of `learning/roadmap.md` without skipping the
roadmap's error-analysis-first order.
**How to apply:** When working in `~/reflective-qa` or planning roadmap Phases 0–3. See [[user-profile]],
[[no-employer-trade-secrets]].
