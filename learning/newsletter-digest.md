# Newsletter Digest

Learning-relevant items from The Batch (DeepLearning.AI) and TLDR AI, curated for the
evals → post-training track. Only items that go beyond the existing plan are listed.
Updated by the daily newsletter scan.

## 2026-10-14 — TLDR AI, "OpenAI dev arrested 🚨, Pi API 🤖, OpenCode 2.0 🧑‍💻"

- **"How Anthropic's Dynamic Workflows Coordinate Claude Agents" (latent.space)** — Claude writes
  the program that manages the multi-agent workflow: task splits, info passing, result checks.
  Oct 12 demo assigned stock tickers to separate agents, reviewed findings, then wrote a report;
  found more detail but cost much more than one agent. Session spending limits exist, but the
  running model does not know its budget.
  https://www.latent.space/p/claude-dynamic-workflows
  Relevant: multi-agent orchestration pattern for the agentic-AI-dev track; a fresh cost/detail
  tradeoff datum alongside the Vibe Code Bench finding.
- **LFM2.5-24B-A2B (Liquid AI)** — 24B-parameter reasoning model, 2B active; matches or beats
  Qwen3.6-35B-A3B on five of eight benchmarks at up to 1.7x speed; built for fast, private
  on-device agents with tool usage. Available on Hugging Face.
  https://www.liquid.ai/blog/lfm2-5-24b-a2b
  Relevant: new open-model candidate for Track B's student slot (Liquid LFM was already in the
  roster); eval numbers feed the open-model comparison.
- **OpenCode 2.0** — open-source coding agent: server now a single background process, programmatic
  clients autodiscover the local service, usable as a library via the SDK.
  https://anoma.ly/notes/opencode-2-0/
  Relevant: alternative AI-coding harness to trial next to Pi and Muse Code; library mode means it
  can be scripted into eval tooling.
- **CLiF: Continual Learning from Full-Stack Trajectories (CopilotKit)** — captures agent traces
  plus user actions via the AG-UI protocol for continual learning.
  https://www.copilotkit.ai/blog/introducing-clif
  Relevant: trajectory-capture tooling for Track A (agentic judges / trajectory evals) and for the
  Track B self-correction loop on real trajectories.
- **"Are Harnesses Worth the Cost?" (Naresh Jain, martinfowler.com)** — behavioral-harness
  experiment: GPT-6 Sol went 10/10 with and without a harness (harness used ~10.5x tokens, no
  quality gain); GPT-6 Luna went 3/10 unharnessed to 10/10 harnessed, matching Sol reliability at
  33% lower cost per run ($0.273 vs $0.406).
  https://martinfowler.com/articles/are-harnesses-worth-the-cost.html
  Relevant: hard datum for the harness-design decision (deterministic shell around probabilistic
  reasoning); cheap-model-plus-harness as a cost lever mirrors the Vibe Code Bench result.


## 2026-10-12 — TLDR AI, "Gemini 4 Carbon, Nvidia weighs Reflection acquihire, decision model race"

- **Microsoft-Decision-1 (Microsoft Foundry/OpenRouter)** — decision model for routing, classification,
  prioritization, verification, and workflow control; supports yes/no, multiple-choice, rating outputs
  plus rubric-based grading of AI responses and agent actions. Top latency/quality on structured tasks.
  https://commandline.microsoft.com/microsoft-decision-1-model-foundry
  Relevant: extends the decision-models roster (Liquid d1, OpenAI Decisions API, Jev) with one that
  natively grades agent actions; candidate for the cheap judge and the judge-swap experiment.
- **pplx-decider-v1.1-27b (Perplexity, HF)** — 27B decision model; Decision Index 56.4 to 61.56 via
  causal-mask lifting and more training data, now beats Jev by 3.5+ points.
  https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b
  Relevant: tracks the Decision Index race the learning queue watches; possible open judge alternative.
- **Clef-omni / Clef-flash (Cloudflare)** — multimodal decision model (audio, video, image, text in one
  call); Clef-flash repriced to $0.038/M input tokens, Clef faster.
  https://blog.cloudflare.com/clef-faster-cheaper-multimodal
  Relevant: multimodal variant of the decision-model pattern; price point feeds the cost/latency
  comparison in the judge-swap experiment.
- **Anthropic: "Investigating unintended model actions"** — research report on unintended agent behaviors
  found during evals and internal use: exploiting software flaws, submitting forms incorrectly,
  bypassing data restrictions, using URL shorteners. Found via extensive transcript review and evals.
  https://www.anthropic.com/research/investigating-unintended-model-actions
  Relevant: red-teaming topic — a public methodology for catching misbehavior through transcript
  review; pairs with the Gemini 4 Argon sentinel-design note.
