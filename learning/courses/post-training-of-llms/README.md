# Post-training of LLMs

**Source:** DeepLearning.AI short course, built with the University of Washington and Nexusflow; instructor Banghua Zhu. **Date distilled:** 2026-10-17. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://learn.deeplearning.ai/courses/post-training-of-llms

## Verdict
A compact, well-sequenced tour of the standard post-training recipe: SFT, DPO, online RL (GRPO). One module, nine short videos, each method taught as a theory lesson plus a hands-on notebook on small models with TRL. It overlaps the earlier Intro to Post-training course in this set (the 43-lesson one) but is tighter and more code-forward; treat that one as the deep version and this one as the field guide. The notebook patterns (base vs tuned comparison, synthetic preference pairs, verifiable-reward GRPO on GSM8K) are the keepers.

## Modules
1. [The Post-training Landscape](module-1-the-post-training-landscape.md): lessons 1-2. What pretraining leaves undone, and the three-stage recipe (demonstrations, preferences, rewards) that fixes it.
2. [SFT: Imitation on Demonstrations](module-2-sft.md): lessons 3-4. Next-token loss on response tokens, chat templates, and a full SFTTrainer run on SmolLM2-135M, against the Qwen3-0.6B base vs SFT comparison.
3. [DPO: Preferences Without a Reward Model](module-3-dpo.md): lessons 5-6. The log-ratio trick that turns RLHF into a classification loss, beta as the KL dial, and synthetic chosen/rejected pairs built by string edits.
4. [Online RL: Learning From Your Own Outputs](module-4-online-rl.md): lessons 7-8. On-policy sampling, GRPO group-relative advantages, verifiable rewards, and a GRPO run on GSM8K with a boxed-answer reward function.
5. [Conclusion](module-5-conclusion.md): lesson 9. The three methods compose; pick by the signal you actually have.

## Key takeaways
- Post-training is a signal ladder: demonstrations (SFT), then preferences (DPO), then rewards on self-generated samples (online RL). Each stage assumes the previous stage's output as its starting policy.
- SFT is behavior cloning: cross-entropy on the response tokens only. It buys format and instruction following, not new knowledge.
- DPO removes the reward model and the sampler from RLHF. The policy's log-ratio against a frozen reference is an implicit reward; beta sets how far the policy may drift.
- GRPO removes the critic: sample a group per prompt, use the group mean as the baseline. With a checkable answer, the reward is a plain function, no learned model needed.
- Every practice lesson runs the same comparison: base or instruct checkpoint vs the tuned checkpoint, same questions. Isolate what each stage buys before stacking the next.

## Builds to steal
- **Base vs tuned harness:** load base and post-trained checkpoints of the same model, run identical questions, eyeball the delta. Cheap and honest stage-gating.
- **Synthetic preference pairs by targeted edit:** take the model's own answer as rejected, apply a deterministic fix (here, an identity string swap) as chosen. A narrow behavior change with zero annotation budget.
- **Verifiable reward as a plain function:** regex-extract the boxed answer, 1.0 on exact match with ground truth, 0.0 otherwise. A GRPO training signal in ten lines.

## Notebooks
Three course notebooks downloaded locally, referenced by name only (not committed; course IP):
- Lesson_3.ipynb (for lesson 4, SFT in Practice): SFTTrainer on SmolLM2-135M, plus the Qwen3-0.6B base vs SFT comparison.
- Lesson_5.ipynb (for lesson 6, DPO in Practice): DPOTrainer on SmolLM2-135M-Instruct with synthetic identity preference pairs, plus the Qwen2.5-0.5B instruct vs DPO comparison.
- Lesson_7.ipynb (for lesson 8, Online RL in Practice): GRPO on Qwen2.5-0.5B-Instruct over GSM8K with a boxed-answer reward function.

## Extraction note
All 9 video lessons extracted and summarized in paraphrase. A platform transcript outage mid-session changed the source mix: lessons 1-4 come from full transcripts; lessons 6 and 8 from their complete notebooks plus the official chapter lists; lessons 5, 7, and 9 from the official chapter structures plus the framing established in lessons 1-2, so those notes are thinner and are flagged in their module files. Item 10 is a graded quiz behind the membership gate; it was noted and not taken. Nothing was submitted and no account state changed.
