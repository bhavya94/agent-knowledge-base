# Module 2: SFT, Imitation on Demonstrations

**Course:** Post-training of LLMs (DeepLearning.AI, with UW and Nexusflow) **Date:** 2026-10-17 **Verdict:** standard content, well executed. The base vs SFT side-by-side is the part to copy.

## What problem?
A base model given a question tends to continue the text: more questions, a fake forum thread, a rambling completion. It has the knowledge but not the contract. SFT installs the contract: given an instruction, produce one direct answer in the expected format.

## What idea? (lesson 3, Basics of SFT)
- SFT is supervised training on demonstration pairs: prompt in, target response out, ordinary cross-entropy next-token loss.
- The loss is computed on the response tokens; the prompt is context and is typically masked out. The model learns P(response | prompt), one token at a time.
- Mechanically this is behavior cloning: whatever distribution the demonstrations come from is the behavior you get. Dataset quality, consistency of style, and coverage of the target tasks dominate; raw size does not.
- Formatting is part of the training signal: examples are wrapped in a chat template (system/user/assistant roles, ChatML style) so the model learns where turns start and stop, including the end-of-turn token that makes generation halt cleanly.
- Known limits: SFT teaches format and surface behavior, not new facts; and it can narrow the model (catastrophic forgetting of pretraining breadth) if the data is too narrow or training runs too long.

## What practice? (lesson 4, SFT in Practice; notebook Lesson_3.ipynb)
Two-part notebook pattern:
1. **Read a finished run:** load Qwen3-0.6B-Base and the course's pre-trained Qwen3-0.6B-SFT checkpoint, run the same simple questions through both. The base model drifts and continues the text; the SFT model answers directly. This isolates exactly what the stage buys.
2. **Run it yourself, small:** SmolLM2-135M plus the course dataset (banghua/DL-SFT-Dataset), trained with TRL's SFTTrainer. Config worth noting: learning rate 8e-5, 1 epoch, per-device batch 1 with gradient accumulation 8, logging every 2 steps. CPU-feasible end to end; afterward the same questions are re-run to see the shift.

## Takeaways
- Always evaluate a fine-tune against its own base checkpoint on identical prompts; comparing to a different model muddies what the stage did.
- One epoch over good demonstrations at a modest learning rate is the default recipe here, not a long grind.
- TRL's SFTTrainer collapses the boilerplate: model, SFTConfig, dataset, train. The interesting decisions are data and template, not the loop.