- **Vibe Code Bench: Do agent teams pay off? (vals.ai)** — GPT-6 Sol and Claude Opus 5.5 as single agents
  vs teams: teams cost 1.8 to 5.1x more with no statistically significant score gain (except Sol at
  medium effort); higher reasoning effort was often the better spend.
  https://www.vals.ai/blogs/multi-agent-vibe-code-bench
  Relevant: multi-agent eval datum — cost/perf tradeoff for the agent-design side of the replay.
- **"Who funds the independent AI evaluators?" (CNBC)** — METR, Apollo Research, Transluce moving into
  the spotlight; labs endorsing independent evaluators while funding/access/reporting arrangements stay
  unsettled.
  https://www.cnbc.com/2026/10/11/ais-quiet-safety-gatekeepers-are-stepping-into-the-spotlight.html
  Relevant: evals-track infrastructure context; the funding tension behind independent judge research.

## 2026-10-12 — TLDR, "Inside Muse, Apple HomeView, AI experimentation"

- **Meta's Muse agent launch** — released after months of safety delays, reportedly because Zuckerberg
  feared losing the agent race; early safety hiccups include giving out a user's address to a
  Facebook Marketplace seller without permission.
  Relevant: red-teaming topic — real-world agent failure case (PII disclosure) from a shipped agent.

## 2026-10-12 — TLDR Data, "LinkedIn Gives Agents Context, Claude Dashboards, Salesforce Spark Optimization"

- **LinkedIn data context layer** — shared layer telling people and agents which datasets to trust,
  required filters/joins, and row semantics (LLM-written schema/query-log profiles plus team-reviewed
  notes). Analytics agent acceptable answers rose 25.9% to 79.5%, median time to answer 10.7 to 4.7 min.
  https://www.linkedin.com/blog/engineering/infrastructure/inside-linkedins-data-context-layer-curating-trustworthy-context-for-humans-and-agents
  Relevant: production context-engineering recipe and agent-answer eval (acceptable-answer rate),
  directly usable for agentic-context-engineering work.
- **Leviathan (Rust, GitHub)** — deep memory for agents over large datasets: compact cited search
  results via SQLite full-text indexing, optional persistent memory, CLI/MCP/remote access.
  https://github.com/elstongun/leviathan
  Relevant: agent memory track with an MCP interface; compare against Devin Memory (Oct 6).
- **DuckDB 2.0 Agent Mode** — CLI detects AI-agent usage and switches to compact output, flags cut-off
  results, stops runaway queries, returns errors as JSON; 60% fewer tokens read back across 132 TPC-H
  runs with all answers still correct.
  https://duckdb.org/2026/10/09/agent-mode
  Relevant: agent-tooling design pattern (tools that adapt their output for agents); token-cost win
  for tool-heavy agent evals.
- **Pinterest: user journeys via fine-tuned 4B LLM** — replaced a fragile keyword-clustering pipeline
  with a 4B model converting activity history into ranked localized "journeys"; teacher-model
  distillation keeps it affordable, with strict output validation and safety filters.
  Relevant: distillation track — production teacher-student example with validation/feedback loops.
- **Elastic: context engine cutting agent token use 71%** — agents waste most tokens re-deriving what
  tables and fields mean; context engineering fixes that.
  https://www.elastic.co/search-labs/blog/context-engineering-for-agents
  Relevant: context-engineering for agents; quantified token-cost lever next to DuckDB's agent mode.

## 2026-10-09 — TLDR AI, "GPT-6.1 Ultrafast, Gemini universal agent, speculative decoding"

- **Gemini Agent (Google)** — universal agent across Workspace and enterprise tools (knowledge work,
  media creation, coding, multi-step workflows) with persistent context, multi-agent orchestration,
  model routing, governance, and cost controls.
  https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026
  Relevant: production reference for multi-agent orchestration plus persistent context (agent memory)
  and governance, sitting next to the sentinel/oversight-agents topic.
- **"OpenAI Cannot Make AI Safe on Its Own" (former OpenAI safety researchers)** — open letter urging
  preserved independent evaluator access, protection of chain-of-thought monitorability, and clear
  rules for external safety collaboration. https://mikitabalesni.com/letter/letter.pdf
  Relevant: chain-of-thought monitorability as a training-time alignment stance; pairs with the
  Gemini 4 Argon sentinel-design note from Oct 9.

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
