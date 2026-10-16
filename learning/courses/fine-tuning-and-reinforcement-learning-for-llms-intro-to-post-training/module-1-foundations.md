# Module 1 — Foundations: What Post-Training Is

**Course:** Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, Sharon Zhou, AMD) **Date:** 2026-10-15 **Verdict:** the framing module. If you only keep one idea: fine-tuning is imitation, RL is optimization against feedback.

## What problem?
Prompt engineering plateaus (92% → 95% → 95.5% → stuck). Base models are raw intelligence: they continue text instead of answering, ramble instead of helping. Something has to convert that raw capability into usable behavior, and prompting alone cannot.

## What idea?
**Post-training** is that conversion step, sitting after pre-training (next-token prediction on internet-scale data) and mid-training (curated continued pre-training for languages, modalities, context length). Two techniques:
- **Fine-tuning (SFT):** train on input/target-output pairs. The model compares its output to the target token by token and nudges weights toward the demonstrated behavior. Imitation: "do it like this example." Excellent at format, style, process.
- **RL:** no target output. The model generates, a grader scores it (+1 correct, 0 incorrect), and weights shift toward high-scoring outputs. Optimization: "do whatever scores well." Can discover paths beyond the demonstrations, at the cost of instability (hence stability-obsessed algorithms).

What makes each work: **data** makes fine-tuning work (pairs must reflect the full interaction, including chat history, think/answer tags, and recovery from bad retrieval); **grading** makes RL work (deterministic regex verifiers or learned LLM judges; a flawed grader gets reward-hacked). The production pipeline combines both, iteratively: fine-tune, build RL environments (inputs, graders, tools), run the RL loop, repeat.

Two worked examples anchor the module:
- **Reasoning:** fine-tune on chain-of-thought data (roughly 2,000-10,000 examples) so the model learns process templates, then RL with verifiers so it learns better reasoning. DeepSeek R1-Zero skipped the fine-tuning and got reasoning from RL alone, plus endless repetition and poor readability. The two-phase recipe exists for a reason.
- **Safety (Constitutional AI / RLAIF):** a human writes a constitution once; an LLM critiques and revises outputs against it for fine-tuning data; the same constitution drives AI preference labels for a reward model and RL. Anthropic's result: as helpful as RLHF, significantly more harmless.

In the wild, labs pipeline the techniques repeatedly: DeepSeek R1 and Qwen both run SFT → RL → generate more data → SFT → RL. Llama adds rejection sampling (generate lots, keep the best, fine-tune on it) and DPO.

## Why it matters
- The recipe framing (SFT teaches form, RL teaches optimization) predicts which lever to pull for a given failure.
- Error analysis is named as the hardest-to-automate, highest-value human skill in the loop. That is a career-relevant claim, not just a course nicety.
- Cooking analogy worth keeping: fine-tuning is following a recipe step by step; RL is "produce the final dish, any path allowed," which can find superhuman routes and weird ones.

## How I'd use it
- **Roadmap Phase B (training track):** SFT then GRPO on LiveCodeBench is exactly the two-phase recipe. The course validates the sequencing.

## Open questions
- None for the framing. The mechanics modules carry the detail.
