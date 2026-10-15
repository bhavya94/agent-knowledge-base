# Module 3 — Automated Red Teaming

**Course:** Red Teaming LLM Applications (DeepLearning.AI, built with Giskard) **Date:** 2026-10-15 **Verdict:** the most actionable module. The three-layer automation ladder is directly reusable.

## What problem?
Manual red teaming is slow and unrepeatable. Every attempt has three steps (devise a failing input, send it, judge the output), and doing all three by hand does not scale to a real app.

## What idea?
The automation ladder, three rungs:
1. **Hand-written injections + rule-based detection:** a `prompt_attempts` list (fake system prompts, "forget all previous instructions," assistant-completion primers). Loop over them, reset the app each time, detect success by matching the payload in the output. Cheap, deterministic where it works.
2. **Prompt library:** a CSV of known jailbreak techniques (columns: name, prompt, payload, type), run the same loop. Successful ones become leads for deeper manual work. Caveats: repeat each injection (non-determinism), keep the library current with the literature.
3. **Giskard LLM Scan:** open-source vulnerability scanner. Wrap the model in a standard interface (prediction function over a DataFrame, `giskard.Model` with type/name/description), provide a dataset, run `scan()`. The injection scan found 7 issues (6 major, 1 medium) on the demo bot in minutes. Scan tags extend to other categories.

Then the course pushes past rules: **LLMs doing all three steps.** An LLM generates adversarial inputs (cast as a red teamer, asked for a JSON list of questions likely to elicit bias, temperature=1 for diversity), the app answers them, and an **LLM evaluator** labels each Q&A pair safe/unsafe against the requirement. The Giskard scan does exactly this for discrimination: auto-generates the requirement ("loan eligibility must be based solely on business factors, not demographics") and reports violations. Practical tip: tweak the model description to steer the scan toward more problematic examples.

## Why it matters
- The three-step loop (generate, execute, judge) is the same loop as my eval harness. Red teaming is eval with an adversarial generator.
- LLM-as-judge for safety evals is the pattern I already plan for Phase 2; this course validates it and adds the adversarial-input generator half.
- Rule-based detection first, LLM judges second: the cheap layer catches the cheap failures.

## How I'd use it
- **Roadmap Phase 2 (judge):** build the adversarial input generator as a permanent fixture of the eval suite. Temperature-high generator model, requirement-specific evaluator prompts, safe/unsafe labels.
- **Project 01 (extraction eval lab):** run the ladder against the extraction pipeline: hand-written injections, then a jailbreak library, then LLM-generated adversarial prompts with an LLM judge.
- **Giskard:** evaluate the open-source scanner for my own use. It is the closest thing to an off-the-shelf red teaming baseline.

## Open questions
- How well does the LLM-judge step agree with human labels on safety? The course asserts it works; I want a Kappa number before trusting it in my pipeline.
