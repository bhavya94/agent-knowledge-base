# Evaluating AI Agents

**Source:** DeepLearning.AI short course, built with Arize AI. **Date distilled:** 2026-10-15. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://learn.deeplearning.ai/courses/evaluating-ai-agents

## Verdict
The most directly applicable course in the set for my Phase 2 judge work. It teaches a complete method: decompose the agent, trace it, grade each skill with the right evaluator family, structure experiments, calibrate your judges, and keep evaluating in production. Modules 2 and 4 are the re-reads.

## Modules
1. [Decomposing Agents and Tracing Them](module-1-decomposition-and-tracing.md) — system vs model evaluation; skills with core and context; skill, trajectory, and end-to-end levels; OpenTelemetry tracing with Phoenix.
2. [Evaluators](module-2-evaluators.md) — code-based, LLM-as-a-judge, and human evaluators; the selection rule; discrete labels never numeric scores; router eval's two dimensions (choice and parameters).
3. [Trajectory Evaluation and Structured Experiments](module-3-trajectory-and-structure.md) — convergence as a path-efficiency metric; Phoenix experiments (dataset, task, evaluators); one evaluator per component; version and prompt comparisons.
4. [Evaluation-Driven Development, Better Judges, Monitoring](module-4-edd-judges-monitoring.md) — the EDD loop; comprehensive-not-exhaustive datasets; judge improvement via models, rubrics, few-shot examples, and human calibration; production monitoring with the same evaluators.

## Key takeaways
- Decompose first: per-skill evals are what make agent failures diagnosable.
- Judges return discrete labels with explanations, never 1-100 scores.
- A judge you have not calibrated against human labels is a random number generator with good branding.
- Trajectory quality (convergence) is measurable, and its blind spots are knowable.
- Development evals and production monitoring are one system, not two.

## Builds to steal
- **Three-level eval design:** skill judges + trajectory checks + end-to-end judges, fed by traces.
- **Judge calibration protocol:** sample verdicts, human review, agreement rate, iterate prompt/model, then scale.
- **Experiment harness shape:** dataset → task → evaluator suite, one evaluator per component, mixed families by ground-truth availability.

## Notebooks
Five course notebooks (agent build, tracing, router/skill evals, trajectory evals, structured evals) downloaded to my local workspace `browser_downloads/`. Not committed here; they are course IP. The patterns above capture what matters.

## Extraction note
All 15 lessons extracted. Lessons 11, 13, 14, and 15 initially failed during a platform transcript outage and were recovered in a follow-up pass; lesson 12 was covered via its full lab notebook. The notes are complete.
