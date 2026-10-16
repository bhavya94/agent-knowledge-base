# Newsletter Digest

Learning-relevant items from The Batch (DeepLearning.AI) and TLDR AI, curated for the
evals → post-training track. Only items that go beyond the existing plan are listed.
Updated by the daily newsletter scan.

## 2026-10-16 - TLDR AI, "Muse Spark Open ✨, Microsoft’s 3T param model 🧠, d1-ultra 💡"

- **Muse Spark Open (Meta)** - 816B-parameter multimodal open-weight model, 42B active
  parameters, 1M-token context; designed for coding and long-horizon agentic tasks and
  able to run locally across two Apple M5 Ultra Mac Studios using MLX.
  https://research.meta.ai/blog/muse-spark-open
  Relevant: notable open-model release for the agentic track; too large for the Phase B
  student slot, but a reference point for open-weight agentic capability and local
  multi-machine inference.

- **"The Gradient Is a Covariance"** - RL, on-policy distillation, and SFT on near-policy
  data each change only a small fraction of parameters; the expected gradient is a
  covariance and the Fisher (a variance) caps the gradient for any reward, so what the
  update needs is a score centered under the sampling distribution, not on-policy
  sampling itself.
  Relevant: theory under the Phase B distillation decision; complements the NVIDIA
  on-policy distillation note from Oct 13 and the Thinking Machines reference in the
  roadmap sources.

- **"Mo' turns, mo' problems" (Ian Barber)** - agentic RL post-training in practice: one
  VM with a harness and a fresh model context per problem, tool calls during the run,
  and a single score at the end; even with a fixed harness, trajectories go off-policy
  because agents spawn subagents, make parallel tool calls, and compact large sessions.
  https://ianbarber.blog/2026/10/15/mo-turns-mo-problems/
  Relevant: RL-gyms and trajectory-eval tracks; a concrete off-policy caveat for the
  project 6 GRPO design and for scoring multi-turn agent runs.

- **d1-ultra (Liquid AI)** - multimodal decision model for complex real-world tasks;
  better-calibrated answers and higher accuracy than Jev 1.14; $0.042 per million input
  tokens on the Liquid API, with Vercel and OpenRouter access coming.
  https://www.liquid.ai/blog/d1-ultra
  Relevant: decision-models queue; a calibration-first successor to the d1 already
  referenced in project 2, and a new entry for the judge-swap cost and agreement
  comparison.

- **Anthropic expands independent evaluator access (METR)** - Anthropic is giving METR
  employee-like access to models, training information, safeguards, and other internal
  material so it can independently assess frontier-model risks and publish its
  conclusions.
  https://www.anthropic.com/news/an-update-on-independent-evaluators
  Relevant: evals-track infrastructure; the access arrangement the Oct 9 open letter
  asked labs to preserve, now granted by one lab, next to the Oct 12 evaluator-funding
  note.

- **Perplexity open-sources SPACE** - SPACE is the sandbox infrastructure behind
  Perplexity's Computer agent, now open source.
  https://www.perplexity.ai/hub/blog/open-sourcing-space
  Relevant: agent sandboxing for eval and RL environments; pairs with the Microsoft
  Quicksand note in project 5 as a reference for running tool-using agents safely.

## 2026-10-15 - The Batch, "Claude Haiku 5.5, Mistral Large 4, and Local Models for Mac and Windows"

- **Andrew Ng letter: verifiable tasks vs judgement tasks** - progress is much faster on
  verifiable tasks (code, math) because RL gyms can check outcomes automatically
  against a reward function; judgement tasks have no unambiguous ground truth, only
  better and worse answers, so gains need domain training data and laboriously crafted
  reward functions, and easy verifiable test sets make overall progress look better
  than it is.
  Relevant: core framing for Track A; why ground-truth curation and rubric design are
  the hard part of judging judgement tasks, and why RL-gym results transfer unevenly
  to them.

- **Claude Haiku 5.5 and Sonnet 5.5: reasoning effort is an eval variable** - Sonnet 5.5
  tops independent indices at max effort but scores lower on FrontierCode at max than
  at xhigh (46.2 percent vs 52.1 percent), and its cost per task varies more than 18x
  across reasoning levels; Sonnet 5.5 also ships classifiers that block reasoning
  extraction, with reasoning blocks bound to the account that generated them, to make
  distillation of its outputs harder.
  Relevant: agent-eval methodology for projects 4 and 6; sweep effort levels and report
  cost per task alongside accuracy, and note the new anti-distillation constraint on
  using frontier reasoning traces as SFT data.

