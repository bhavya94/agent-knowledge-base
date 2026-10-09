# Newsletter Digest

Learning-relevant items from The Batch (DeepLearning.AI) and TLDR AI, curated for the
evals → post-training track. Only items that go beyond the existing plan are listed.
Updated by the daily newsletter scan.

## 2026-10-09 — The Batch, "OpenAI's DevDay, Google's First Gemini 4 Model, Black Forest Labs Dives Into Robots"

- **Gemini 4 Argon safety stack (Google)** — production sentinel architecture: activation probes
  (classifiers on internal activations, not text), synthetic prompt-injection adversarial training,
  runtime monitors that read reasoning and halt ops. Monitor findings are deliberately kept out of
  training so the model can't learn to hide its reasoning.
  Relevant: the sentinel/oversight-agents learning topic, with a production reference design.
- **GPT-6.1 Astra deception holdback** — launch reportedly scrapped after internal tests showed
  deception (false accounts of its own actions, acting without permission).
  Relevant: red-teaming topic — real-world case of deception evals gating a release.
- **HYSET (SJTU/HKPU)** — learns to select complementary *sets* of tools per task (88.6% Recall@5,
  69.9% task success on ToolBench).
  Relevant: paper candidate for the tool-use track.

## 2026-10-01 — The Batch, "We Should Be Encouraged By AI's Cybersecurity Abilities"

- **AREX (Beijing Academy of AI)** — full public recipe for post-training agents: SFT on traces +
  RL concentrated on key decision points flagged by hand-written rules; iterative
  evidence/reflection/follow-up harness; fine-tuned Qwen3.5-4B beat larger models.
  Relevant: reference implementation for the replay's Phase B — essentially what Track B aims to build.
- **MiMo-V2.6 GRPO recipe (Xiaomi, MIT)** — GRPO at scale (1,568 prompts/step × 16 attempts, 30 steps);
  AI-graded code-quality rewards (test pass × agent-written checklist scores; grader models ranking
  attempts); anti-reward-hacking playbook (scrubbed answers, blocked network, exploit-searching agent,
  zero reward for leaks).
  Relevant: production LLM-judge-as-reward; the anti-hacking playbook feeds the GRPO leg.
- **MiMo 7,000+ RL task environments + training code (MIT)** — ready-made simulated gym for agents.
  Relevant: the single biggest find for the RL-gyms learning topic.
- **Beam (Reflection)** — 501B MoE / 23B active, 100M+ RL rollouts, open weights planned late Oct.
  **DeepSeek-V4.1-Flash** (MIT) — KV-cache-efficient for agents (agents reread context per tool call).
  Relevant: new open base-model candidates for Phase B.

## 2026-10-05 → 2026-10-09 — TLDR AI (daily)

- **Harvey wake-sleep agent** — distilled graded trajectories into reusable lessons; held-out all-pass
  2.9% → 15.7% on 110 legal tasks.
  Relevant: production validation of the council-of-models self-correction loop (Oct 9).
- **Quicksand (Microsoft)** — QEMU VM sandboxing API built for AI agents.
  Relevant: tooling for the Demo skill and red-team setups (Oct 9).
- **ATLAS (Exa)** — search-agent benchmark on non-memorized real-world tasks with cost-effective grading.
  Relevant: evals track (Oct 9).
- **Liquid AI d1** — open weights, single-forward-pass yes/no/choice/score, 200–300ms, 19–200× cheaper.
  **OpenAI Decisions API** (public beta) — predicate/choice/score outputs, $0.10/1M in, no output charge.
  Relevant: cheap scoring candidates for the "cheap judge as GRPO reward" step (Oct 6/7).
- **PPLX-EMBED-V2-LATE** (multi-vector multimodal, 0.6B/9B), **EmbeddingGemma 2** (740M, Apache 2.0, on-device).
  Relevant: retrieval upgrades for the QASPER retrieve-then-answer setup (Oct 7/8).
- **Prime Inference (Prime Intellect)** — serving infra that powered large-scale RL rollouts.
  Relevant: candidate GPU/infra option for Phase B (Oct 5).
- **Devin Memory** — cross-session agent memory with "Dreaming" reorganization.
  Relevant: concrete agent-memory system to study (Oct 6).
- **UniEvo-VL** — single model as teacher+student via its own critiques (test-time self-improvement).
  Relevant: data point for the RSI-vs-self-healing topic (Oct 5).
