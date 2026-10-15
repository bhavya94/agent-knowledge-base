# Module 4 — Evaluation-Driven Development, Better Judges, Monitoring

**Course:** Evaluating AI Agents (DeepLearning.AI, with Arize AI) **Date:** 2026-10-15 **Verdict:** the operating system for everything before it. EDD is the workflow; judge calibration is the discipline; monitoring is the flywheel.

## What problem?
Evals scattered across notebooks do not compound. Teams guess where to improve, cannot compare iterations cleanly, trust judges they never validated, and stop evaluating the moment the agent ships, exactly when real users start breaking it.

## What idea?
**Evaluation-driven development (lesson 11)** organizes the whole practice into a loop: curate a dataset of test cases → run cases through agent variants (models, prompts, logic) → score with evaluators → compare iterations apples-to-apples. Each pass improves the test set, the evaluators, and the agent. Test-case curation guidance: **comprehensive, not exhaustive** (representative inputs, one or two examples per input type), sourced from production runs, manual construction, or LLM generation; include expected outputs where possible to unlock code-based evaluators, and use judges where outputs cannot be pinned down. An experiment is one variant run through the cases; the dashboard view (runs as rows, evaluators as columns) shows the holistic effect of a change across the whole agent, not one metric.

**Improving the LLM judge (lesson 13):** a judge is a model plus a prompt, so there are exactly two levers. Model-side: swap judge models between runs, consider specialized judges (a hallucination-detection judge) or larger models, and remember judge cost scales with evaluation volume. Prompt-side: ask for explanations with the verdict, give an explicit rubric, and load few-shot examples (the instructor adds five or six, more is better). Iterate fast with versioned templates in a prompt playground before spending evaluation budget. Then **calibrate**: humans review a sample of verdicts (no need to label everything), compute the human-judge agreement rate, and iterate the prompt or model until agreement is high. A calibrated judge is how human intuition scales.

**Monitoring (lesson 14)** runs the same evaluators on live production traffic. Pick two or three development evaluators that generalize (LLM judges fit production because inputs are unpredictable and expected outputs do not exist; keep code-based checks that still apply, like JSON parseability). On Arize, spans already flow in via OpenTelemetry, so monitoring is applying evaluator objects across spans in parallel and logging the labels back onto the spans. The demo is persuasive: pointed at a sloppier support agent, monitoring catches an entity failure (answering "your most recent order" instead of the actual order ID in the trace) and a pile of hallucinated responses. Monitoring catches drift, data-quality issues, and unexpected inputs, and its failures become new test cases, closing the flywheel back into development.

## Why it matters
- Judge calibration with an agreement rate is the missing step in most LLM-judge setups, mine included. Uncalibrated judges produce numbers nobody should ship on.
- Comprehensive-not-exhaustive is the dataset-sizing principle that keeps eval suites maintainable.
- Development evals and production monitoring are the same evaluators in two places. Build once, run everywhere.

## How I'd use it
- **Roadmap Phase 2 (judge):** calibration becomes a formal step: human-label a sample, measure agreement (Kappa), iterate the judge prompt with few-shot examples and a rubric until agreement clears a bar, then scale. This answers the open question I flagged in the Red Teaming and post-training notes.
- **Roadmap Phase A replay:** the eval set gets built comprehensive-not-exhaustive, with production-style prompts feeding new cases over time.
- **Interview prep:** "how do you know your judge is any good?" is now a rehearsed answer: sample, human review, agreement rate, iterate.

## Open questions
- None. The course is complete and self-consistent.
