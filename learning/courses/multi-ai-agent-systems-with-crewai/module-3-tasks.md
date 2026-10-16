# Module 3 — Tasks

**Course:** Multi AI Agent Systems with crewAI (DeepLearning.AI) **Date:** 2026-10-15 **Verdict:** practical. The task anatomy is the closest thing the course has to an API worth memorizing.

## What problem?
Vague task definitions produce vague, unusable outputs. Output quality is bounded by task-definition quality: crisp descriptions plus explicit expected outputs are what let an agent deliver exactly what is needed.

## What idea?
A **Task** is the unit of work: `description` (what to do) + `expected_output` (exactly what the result should look like) + assigned agent. The expected output acts as a forcing function that keeps the agent focused.

Power features:
- **async_execution:** independent tasks run in parallel instead of blocking the crew.
- **context:** feed one task's output as input to another, building explicit pipelines.
- **Structured outputs:** `output_json` / `output_pydantic` force machine-readable results conforming to a schema, so downstream code or agents can parse reliably. The course's `VenueDetails` model demo is the pattern: name, address, capacity as typed fields instead of prose.

## Why it matters
- Briefing-task-like-you'd-brief-a-contractor is the whole discipline: specific, with context and constraints.
- Structured outputs are the interface between fuzzy agents and deterministic code. Any pipeline that consumes agent output needs this.
- Parallelize with async + context rather than accepting a slow sequential chain.

## How I'd use it
- **Roadmap Phase 2 (judge):** judge agents should emit Pydantic-structured verdicts. Per-criterion scores as typed fields, not prose to parse.
- **Roadmap Phase 3 (harness):** pipeline stages chained via context, with schemas at each boundary.

## Open questions
- None. Straightforward module.
