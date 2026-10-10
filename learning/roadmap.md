# Learning Roadmap — Evals → Post-Training

Goal: build concrete, public, end-to-end projects in evals and post-training.
Track A produces the judge that Track B depends on, so do A first.

## Track A — Evals and LLM judges
1. **Error analysis** — generate outputs from the system being judged, read ~100, open-code what goes
   wrong, cluster into failure modes. Criteria come from observed outputs, not a priori ("criteria drift").
2. **Ground truth** — one trusted domain expert labels outputs Pass/Fail per failure mode (~50 Pass /
   ~50 Fail each, ≥30% negatives). Code checks first; LLM judges only for what code can't check.
3. **Agreement** — judge vs. expert: TPR/TNR (not raw accuracy) plus Cohen's κ; dev split to iterate,
   test split once. Ceiling = the expert's self-agreement (blind re-label). Fleiss' κ / α only if
   more raters join.
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
2. **SFT warm start** — frontier answers with reasoning, filtered by the judge (rejection sampling).
3. **Self-correction** — student answers below threshold are repaired by a frontier "council"
   (judge or vote selects) and fed back into SFT.
4. **GRPO** — reward = per-question checklist rubric graded by a cheap training judge (Rubrics as
   Rewards). The validated frontier judge is a separate gold judge, never the reward; watch for
   train-vs-gold divergence (reward hacking); consider rubric dropout.
   On-policy distillation (per-token teacher logprobs) needs an open-weight same-family teacher —
   stretch goal.
5. **Evaluate** — compare student vs. frontier on held-out judge evals; report cost per query and
   quality gap.

## Decisions (2026-10-07)
- **Task:** grounded QA over research papers — [QASPER](https://huggingface.co/datasets/allenai/qasper)
  (Dasigi et al., 2021; CC BY 4.0; 5,049 questions over 1,585 NLP papers; extractive / abstractive /
  yes-no / unanswerable answers with evidence; ~44% of questions have >1 human answer).
- **Input format:** retrieve-then-answer — question + top-k retrieved paragraphs (~2–3k tokens), not the
  full paper. Keeps GRPO affordable; faithfulness is judged against the provided context.
- **Annotation (revised 2026-10-09):** single domain expert (me) — standard practice, not a compromise.
  Binary Pass/Fail per failure mode on *model outputs*; judge reported as TPR/TNR + κ vs. my labels.
  Ceiling = my blind re-label agreement. QASPER human answers + evidence are references and the
  source for per-question checklist rubrics, not the items being labeled.
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
1. **Error analysis** — answers from frontier, small, and deliberately weak models; read and annotate
   ~100; cluster into failure modes (expected: unfaithful claims, wrong vs. evidence, incomplete,
   wrong answer type, "unanswerable" shortcut). Answer-F1 vs. gold reported alongside.
2. **Judges** — code checks first (format, unanswerable, quote-in-context, F1); one binary judge per
   remaining failure mode, ~100 labels each; baseline → MIPROv2 → GEPA → ACE scored on TPR/TNR;
   dev to iterate, test once; blind re-label for the ceiling; degradation tests.
3. **Agentic + cheap judge** — tool-using judge (evidence lookup) vs. plain on agreement and cost; a cheap
   judge for use as the GRPO reward. Open design decision: offline eval (scores completed outputs)
   vs live sentinel (watches the trajectory, can intervene) — same architecture, different trust model.
   Reflection is self-critique (correlated blind spots, optimizes quality); a sentinel is a separate
   watcher (optimizes safety: block/halt/escalate). Decide explicitly.
4. **Post-train** — baseline student; frontier-prompt baseline; closed-book (question-only) baseline for
   contamination; SFT on judge-filtered frontier answers with reasoning → council repair of student
   failures → GRPO with per-question checklist reward (rubrics built from QASPER references + evidence),
   cheap training judge, frontier gold judge for eval.
5. **Report** — student vs. frontier: judge scores, answer-F1, cost per 1k queries.

## Learning topics (queue)
- Alignment at training time — RLHF, DPO, constitutional AI; how alignment is handled during training.
- RL gyms — simulated environments for testing agents across scenarios (AutoGym, SkillGym).
- Red teaming agents — adversarial verification that an agent does what it's supposed to do.
- Recursive self-improvement vs self-healing — self-healing fixes outputs in a fixed capability
  envelope; RSI improves the improvement machinery itself.
- Sentinel / oversight agents — a monitor agent watching the main agent's trajectory for safety
  and policy compliance; catches deceptive or out-of-bounds actions.
- Decision models — fast, structured decisions inside agent loops (tool selection, completion checks,
  Pass/Fail scoring) via typed outputs in one pass, not open-ended generation. Hot as of Oct 2026:
  Jev (TypeSafe, $0.042/M in), StartLux-Decision (open-source, tops Decision Index 0.2.1),
  AutoTrust JEV/GEV family (Apache-2.0 adapters; GEV-26B-Decide escalates low-confidence calls to System 2).
  Learn: decision-head architectures, calibration, and where they beat frontier LLMs (high-volume typed
  decisions, ~40x cheaper, 3-5x faster) vs hard-coded rules. Implement: swap one high-frequency judge
  call in reflective-qa for a decision model; compare cost/latency/agreement.


## Method notes (general practice, domain-neutral)
- Error analysis before criteria; label outputs of the system being judged.
- One trusted expert labeling beats many outsourced labelers; low self-agreement means the criterion is ambiguous.
- Judge target: agree with the expert about as well as the expert agrees with themselves (TPR/TNR, not accuracy).
- Prefer several small binary per-failure-mode judges over one monolithic Likert judge.
- RL against a judge gets hacked: keep a separate gold judge and watch for divergence.
- Validate a judge with degradation tests: deliberately worsen one behavior; only its criterion should drop.
- Training labels can be synthetic (frontier models + automated checks); humans label the held-out test set.
- Optimize prompt/harness first; move to weights only once that plateaus.
- SFT on full reasoning traces, not just final answers. Report cost per 1k queries alongside quality.

## Sources (industry practice, 2026-10-09)
- [Shankar et al. — Who Validates the Validators? (criteria drift)](https://arxiv.org/pdf/2404.12272)
- [Husain — validate-evaluator (binary judges, TPR/TNR, single expert)](https://skills.sh/hamelsmu/evals-skills/validate-evaluator)
- [Databricks — Align LLM judges with human feedback](https://docs.databricks.com/gcp/en/mlflow3/genai/eval-monitor/align-judges)
- [Rubrics as Rewards (ICLR 2026)](https://arxiv.org/html/2507.17746v2)
- [Thinking Machines — On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/)
- [Rubric Dropout — reward hacking in rubric-as-reward RL](https://hub.baai.ac.cn/paper/b0256a30-0c5b-49c7-8c0d-4b07a9a80168)