- **Mistral Large 4: post-training recipe** - 1.05T-parameter MoE (52B active), weights
  promised by end of month; after pretraining, SFT then a single RL run mixing chat,
  science, safety, factual accuracy, and long-running tool use in shared environments
  (code sandboxes, web search, APIs), with rewards from unit tests, reward models,
  language model judges, and static code checks, updated asynchronously while parallel
  attempts are still running; 82 percent on CyberGym-E2E-AA, best among publicly
  available models.
  Relevant: post-training track; a frontier-scale reference recipe for reward sourcing
  in RL, and an open-weight release to watch for the comparison roster.

- **CausalMix: data mixing for fine-tuning, minus the guesswork** - causal method that
  separates a dataset's mixture effect (domain proportions) from its quality effect;
  built from 512 subsets of Tulu 3 fine-tuning Qwen2.5-0.5B, the mixture it selects
  transfers to Qwen2.5-7B and to Qwen3-4B on a distilled code and math set, beating Data
  Mixing Optimization on the selection benchmarks, with weaker results on a held-out
  Tulu 3 subset as the caveat.
  Relevant: SFT track; a principled way to set domain proportions for the project 6
  training set at small scale before committing GPU budget.

## 2026-10-15 - TLDR AI, "Jev 1.14, Grok Voice 3, RSI"

- **Google Harness²: recursive self-improvement loop (github.com/google-research/harness2)** -
  agents iteratively refine their prompts, tools, memory, and orchestration with no weight changes;
  carries evidence-backed lessons forward to improve future tasks.
  https://github.com/google-research/harness2
  Relevant: concrete reference implementation of the roadmap's "prompt/harness before weights"
  principle; an RSI counterpart to the UniEvo-VL self-improvement note on the Oct 5 list.
- **Agent observability on the Claude Platform (OpenTelemetry)** - send OTel traces from Claude
  Managed Agents, the Messages API, and Claude SDKs to any OTel tool; GenAI semantic conventions
  make Claude and other providers' data work in the same dashboards; use for debugging agents,
  improving agents with production data, and org-wide usage tracking.
  https://claude.com/resources/articles/agent-observability-on-the-claude-platform
  Relevant: trajectory-capture/observability tooling for the agentic-eval leg of Track A;
  pairs with CLiF from the Oct 14 scan.
- **Google Deep Review (agent document reviewer)** - agent AI system that provides rigorous feedback
  and technical verification on complex documents; started with CS papers, now multi-domain;
  PDF and text input with multi-file support coming.
  https://research.google/blog/analyzing-technical-documents-with-deep-review/
  Relevant: worked example of an agentic judge/verifier; a design reference for the Track A
  reviewer/judge agents.
- **"Routers Are a New AI Primitive" (vals.ai)** - independent comparison of AI routers: same
  fundamental design, different decision mechanisms; routers vs single models on quality and cost.
  https://www.vals.ai/blogs/routers-new-ai-primitive
  Relevant: feeds the model-tier-routing line in the harness design; a router quality-vs-cost datum.
- **Ling-3.1-flash (inclusionAI, HF)** - native hybrid reasoning model, 560B total / 25B active
  parameters, 1M-token context, on Hugging Face.
  https://huggingface.co/inclusionAI/Ling-3.1-flash
  Relevant: new open-model candidate for the Phase B comparison roster.

## 2026-10-15 - TLDR, "Inside GTA, Anthropic revenue jump, agentic verification"

- **"Agentic Verification" (addyo.substack)** - give agents a way to independently verify their work:
  end-to-end tests simulating real user flows as ground truth; property-based testing for
  invariants (what should never happen); fast deterministic tests so agents retry when the loop
  is slow or unreliable.
  https://addyo.substack.com/p/agentic-verification
  Relevant: test-design discipline for the agent-eval leg of Track A; property-based invariants
  complement the roadmap's judge degradation-test validation note.

## 2026-10-15 - TLDR Data, "Meta Puts Idle Compute to Work, GitHub Counts Stars Faster, Claude Dashboard Security"

- **Arize Phoenix (self-hosted open-source AI observability)** - OTel-based tracing, evaluating,
  and debugging of LLM apps; retrieval and response evaluations, versioned datasets, experiments,
  prompt testing and replay; framework- and provider-agnostic.
  https://github.com/Arize-ai/phoenix
  Relevant: eval/experiment tooling for Track A judge iteration; an open alternative to the
  CometML visualization line in the roadmap.
- **Airbnb CASTLE (CIKM 2026)** - jointly generates synthetic queries and relevance labels from
  de-identified booking sessions for cold-start NL search training; queries beat InPars/Promptagator
  baselines 9.2x on KL divergence to real queries; three human SMEs agreed with labels at 91-93%.
  https://airbnb.tech/ai-ml/castle-training-natural-language-search-before-the-first-real-query/
  Relevant: production-grade synthetic label-generation datum for the ground-truth-curation track;
  mirrors the roadmap's "training labels can be synthetic" method note.
