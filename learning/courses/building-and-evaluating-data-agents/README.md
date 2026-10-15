# Building and Evaluating Data Agents

**Source:** DeepLearning.AI short course, taught by Anupam Datta (Snowflake AI Research Lead) and Josh Reini (Snowflake Developer Advocate). **Date distilled:** 2026-10-15. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://learn.deeplearning.ai/courses/building-and-evaluating-data-agents

## Verdict
The most architecturally complete of the short courses: a full planner-executor data agent, enterprise data via Snowflake Cortex, trace-based evaluation, and an original process-eval framework (GPA). Module 3 is the re-read; module 1 is the architecture reference.

## Modules
1. [Multi-Agent Architecture for Data Work](module-1-multi-agent-architecture.md) — planner, executor, and specialized sub-agents in LangGraph; Command-pattern state flow; bounded replanning.
2. [Data Capabilities and Observability](module-2-data-capabilities-observability.md) — Cortex Analyst (text-to-SQL) and Cortex Search wrapped as an agent tool; RAG triad evaluation over OpenTelemetry traces via TruLens.
3. [GPA and Runtime Improvement](module-3-gpa-and-improvement.md) — Goal-Plan-Act alignment (plan quality, plan adherence, execution efficiency, logical consistency); planner prompt surgery; inline evals in the live control loop.

## Key takeaways
- Evaluate the process, not just the output. GPA's four failure modes localize where an agent broke.
- Instrumentation design follows eval design: no retrieval spans, no context relevance.
- An agent can be wrapped as a tool inside another agent, recursively, as long as the node interface stays uniform.
- Inline evaluations turn grading into a runtime control signal: score retrieval mid-run, replan if it is irrelevant.
- Bounded replanning (a hard cap) is a non-negotiable guardrail.

## Builds to steal
- **Planner-executor template:** numbered sub-goals with named owners, executor-written standalone sub-questions, replan cap of 3, synthesizer that reads only worker outputs.
- **GPA judge set:** four process judges (plan quality, adherence, efficiency, consistency) over traces, complementing triad output judges.
- **Inline eval decorator:** context-relevance scoring attached to retrieval steps, feeding the replan decision.

## Notebooks
Five course notebooks (workflow construction, Cortex expansion, observability, GPA measurement, GPA improvement) downloaded to my local workspace `browser_downloads/sess-55229930/`. Not committed here; they are course IP. The patterns above capture what matters.

## Extraction note
The platform transcript service failed for most lessons during extraction. Lessons 3-7 were covered via the full lesson 3 transcript plus all five notebooks read in full; lessons 1, 2, and 8 (intro, definitions, 1-minute conclusion) were covered from the course page descriptions and the course arc. Nothing material is missing, but fine detail in lessons 1-2 is thinner than elsewhere in this set.
