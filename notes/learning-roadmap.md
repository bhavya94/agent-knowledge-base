# Learning Roadmap — Evals → Post-Training

Goal: build concrete, public, end-to-end projects in evals and post-training.
Track A produces the judge that Track B depends on, so do A first.

## Track A — Evals and LLM judges
1. **Rubric** — pick a task; write a rubric with clear, scorable criteria and examples per level.
2. **Ground truth** — curate a labeled set (~200–500 items) with multiple annotators.
3. **Agreement** — Cohen's κ (2 raters), Fleiss' κ / Krippendorff's α (many raters, missing labels,
   ordinal scales); precision/recall/F1 of judge vs. consensus labels. Resolve disagreements; refine rubric.
4. **Judge prompt** — baseline hand-written judge, then optimize with DSPy (MIPROv2), GEPA
   (reflective prompt evolution), and Agentic Context Engineering (evolving playbooks).
5. **Tracking** — log every candidate prompt and its metrics to Comet ML / Opik (or W&B Weave, MLflow);
   select the judge on held-out agreement with humans, not on the optimization set.
6. **Agentic judges** — judges that call tools (code execution, retrieval, search) to verify claims;
   compare against the plain judge on cost and agreement.

Deliverable: a judge with reported κ/α/F1 against humans, plus the prompt-search history.

## Track B — Post-training with the judge
1. **Base** — small open model (Qwen or Liquid LFM); optionally warm-start by distilling from a
   frontier model.
2. **On-policy distillation** — sample from the student, score with the Track A judge.
3. **Self-correction** — below a score threshold, use the judge feedback plus a frontier model to
   produce a corrected response that passes the judge. Use a "council of models" (multiple
   frontier models propose; judge or vote selects).
4. **Train** — SFT on corrected data; then GRPO with the judge as the reward.
5. **Evaluate** — compare student vs. frontier on held-out judge evals; report cost per query and
   quality gap.

Open decisions: target task/domain, compute budget (local vs. rented GPUs), training stack
(TRL / Unsloth / verl).

## References
- [Shopify — Sidekick's continual learning loop](https://shopify.engineering/sidekicks-continual-learning-loop)
  — the end-to-end version of this roadmap. Rubric with anchored levels (completeness, execution,
  response quality, safety); 2 experts blind-score 25 samples, Cohen's κ (~0.2 = rubric is ambiguous);
  judge target = agree with humans as well as humans agree with each other. Calibrate with DSPy +
  GEPA/ACE; several small targeted judges rather than one. Validate judges by backtesting past A/B
  results and by deliberately degrading one behavior. Mine low-scoring production traces → frontier
  critic panel + arbiter writes repair instructions → replay → SFT on full reasoning traces → GRPO
  with judge reward; unfixable cases go to human experts. Prompt/harness first, weights only once
  that plateaus. ~$27M → ~$1M/yr serving cost.
- [ICML 2026 Expo — Model Optimization Flywheel (McNamara, Mazza-Anthony, Sun)](https://icml.cc/virtual/2026/75732)
  — talk version of the above; adds on-policy distillation and gist-token prompt compression.
- [Toloka — CV parser fine-tuned with Shopify's Tangle](https://toloka.ai/blog/fine-tuning-for-agentic-workflows-building-a-production-cv-parser-with-shopifys-tangle/)
  — structured extraction. Training labels synthetic (frontier models + automated validation); humans
  label only the holdout. Per-field multiset F1: small model 0.94 vs. frontier 0.93; ~$0.80 vs.
  $10–30 per 1k CVs. Tangle (open source) orchestrates ingest → fine-tune → eval.
