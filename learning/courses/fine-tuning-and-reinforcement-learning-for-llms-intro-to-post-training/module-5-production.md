# Module 5 — Production: Pipelines, Promotion, Infrastructure

**Course:** Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, Sharon Zhou, AMD) **Date:** 2026-10-15 **Verdict:** the module that separates a training run from a product. Promotion rules and the feedback flywheel are the keepers.

## What problem?
A model that trains well can still fail in production: it games an uncaught reward hack, drifts as user language shifts, gets promoted on a fluent-but-wrong output, or costs more to serve than the traffic justifies. Post-training does not end at the checkpoint.

## What idea?
**The DeepSeek R1 pipeline** is the capstone worked example. R1-Zero: RL only, GRPO with two rule-based verifiers (accuracy, think-tag format) on math/code, AIME accuracy 15.6% → 86.7%, emergent longer reasoning, reflection, and backtracking with no demonstrations and no reward model. Also: poor readability, mixed languages, verifier-bound domains only. Production R1 adds the scaffolding: cold-start long-CoT fine-tuning → RL with a language-consistency reward (auditable, single-language reasoning) → rejection-sampled synthetic reasoning data → combined ~800K-example fine-tune → final RL with a reward model. (Context: the v3 base cost roughly $5.3M in pre-training compute, remarkably cheap for its class.)

**Agents need production-first post-training.** Define required behaviors first (tool use, planning, coordination), then train for them. Teach reaching for tools over frozen parametric knowledge (a date-time tool instead of "remembering" today). Grade the behaviors: small reward for code that executes, large for code that executes correctly; negative reward for quitting, positive for escalating to a human. Harvest failures from limited deployment, then fine-tune on correct tool-call patterns and RL the graded outcomes.

**Promotion rules gate everything.** Freeze the test environment (RAG setup included) so metrics are reproducible. Slice it by behavior (search-API debugging, profile updates, math correctness, safety) and track pass rates per slice. Promotion contract: zero-regression slices where any dip is an automatic no-go (the course's example: output fluent, unit tests pass, reward model passes it, but a required version pin is missing, so no-go), safety under a strict cap, target capabilities must actually improve. Then staging: canary or shadow deployment on live traffic (at least 5,000 requests over 24 hours) compared against the production model, then production gates. A fine-tuned model is a frozen artifact, close to regular software; an RL model is less stable in deployment because not every reward hack has been caught.

**The data-feedback flywheel** closes the loop: production logs and feedback → cluster failures and successes → clean (filter aggressively, dedupe, bias checks, scrub PII) → convert to fine-tuning pairs and preference pairs → next experiments. The intervention ladder, matched to speed: prompt/template change (about a day) for hot fixes, RAG index update for stale knowledge, fine-tuning for unseen topics, RL for shifted preferences (sycophancy), fine-tuning plus RL for real capability gaps. Fine-tuning and RL cycles run about a week even with infrastructure ready.

**Monitoring** covers performance, cost, reliability: latency and token-usage distributions (which should shape training data representativeness), data drift, reward collapse (clickbait-style metric gaming), model forgetting, and infrastructure problems that silently degrade capability. Version control underpins rollback. A/B tests and side-by-side comparisons harvest winner data back into experimentation.

**Infrastructure** is concrete: fine-tuning tools (Hugging Face, LlamaFactory, Unsloth), RL tooling (plus Verl for distributed scale), serving (vLLM, SGLang). Start small on model size; quantize after training, for inference only (a 7B model at 4-bit is about 3.5 GB); distillation when you need teacher quality in a student footprint. Memory math decides hardware: GRPO on a 13B model runs roughly 170-190 GB VRAM (policy + frozen reference + small reward model + activations), about 2-4x the fine-tuning footprint. Capacity planning from QPS × tokens, with headroom and elastic scale-out.

**The production-ready checklist:** (1) reproducible config, same numbers on held-out sets within tolerance; (2) codified promotion rules and rollback conditions; (3) monitoring SLOs on behavioral and system metrics for the slices that matter; (4) a working feedback-to-data pipeline; (5) infrastructure for experiments and serving at target throughput, latency, and cost.

## Why it matters
- Promotion rules turn evals from dashboards into contracts. Zero-regression slices are the difference between "looks better" and "safe to ship."
- The intervention ladder is an incident-response skill: knowing which fix takes a day versus a week, and which failure class maps to which lever.

## How I'd use it
- **Roadmap Phase B:** GRPO memory math (170-190 GB for 13B) sets my hardware expectations before I scope any run.
- **My own projects:** the five-item checklist becomes the ship gate for anything I post-train.

## Open questions
- Canary thresholds (5,000 requests / 24h) are scale-dependent; a small-traffic product needs a different statistical basis. The principle holds, the numbers do not transfer blindly.
