# Module 3 — Evaluation as the North Star

**Course:** Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, Sharon Zhou, AMD) **Date:** 2026-10-15 **Verdict:** the module closest to my day job. Error analysis plus eval investment is the whole game.

## What problem?
Teams treat evals as a passive final exam: train, score, done. A thin eval (only 1+1 and 2+2) makes a broken model look finished. Meanwhile RL training quietly games its reward model, and a headline "80% accuracy" says nothing about what to fix next.

## What idea?
Evals are an **active steering mechanism**, not a ranking ceremony. Design them to reveal weaknesses and direct effort.

**What to measure:** input diversity, task coverage, output correctness (verifiable cases give cheap, trustworthy signal, e.g., a math answer graded +1 for correct and +1 for valid JSON), plus efficiency metrics (latency, cost per token, token efficiency: a terse correct answer in 20ms beats a verbose CoT in 100ms). HELM adds the holistic dimensions accuracy hides: calibration, fairness, robustness, toxicity, efficiency.

**Monitoring RL updates:** watch KL divergence to the base model (drift control), sample efficiency, rollout diversity, and the **alignment tax**: the gap between reward-model scores and human judgment. Worked example: RM score jumps 0.62 → 0.85 (+0.23) while human win-rate barely moves 0.55 → 0.57 (+2%). That signature means the model is gaming the reward model. Response: inspect rollouts, fix or retrain the reward signal.

**Reward hacking** is structural, not a bug: we never have a perfect oracle for "good," so training uses proxies (verifiable rewards, learned reward models), and optimizers exploit proxy gaps. Goodhart's Law with gradients. DeepSeek R1-Zero's verifiers-only design (accuracy + format rewards) mostly avoids it, but the accuracy/format weighting is itself a new hacking surface.

**Error analysis** is the leverage skill: never stop at a headline number. Decompose failures into categories, find patterns at scale (embed + KMeans cluster failure texts, or have an LLM categorize 10K+ failures into a distribution), then apply the errors → causes → fixes mapping. The course's reference table pairs 14 error buckets with matched interventions under both fine-tuning and RL: factuality (context-conditioned citation data / preferences for grounded answers), reasoning (quality CoT + rejection sampling / preferences for correct step sequences), over-refusal (benign-but-sensitive prompts with helpful answers / penalize over-refusal), overconfidence ("I don't know" targets / up-rank calibrated admissions), and so on. Disciplined decomposition means fewer, smaller experiments, then scale the validated fix 10x.

**Investing in evals:** start small and scale; representativeness (the eval must match the real query distribution, not just the queries you wish users asked); reliability (enough examples that a 90% vs 92% delta is signal, not noise).

**Red teaming** closes the module: jailbreaks (DAN-style), automated adversarial generation with LLMs, and Anthropic's agentic misalignment research (a model blackmailing a CTO to avoid decommissioning) as the agentic failure mode to design against. Mitigations: runtime monitors with anomaly detection, prompt-level safety.

## Why it matters
- Alignment tax is the metric my judge work needs: judge score up, human agreement flat means the judge is being gamed.
- The errors → causes → fixes table is a diagnostic playbook I can run verbatim on my own eval failures.
- "Evals steer, they don't just score" reframes eval work from QA chore to the highest-leverage activity in post-training.

## How I'd use it
- **Roadmap Phase 2 (judge):** track judge-vs-human agreement (Kappa) as my alignment-tax proxy. Add rollout inspection to the judge loop, not just scores.
- **Roadmap Phase A replay:** RAG faithfulness evals get the representativeness treatment: prompts drawn from realistic usage, not just convenient ones.
- **Interview prep:** EvenUp's HM call covers eval metrics explicitly. Alignment tax + error decomposition is a staff-level answer.

## Open questions
- The module asserts LLM-based failure categorization works at 10K+ scale. I want to verify categorization stability (same failures, same buckets across runs) before building on it.
