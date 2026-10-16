# Fine-tuning & RL for LLMs: Intro to Post-training

**Source:** DeepLearning.AI long course, taught by Sharon Zhou (AMD), opening conversation with Andrew Ng. **Date distilled:** 2026-10-15. **Status:** enrolled, read-only extraction. No account changes made; graded labs were not started (they sit behind the paid plan and the read-only constraint).

**Course page:** https://learn.deeplearning.ai/courses/fine-tuning-and-rl-for-llms-intro-to-post-training

## Verdict
The flagship of the six-course distillation set: SFT, rejection sampling, judge/reward signals, GRPO. Modules 3 (evaluation) and 4 (data) are the re-reads; module 2 is the reference I will keep open during Phase B.

## Modules
1. [Foundations](module-1-foundations.md) — what post-training is, imitation vs optimization, reasoning and Constitutional AI examples, lab recipes (R1, Qwen, Llama).
2. [Mechanics](module-2-mechanics.md) — tokens, cross-entropy and loss masking, hyperparameters and loss curves, LoRA/PEFT, preference learning, the RL objective, PPO vs GRPO.
3. [Evaluation as the North Star](module-3-evaluation.md) — evals as steering, RL monitoring signals, alignment tax, reward hacking, error analysis playbook, red teaming.
4. [Data](module-4-data.md) — error-driven dataset iteration, rollout sizing, synthetic pipelines, template engineering, data/reward balancing, the DeepSeek v3 recipe.
5. [Production](module-5-production.md) — the R1 pipeline, agent post-training, promotion rules, the feedback flywheel, monitoring, infrastructure and memory math, the go-live checklist.

## Key takeaways
- Fine-tuning is imitation; RL is optimization against feedback. Pick the lever by failure type.
- Data makes fine-tuning work; grading makes RL work. Both are built iteratively from error analysis.
- Evals steer. Track the alignment tax (reward-model score vs human judgment) or you will ship a reward hacker.
- GRPO's group-mean baseline is why reasoning RL is now runnable outside frontier labs.
- Production is a contract: frozen test environments, sliced promotion rules, zero-regression gates, and a feedback-to-data flywheel.

## Builds to steal
- **Phase B recipe:** SFT (LoRA) on quality CoT, then GRPO with verifiable rewards on LiveCodeBench, rollout difficulty filtering, group-mean baselines.
- **Error analysis playbook:** cluster failures, categorize with an LLM analyst, apply the errors → causes → fixes mapping, scale validated fixes 10x.
- **Promotion-rule template:** zero-regression slices, safety caps, capability-must-improve gates, canary on live traffic before full release.

## Notebooks
None downloaded. The video lessons carry no notebooks; the graded labs sit behind the paid plan and were not started under the read-only constraint. The patterns above capture what matters.

## Extraction note
All 43 video lessons extracted and distilled, including lesson 9 (data shapes, splits, and leakage prevention), which was recovered in a follow-up pass and folded into module 2.
