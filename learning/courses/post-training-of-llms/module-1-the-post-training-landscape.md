# Module 1: The Post-training Landscape

**Course:** Post-training of LLMs (DeepLearning.AI, with UW and Nexusflow) **Date:** 2026-10-17 **Verdict:** the framing lessons. One clean mental model: post-training is three kinds of signal applied in sequence.

## What problem?
Pretraining teaches a model to predict the next token over web-scale text. The result is a base model that completes documents, not one that follows instructions, answers in a usable format, or prefers helpful answers over merely plausible ones. Post-training is everything done after pretraining to close that gap.

## What idea?
Three methods, ordered by the signal they consume (lessons 1-2):
1. **SFT (supervised fine-tuning):** imitate labeled demonstrations. Input: (prompt, good response) pairs. Offline and supervised; standard next-token training on curated answers.
2. **DPO (direct preference optimization):** learn from comparisons. Input: (prompt, chosen response, rejected response) triples. Still offline; no sampling during training and no separate reward model.
3. **Online RL:** optimize a reward on the model's own fresh outputs. Input: prompts plus a reward function or reward model. On-policy: the model generates, gets scored, and updates toward higher-reward behavior (RLHF with PPO historically; GRPO in this course).

## Why the order matters
Each stage starts from the previous stage's checkpoint. SFT produces a policy that follows instructions well enough to generate meaningful candidates. DPO sharpens which of those candidates it prefers. Online RL then explores beyond the fixed datasets, because its training data is whatever the current policy produces. Skipping stages breaks the chain: preference pairs are useless if the model cannot yet produce a coherent answer, and RL exploration is wasted on a model that cannot follow the prompt format.

## Key details
- The course's working definitions, restated in its (gated) quiz: SFT is imitation of labeled responses, DPO is learning from preferred vs less-preferred pairs, online RL is optimizing reward on generated outputs. One line per method, worth memorizing as-is.
- All three methods are weight updates on the same pretrained backbone; nothing here changes the architecture.
- Data, not algorithms, is the differentiator between stages: demonstrations, comparisons, or a scorer.
