# Module 3: DPO, Preferences Without a Reward Model

**Course:** Post-training of LLMs (DeepLearning.AI, with UW and Nexusflow) **Date:** 2026-10-17 **Verdict:** the cleverest idea in the course. Coverage note: lesson 5 was extracted from the official chapter structure plus course framing after a transcript outage, so the theory half of this file is thinner than the others; lesson 6 is grounded in its full notebook.

## What problem?
After SFT the model answers in the right format, but many answers are mediocre, and some are wrong in ways demonstrations alone cannot fix: often you cannot write the ideal response, but you can recognize the better of two. Classic RLHF turns those comparisons into a reward model and then runs PPO against it, two extra systems to build and keep stable. DPO asks whether the reward model and the RL loop can be skipped entirely.

## What idea? (lesson 5, Basics of DPO)
- Data is triples: prompt, chosen response, rejected response. Preferences follow a Bradley-Terry style model: the probability of preferring chosen over rejected rises with the gap in their underlying rewards.
- The RLHF objective (maximize reward, stay within a KL budget of a reference policy) has a closed-form optimal policy. Rearranged, the reward of a response can be written as a scaled log-ratio between the trained policy and the frozen reference model, plus a constant that cancels within a pair.
- Substituting that expression into the preference model gives the DPO loss directly on the policy: increase the log-probability margin of chosen over rejected, measured relative to the reference model. It looks and trains like binary classification. No reward model, no sampling, no RL machinery.
- The coefficient beta is the KL dial: high beta keeps the policy close to the reference; low beta lets it chase the preference margin harder, with more drift risk.
- Equivalent view: the policy is its own implicit reward model. The log-ratio is the reward.
- Limits to keep in mind: DPO is offline, so it cannot explore responses outside the pair data; it can push down the probability of chosen responses too, as long as the margin grows; and it inherits whatever biases (length, style) the preference data contains.

## What practice? (lesson 6, DPO in Practice; notebook Lesson_5.ipynb)
- Comparison first: Qwen2.5-0.5B-Instruct vs the course's Qwen2.5-0.5B-DPO checkpoint on the same questions.
- The hands-on target is deliberately narrow: change the model's stated identity. The notebook builds preference pairs synthetically: take prompts from an identity dataset (mrfakename/identity), generate the model's own answer as the rejected response, then string-replace the original name (Qwen) with the target name (Deep Qwen) to create the chosen response. Pairs are formatted as ChatML chosen/rejected fields; a prepared version ships as banghua/DL-DPO-Dataset.
- Training is TRL's DPOTrainer on SmolLM2-135M-Instruct. Note the starting point: DPO runs on an instruct checkpoint, not a raw base model, matching the pipeline order from module 1.

## Takeaways
- If I can generate a bad answer and mechanically fix it, I have a preference dataset for free. Targeted edits are a legitimate pair-construction strategy for narrow behaviors.
- Beta is the one hyperparameter with a real interpretation: how much drift from the reference I am buying with the preference margin.
- DPO's simplicity is the point: a dataset of pairs, one loss, a standard training loop.
