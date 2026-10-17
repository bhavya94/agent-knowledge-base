# Module 5: Conclusion

**Course:** Post-training of LLMs (DeepLearning.AI, with UW and Nexusflow) **Date:** 2026-10-17 **Verdict:** two minutes, one decision rule. Coverage note: extracted from the official chapter structure plus course framing after a transcript outage.

## The wrap-up (lesson 9)
The course closes by restating the pipeline as a single recipe: start from a pretrained base model, run SFT on demonstrations to install instruction following, run DPO on preference pairs to sharpen choices, then run online RL so the model optimizes reward on its own outputs. Each stage exists because the previous stage's signal runs out: demonstrations cannot express comparisons, comparisons cannot express discovery, and a reward can score anything the policy can generate.

## Decision rule to keep
Pick the stage by the signal I actually have:
- I can write good answers: SFT.
- I can only judge answers: DPO (or collect pairs for it).
- I can automatically check answers: online RL with a verifiable reward.

That framing is the course in one paragraph, and it maps directly onto my evals work: building the checker is what unlocks the strongest training stage.
