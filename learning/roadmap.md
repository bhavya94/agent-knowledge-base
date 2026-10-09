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

## Decisions (2026-10-07)
- **Task:** grounded QA over research papers — [QASPER](https://huggingface.co/datasets/allenai/qasper)
  (Dasigi et al., 2021; CC BY 4.0; 5,049 questions over 1,585 NLP papers; extractive / abstractive /
  yes-no / unanswerable answers with evidence; ~44% of questions have >1 human answer).
- **Input format:** retrieve-then-answer — question + top-k retrieved paragraphs (~2–3k tokens), not the
  full paper. Keeps GRPO affordable; faithfulness is judged against the provided context.
- **Annotation:** single annotator (me). Reliability = intra-rater κ (re-label the pilot blind after ≥1 week);
  human-vs-human reference from QASPER's multi-answer questions; other LLM judges reported as
  non-human raters. Judge target: agree with me about as well as I agree with myself.
- **Compute:** laptop (M1, 8 GB) for orchestration, labeling, and API calls only. Rented single GPU for
  student inference, SFT, and GRPO.
- **Stack (proposed):** DSPy (MIPROv2, GEPA) for the judge; MLflow for tracking; TRL + vLLM for SFT/GRPO
  (Unsloth if memory-tight); small open student (~1.7B, step up to ~4B if the gap is large).
- **Phase B eval set (2026-10-09):** LiveCodeBench filtered to post-model-cutoff problems —
  unit-test-verifiable for clean GRPO rewards and contamination-resistant via time-sliced releases.
  Paired with QASPER: QASPER covers the judge track (faithfulness needs a judge), LiveCodeBench
  covers the verifiable training track. Train and eval slices stay disjoint from day one.

## Plan
- **Prerequisite (started 2026-10-08):** DeepLearning.AI coursework before Phase 0.
  Ranked shortlist (~20–25h): 1. Agentic AI (Ng) → 2. DSPy → 3. Evaluating AI Agents →
  4. Fine-tuning & RL for LLMs → 5. GRPO → 6. Post-training of LLMs → 7. MCP → 8. LangGraph.
  Courses #2–#3 feed Phase A; #4–#6 feed Phase B. Agentic AI modules 1–2 done, notes in
  learning/courses/agentic-ai/. Log takeaways that change the plan here.
0. **Scope** — verify current small-model options and GPU/API prices; task spec; retrieval baseline.
1. **Rubric + labels** — rubric: faithfulness, correctness vs. gold, completeness, handling of unanswerable.
   Generate answers from frontier, small, and deliberately weak models. Pilot 25, re-label later for κ,
   refine; then ~200-item held-out test set. Deterministic answer-F1 vs. gold reported alongside.
2. **Judge** — per-criterion judges; baseline → MIPROv2 → GEPA → ACE; select on held-out agreement;
   degradation tests.
3. **Agentic + cheap judge** — tool-using judge (evidence lookup) vs. plain on agreement and cost; a cheap
   judge for use as the GRPO reward. Open design decision: offline eval (scores completed outputs)
   vs live sentinel (watches the trajectory, can intervene) — same architecture, different trust model.
   Reflection is self-critique (correlated blind spots, optimizes quality); a sentinel is a separate
   watcher (optimizes safety: block/halt/escalate). Decide explicitly.
4. **Post-train** — baseline student; frontier-prompt baseline; on-policy sampling → critic-panel repair →
   SFT on reasoning traces → GRPO with judge reward.
5. **Report** — student vs. frontier: judge scores, answer-F1, cost per 1k queries.

## Learning topics (queue)
- Alignment at training time — RLHF, DPO, constitutional AI; how alignment is handled during training.
- RL gyms — simulated environments for testing agents across scenarios (AutoGym, SkillGym).
- Red teaming agents — adversarial verification that an agent does what it's supposed to do.
- Recursive self-improvement vs self-healing — self-healing fixes outputs in a fixed capability
  envelope; RSI improves the improvement machinery itself.
- Sentinel / oversight agents — a monitor agent watching the main agent's trajectory for safety
  and policy compliance; catches deceptive or out-of-bounds actions.


## Method notes (general practice, domain-neutral)
- Pilot the rubric with 2 annotators on ~25 items; low κ means the rubric is ambiguous — fix it before scaling.
- Judge target: agree with humans about as well as humans agree with each other.
- Prefer several small per-criterion judges over one monolithic judge.
- Validate a judge with degradation tests: deliberately worsen one behavior; only its criterion should drop.
- Training labels can be synthetic (frontier models + automated checks); humans label the held-out test set.
- Optimize prompt/harness first; move to weights only once that plateaus.
- SFT on full reasoning traces, not just final answers. Report cost per 1k queries alongside quality.
