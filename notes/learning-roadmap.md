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


## Method notes (general practice, domain-neutral)
- Pilot the rubric with 2 annotators on ~25 items; low κ means the rubric is ambiguous — fix it before scaling.
- Judge target: agree with humans about as well as humans agree with each other.
- Prefer several small per-criterion judges over one monolithic judge.
- Validate a judge with degradation tests: deliberately worsen one behavior; only its criterion should drop.
- Training labels can be synthetic (frontier models + automated checks); humans label the held-out test set.
- Optimize prompt/harness first; move to weights only once that plateaus.
- SFT on full reasoning traces, not just final answers. Report cost per 1k queries alongside quality.