- **Row-level security for Claude Dashboards via MCP (thedatavist)** - PoC enforcing access rules
  inside an MCP server (DuckDB backend) before data reaches Claude; one dashboard shows different
  results per user.
  https://thedatavist.substack.com/p/need-to-know-implementing-row-level
  Relevant: MCP track; security-enforcement pattern for tool-using agents.
- **XERJ (Apache-2.0 local search engine)** - Elasticsearch-compatible local engine that
  auto-indexes code, logs, PDFs, SQLite, and CSVs into typed datasets for agent retrieval and RAG;
  returns ranked passages with file and line locations; local by default.
  https://github.com/xerj-org/xerj
  Relevant: retrieval infra for agent RAG loops, adjacent to the PPLX/EmbeddingGemma retrieval note.

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

## 2026-10-13 — TLDR AI, "Muse Wonder, Maia 300, AI self-replication"

- **"When Do We Need On-Policy Distillation?" (NVIDIA Research)** — finds that distilling from
  offline rollouts generated by the initial student (Semi-OPD) often beats full on-policy
  distillation on accuracy and training efficiency; OPD only helps when teacher and student are
  highly aligned (high overlap ratio).
  https://research.nvidia.com/publication/2026-12_when-do-we-need-policy-distillation-distilling-offline-student-rollouts-often
  Relevant: sharpens the Phase B distillation plan; Semi-OPD is cheaper than full OPD and may be
  the better default for the Qwen/LiquidFM council-of-models loop.
- **Decision models cut agent LLM calls 29.6% (HuggingFace discuss)** — offloading step-completion
  checks and bounded decisions to Jev over 360 SOP-bench cases reduced Qwen agent LLM calls 29.6%,
  estimated API cost 26.6%, latency 19.7%.
  https://discuss.huggingface.co/t/offloading-bounded-decisions-cut-agent-llm-calls-by-29-6-on-360-sop-bench-cases/190420
  Relevant: concrete evidence for the reflective-qa decision-model swap on the roadmap; a Qwen-based
  reference number for his own cost/latency/agreement comparison.
- **Google Agent Skills: building, testing, and scaling agent skills** — engineering breakdown of
  keeping 15,000+ GitHub-star open-source agent skills reliable: skills with remote MCP tools,
  ADK authoring loops, and continuous evals for accuracy and token efficiency.
  https://cloud.google.com/blog/topics/developers-practitioners/behind-the-scenes-how-we-build-test-and-scale-google-agent-skills
  Relevant: MCP tool-use track plus continuous-eval methodology for agent skills; the ADK authoring
  loop is a prompt-optimization pattern worth borrowing for his Explainer/Reviewer/Demo skills.
- **"How Close Are AI Models to Self-Replication?" (Anthropic research)** — tested how close current
  models are to autonomously copying themselves across consumer hardware, from individual replication
  steps to full end-to-end execution.
  https://www.anthropic.com/research/self-replicating-ai
  Relevant: red-teaming topic; an end-to-end eval methodology for autonomous replication capability,
  complementing the Oct 9 deception-holdback note.
- **Muse Wonder and Wonder Full (Meta)** — Meta's first frontier-class models with stronger coding and
  "active memory" for retaining and synthesizing user-provided information.
  https://research.meta.ai/blog/muse-wonder
  Relevant: agent-memory track; another production active-memory design to compare against
  Devin Memory (Oct 6).
- **"The Expensive-Loop Problem" (LessWrong)** — argues most high-value work lives in expensive-loop
  domains (slow, costly feedback) where models must build theories, manage proxies, budget compute,
  and diagnose failures from scarce feedback; cheap-loop training does not teach this.
  https://www.lesswrong.com/posts/2mStxuNDMdaWdyHu6/the-expensive-loop-problem
  Relevant: RL-gyms topic; a framing for why simulated agent environments need realistic feedback
  scarcity to transfer to real agent work.
- **"Releasing AI-generated software" (Mark Seemann)** — argues for not reading AI-agent-written code
  and instead constraining it with unit tests and QA procedures; raises liability and accountability
  questions as AI-driven processes outperform human ones.
  https://blog.ploeh.dk/2026/10/12/releasing-ai-generated-software/
  Relevant: agentic AI development; a process-level quality strategy for his AI-coding workflow,
  in the Reviewer-skill territory.
- **AGENT-ENGINEER (open-source coding plugin)** — 11 skills, 4 subagents, and 5 hooks aimed at
  agent-engineering challenges for AI coding assistants.
  https://sarthakai.substack.com/p/a-coding-plugin-to-make-you-a-10x
  Relevant: agentic AI development; a concrete skills/subagents/hooks design to study for his own
  agent-notes skill set.

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
