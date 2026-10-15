# Module 4 — Data: The Real Lever

**Course:** Fine-tuning & RL for LLMs: Intro to Post-training (DeepLearning.AI, Sharon Zhou, AMD) **Date:** 2026-10-15 **Verdict:** the most hands-on module. Data work is unglamorous and decisive, and this module treats it that way.

## What problem?
Teams treat data as a fixed input: collect a big dataset, train, hope. Failures get blamed on the model or the hyperparameters when the actual fix is targeted data aimed at observed failure patterns.

## What idea?
**Fine-tuning data is built iteratively, driven by error analysis.** Start with a small seed set (~20 examples), fine-tune with LoRA, evaluate, find the worst failure pattern, add targeted counter-examples, repeat. The course's case: a model drops a custom output tag only when "sunny" sits next to punctuation, so you add examples varying punctuation, synonyms, and capitalization. Next failure (wrong emoji for clear skies) gets its own counter-examples; then a "leakiness" failure (tags emitted when they should not appear) gets "no tag" examples. Data is always aimed at observed failures, never bulk-collected on spec. Two supporting techniques: teach custom prompt tags (novel tokens in inputs and outputs) purely through examples, and scale chain-of-thought share to the product (reasoning-heavy: at least ~40% reasoning data; latency-sensitive: mostly direct answers; a thinking toggle means training both modes). LoRA guidance: adapters in attention layers by default, MLP/linear when you need fact recall; rank scales with data volume; if high-rank LoRA still cannot move behavior, fix the data before reaching for full fine-tuning.

**RL data** is rollouts plus rewards. The pipeline: varied high-coverage inputs → multiple rollouts per input (8 is the GRPO-era default) → grade with verifiers or a reward model → trajectories → train → loop. Scale rules of thumb: thousands to ~20K rollouts for probing and ablations, 20K-100K for midsize updates, frontier alignment runs around 160K with diminishing returns beyond. Filter for signal: near-duplicate rollouts and too-easy/too-hard inputs teach nothing; moderately difficult rollouts carry the gradient. Reward-model data needs care: reward models overfit surface patterns (length as goodness), fixed with counterexamples (long-but-bad, short-but-excellent); track the alignment gap between RM scores and human eval explicitly and collect data where they diverge. Offline preference learning (train the RM once, freeze) is the stable starting point; online (RM adapts during training) suits high-traffic products.

**Synthetic data pipelines** scale all of this: generate, filter, score, transform. Constitutional AI is the exemplar division of labor: humans write the constitution (judgment work), machines critique and select at scale (throughput work). Filtering is what makes aggressive generation safe: LLM-as-judge filtering, verification templates, dedupe/collapse detection, majority voting. A smaller high-quality dataset beats a large noisy one.

**Template engineering** is the force multiplier: fix a template and you fix every example it generates. Error analysis becomes template design (model gives one-sided answers → a template that generates natural contrast pairs). User feedback like "too wordy" becomes a template, converting noisy complaints into structured training signal. Templates can even become rewards: score whether the output followed the template pattern (refused, named the principle, redirected safely) across a rubric (helpfulness, harmlessness, honesty, autonomy, each 0-10).

**Balancing** is the standing tension: generalization vs specialization. A 90% coding mix broke "what is the color of the sky?"; rebalancing fixed it. A helpfulness-maxed reward produced oversharing and unsafe speculation; reweighting toward safety fixed it. Mix ratios are empirical, driven by real usage, and the empiricism never ends because production distributions keep shifting.

**The DeepSeek v3 recipe** ties it together: cold-start long-CoT seed data, ~600K filtered reasoning samples (rejection sampling, no mixed languages, no stray code), ~800K total fine-tuning samples at roughly 75% reasoning / 25% non-reasoning. Production pipelines assemble many datasets, each feeding a specific stage.

## Why it matters
- The error-driven data loop is the Flywheel pattern at dataset scale: observe failure, generate targeted data, retrain, re-measure.
- Template engineering reframes data work from labeling to programming. Hundreds of editable templates beat thousands of hand samples.
- The rollout scale numbers give me concrete planning anchors for Phase B instead of guesses.

## How I'd use it
- **Roadmap Phase B (training track):** LiveCodeBench GRPO runs sized by these rules of thumb; rollout difficulty filtering built in from the start; RM alignment gap tracked if I train a reward model.
- **Roadmap Phase 2 (judge):** judge prompts are templates. The rubric-as-reward pattern (four axes, 0-10, weighted) is a judge design I can lift directly.
- **Project 01 (extraction eval lab):** seed small, error-analyze, add counter-examples. The 20-example seed loop is the fast start.

## Open questions
- The ~40% reasoning-share heuristic is product-dependent; treat as a starting point for my own sweep, not a constant.
