# Learning Roadmap — Learn by Building

Goal: learn evals, agents, and post-training by shipping small, public, end-to-end projects.
Each project is a **new public repo** with a one-page writeup of measured results.

## How this roadmap is fed
- **Courses:** one course a day is distilled into [`courses/`](courses/), in our own words (no slides,
  transcripts, or lab code).
- **Newsletters:** items worth experimenting with go to [`newsletter-digest.md`](newsletter-digest.md). Each new
  item is linked here in the same sync: under the project it changes, or in the learning-topics queue.
- **Projects:** each project below names its learning goal, its sources, and the repo it becomes.
  Pick fresh tasks and datasets per project; don't reuse an earlier project's dataset by default.
- Older notes refer to "Track A / Phase 2" (judges), "Phase 3" (harness), and "Track B / Phase B"
  (post-training). Those now map to projects 4, 5, and 6.

## Done
- **reflective-qa** ([repo](https://github.com/bhavya94/reflective-qa), 2026-10-09 to 2026-10-11) — reflection
  agent (writer + critic + one revise round) for grounded QA on QASPER. Result: no setup changed answer-F1
  measurably (all 95% CIs include zero). Critics fixed wrong "Unanswerable" answers, but rewording correct
  answers lost score, and the two cancelled out. Lesson: score each component, and use a metric that
  understands meaning, not word overlap.
- **metrics-from-scratch** ([repo](https://github.com/bhavya94/metrics-from-scratch), 2026-10-15 to
  2026-10-16): project 1 below. Classification, regression and agreement metrics in numpy, plus bootstrap
  CIs, Welch's t-test and power analysis. Every metric matches sklearn or scipy in tests (62 tests). The
  README shows when each number misleads, with seeded runs. Example: 99% accuracy at 8% recall when 1% of
  examples are positive, and an F1 gap that separate CIs miss but a paired bootstrap finds.

## Projects (queue)
Suggested order: 1 → 2 → 3 build the scoring and retrieval basics; 4 → 5 → 6 build on them.

1. **Metrics from scratch** — repo `metrics-from-scratch`. **Done 2026-10-16** (see Done).
   Implement in numpy and check against sklearn on a synthetic imbalanced set: precision/recall/F1,
   ROC-AUC and PR-AUC (own curve sweep), confusion matrix, MSE/MAE/R2; bootstrap 95% CIs, a two-sample
   t-test, power analysis for A/B sample size; Cohen's κ.
   Writeup: when each metric misleads (accuracy on imbalance, ROC-AUC vs PR-AUC).
   Learn: the statistics every later project reports.
   From the newsletters ([digest](newsletter-digest.md)): independent-evaluator funding (CNBC), as context
   for why reported metrics need intervals and stated methods.
2. **Extraction eval lab** — repo `extraction-eval-lab`.
   Structured extraction from fictional, synthetic documents into a strict JSON schema (entities, dates,
   amounts, relations). Compare (a) LLM extraction with schema validation and a repair loop vs (b) a small
   encoder with BIO token classification. Score exact match and per-field F1, plus a rubric judge; add
   adversarial cases (missing fields, ambiguous dates, conflicting values).
   Writeup: winner per field type, cost/latency/accuracy, failure taxonomy.
   Sources: Agentic AI (tool use, evals), crewAI (structured Pydantic outputs), post-training module 4
   (small seed set, error-driven counter-examples).
   From the newsletters ([digest](newsletter-digest.md)): Liquid AI d1 and the decision models
   (single-pass typed outputs) as a cheap third extractor or field validator; Agentic Verification (addyo) for
   the repair loop checking its own output; Ling-3.1-flash and LFM2.5-24B-A2B as low-cost model candidates.
3. **Embedding lab** — repo `embedding-lab`.
   On a few hundred docs: CLS vs mean pooling, cosine vs dot, scored by Recall@k and NDCG; FAISS ANN vs
   brute-force latency; contrastive fine-tune of a small sentence transformer on synthetic in-domain pairs
   to measure the domain-shift gap; sentence-window and auto-merging retrieval vs fixed chunks.
   Writeup: pooling/similarity table, domain-shift gap, dimension trade-offs (64/128/768).
   Sources: Advanced RAG (retrieval techniques, RAG triad).
   From the newsletters ([digest](newsletter-digest.md)): Airbnb CASTLE (synthetic queries plus
   relevance labels) to build the eval set; EmbeddingGemma 2 and PPLX-EMBED-V2-LATE (multi-vector) as models
   to compare; XERJ (local Elasticsearch-compatible engine) as the keyword baseline.
4. **Agent eval harness** — repo `agent-eval-harness`.
   Build a small tool-using agent (planner-executor, 3-4 tools), then evaluate it properly:
   - Trace it with OpenTelemetry (Phoenix or hand-rolled spans).
   - Evaluate at three levels: per skill, trajectory (convergence, GPA process judges), end to end.
     Use RAG-triad judges on retrieval steps.
   - Code checks first; one binary judge per failure mode, with discrete labels and explanations.
   - Error analysis before criteria: read ~100 traces, cluster failure modes, then write judges.
   - Calibrate judges against my own labels: TPR/TNR plus Cohen's κ, a dev split to iterate, a test split
     once, my blind re-label as the ceiling. Validate with degradation tests.
   - Optimize judge prompts: hand-written baseline → DSPy (MIPROv2) → GEPA. Log every candidate.
   - Try an agentic judge (tool calls to verify claims) against the plain judge on cost and agreement.
   Writeup: judge agreement with humans, where the agent fails, cost per eval run.
   Sources: Evaluating AI Agents, Building and Evaluating Data Agents (GPA, inline evals),
   Advanced RAG (triad), Agentic AI module 4, crewAI (agent design).
   From the newsletters ([digest](newsletter-digest.md)): Claude Platform OTel tracing and Arize
   Phoenix for traces; CLiF (full-stack trajectories); Google Deep Review as an agentic-judge reference;
   Agentic Verification; HYSET (choosing tool sets) for the router eval; decision models cutting agent LLM
   calls 29.6%, to test as a judge swap; vals.ai on routers and on agent teams (Vibe Code Bench); Exa ATLAS
   (cheap grading on non-memorized tasks); "Are Harnesses Worth the Cost?" (martinfowler.com) for the
   cost section of the writeup.
5. **Red-team harness** — repo `red-team-harness`.
   Point the project 4 agent (or a fresh tool-equipped one) at an automated red-teaming loop:
   hand-written injections with rule-based detection → a jailbreak prompt library → LLM-generated
   adversarial probes with an LLM safety judge. Run a scoped assessment: categories, threat actors,
   rounds, and a chained exploit attempt on an action with real effects (e.g. refund or delete).
   Add a sentinel that watches the trajectory and can block or escalate; compare it with no sentinel.
   Writeup: what got through, which layer caught what, and the safety judge's κ against my labels.
   Sources: Red Teaming LLM Applications, post-training module 3 (red teaming, misalignment).
   From the newsletters ([digest](newsletter-digest.md)): Gemini 4 Argon safety stack (a
   production sentinel design) for the sentinel; Anthropic's "Investigating unintended model actions" and
   self-replication studies for threat categories; the GPT-6.1 Astra deception holdback as a case study;
   Microsoft Quicksand (VM sandboxing for agents) to run attacks safely.
6. **Small post-training run** — repo `small-post-training`.
   Small open model (~1.7B, up to ~4B if the gap is large). LoRA SFT on judge-filtered frontier answers
   with reasoning (rejection sampling), then GRPO with verifiable rewards. Candidate eval set:
   LiveCodeBench filtered to post-model-cutoff problems, with train and eval slices disjoint from day one.
   A cheap training judge or verifier is the reward; a separate gold judge is used only for eval.
   Watch train-vs-gold divergence (reward hacking). Optional: a frontier "council" repairs failed student
   answers and feeds them back into SFT.
   Writeup: student vs frontier on held-out evals, cost per 1k queries, memory and GPU-hour actuals.
   Sources: Fine-tuning & RL for LLMs (all modules), Rubrics as Rewards, on-policy distillation.
   From the newsletters ([digest](newsletter-digest.md)): NVIDIA "When Do We Need On-Policy
   Distillation?" to decide distillation vs GRPO; MiMo-V2.6 GRPO recipe and its 7,000+ RL environments; AREX
   (public agent post-training recipe); Pinterest's fine-tuned 4B model as a small-model case study; Harvey
   wake-sleep (distilling graded trajectories into lessons) as a no-training baseline; LFM2.5-24B-A2B and
   Beam (open weights planned) as student or teacher candidates. CausalMix for choosing the SFT data mixture at small scale before scaling up; Mistral Large 4's mixed-task RL run (rewards from unit tests, reward models, and LLM judges) and "Mo' turns, mo' problems" (agent trajectories go off-policy via subagents, parallel tool calls, and compaction) for the GRPO leg.

## Standing decisions
- **Compute:** laptop (M1, 8 GB) for orchestration, labeling, and API calls. Rented single GPU for
  training and student inference.
- **Model access:** I hold API keys in a git-ignored `.env`; agents never handle them. Approve cost before
  any paid run; each repo sets a dollar cap.
- **Tooling order (2026-10-12):** DSPy first; it is a program optimizer, not an agent framework. LangGraph
  only when loops stop being fixed pipelines (retries, conditional edges, parallel branches).
- **Stack (proposed):** DSPy (MIPROv2, GEPA) for judges; MLflow or Arize Phoenix for tracking and traces;
  TRL + vLLM for SFT/GRPO (Unsloth if memory-tight).
- **Models / tooling (2026-10-13):** trialing Muse Code as a cheaper daily driver; the switch waits on a
  side-by-side on a real task. Muse Wonder (API) joins Sonnet/Haiku 5.5 as a judge candidate;
  cost/latency/agreement decide.
- **Courses:** auditing is free (videos only); certificates don't matter. Distilled so far: see [`courses/`](courses/).
- **Course queue (2026-10-17):** 7 of 13 distilled. The 6 priority courses were all distilled on 2026-10-15 (crewAI multi-agent systems, Evaluating AI Agents, Advanced RAG, Fine-tuning and RL for LLMs, Building and Evaluating Data Agents, Red Teaming LLM Applications), and Agentic AI followed on 2026-10-16. Post-training of LLMs is next: extraction complete on 2026-10-17 (all 9 video lessons, 3 notebooks), awaiting distillation via PR; lessons 5, 7 and 9 were covered from chapter structures after a transcript stall, flagged in that course README. Then, one per day: Finetuning Large Language Models, Build and Train an LLM with JAX, Spec-Driven Development with Coding Agents, ChatGPT Prompt Engineering for Developers, and Transformers in Practice (added 2026-10-15, last in the queue).

## Learning topics (queue)
- Alignment at training time — RLHF, DPO, constitutional AI; how alignment is handled during training.
- RL gyms — simulated environments for testing agents across scenarios (AutoGym, SkillGym).
- Recursive self-improvement vs self-healing — self-healing fixes outputs in a fixed capability
  envelope; RSI improves the improvement machinery itself. Reference loop: Google Harness²
  (github.com/google-research/harness2) — agents refine prompts, tools, memory, and orchestration with
  evidence carried across tasks, no weight changes.
- Decision models — fast, structured decisions inside agent loops (tool selection, completion checks,
  Pass/Fail scoring) via typed outputs in one pass, not open-ended generation. Hot as of Oct 2026:
  Jev (TypeSafe, $0.042/M in), StartLux-Decision (open-source, tops Decision Index 0.2.1),
  AutoTrust JEV/GEV family (Apache-2.0 adapters; GEV-26B-Decide escalates low-confidence calls to System 2).
  Learn: decision-head architectures, calibration, and where they beat frontier LLMs (high-volume typed
  decisions, ~40x cheaper, 3-5x faster) vs hard-coded rules. Try: swap one high-frequency judge call in
  project 4 for a decision model; compare cost/latency/agreement. Phase one is harness work (model-tier
  routing, low-confidence escalation, cost-latency budgets), no training needed.
- How GPT actually works (foundations, do early) — context window, transformer architecture, the
  attention mechanism, the role of probability (next-token prediction; sampling via temperature/top-p/top-k),
  KV cache (what it is, how it makes decoding fast, why prompt caching and prefix matching behave the way
  they do). Then extend to decision models: how typed/non-autoregressive outputs differ from
  autoregressive generation, decision heads, and why the same transformer backbone serves both.
- REA — Reverse Engineer Anything ([morluto/rea](https://github.com/morluto/rea), [rea.tools](https://rea.tools))
  — open-source MCP server + CLI giving coding agents decompiler access (Ghidra/Hopper/IDA/JADX
  backends; analysis runs locally, nothing uploaded; native paths are read-only). Output format is
  evidence-first: evidence, limitations, unknowns — eval-harness thinking applied to agent tool use.
  Only point it at software you own or are licensed to analyze. Tinker: run analyze-javascript-application
  against an Electron app; probe where agent conclusions hold vs. need verification.
- Agent memory and harness engineering (from the newsletters) — Devin Memory (cross-session memory with
  "Dreaming" reorganization), Leviathan (cited search over large datasets), Elastic's context engine (71% fewer
  agent tokens), LinkedIn's data context layer, DuckDB 2.0 agent mode, Anthropic's dynamic workflows, Google
  Agent Skills, AGENT-ENGINEER, UniEvo-VL (one model as teacher and student). Fold into project 4 when its
  agent needs memory or context management. Also read: "The Expensive-Loop Problem" (LessWrong) and
  "Releasing AI-generated software" (Mark Seemann), on where agents pay off and how to trust their code.

## Method notes (general practice, domain-neutral)
- Error analysis before criteria; label outputs of the system being judged ("criteria drift").
- One trusted expert labeling beats many outsourced labelers; low self-agreement means the criterion is ambiguous.
- Judge target: agree with the expert about as well as the expert agrees with themselves (TPR/TNR, not accuracy).
- Prefer several small binary per-failure-mode judges over one monolithic Likert judge.
- RL against a judge gets hacked: keep a separate gold judge and watch for divergence.
- Validate a judge with degradation tests: deliberately worsen one behavior; only its criterion should drop.
- Training labels can be synthetic (frontier models + automated checks); humans label the held-out test set.
- Optimize prompt/harness first; move to weights only once that plateaus.
- SFT on full reasoning traces, not just final answers. Report cost per 1k queries alongside quality.
- Score each component, not just the end-to-end answer (the reflective-qa lesson).
- Hands-on labs (code-lab skill): I drive, the agent navigates one step per message.
  Teach top-down (main flow end-to-end first, then details); scope a lab to one PR.
  Exploration is by breakpoint() and print in the terminal, not the IDE debugger UI (adopted 2026-10-16).

## Sources (industry practice, 2026-10-09)
- [Shankar et al. — Who Validates the Validators? (criteria drift)](https://arxiv.org/pdf/2404.12272)
- [Husain — validate-evaluator (binary judges, TPR/TNR, single expert)](https://skills.sh/hamelsmu/evals-skills/validate-evaluator)
- [Databricks — Align LLM judges with human feedback](https://docs.databricks.com/gcp/en/mlflow3/genai/eval-monitor/align-judges)
- [Rubrics as Rewards (ICLR 2026)](https://arxiv.org/html/2507.17746v2)
- [Thinking Machines — On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/)
- [Rubric Dropout — reward hacking in rubric-as-reward RL](https://hub.baai.ac.cn/paper/b0256a30-0c5b-49c7-8c0d-4b07a9a80168)
- [Surge AI — sudo L7](https://surgehq.ai/blog/sudo-l7) — staff-level coding-agent benchmark: expert rubrics across 8 behavior dimensions, grader models with executable checks as evidence; tasks from private production repos.
