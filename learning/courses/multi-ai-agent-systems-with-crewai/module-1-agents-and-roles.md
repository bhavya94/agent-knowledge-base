# Module 1 — Agents and Roles

**Course:** Multi AI Agent Systems with crewAI (DeepLearning.AI) **Date:** 2026-10-15 **Verdict:** foundational. The vocabulary and mental models are the durable part; the crewAI API specifics are not.

## What problem?
Single-shot prompting caps what an LLM can do: one pass, no tools, no iteration, no self-check. Traditional if/else automation is brittle for the same reason in reverse: every edge case must be hand-coded. The agentic paradigm handles fuzzy inputs, fuzzy transformations, and fuzzy outputs.

## What idea?
An **agent** is an LLM that poses and answers its own questions, self-correcting toward a goal, equipped with tools to act in the world. crewAI's six components:
- **Role playing:** role + goal + backstory. Measurably improves performance; a backstory gives the persona context to reason from.
- **Focus:** sharp objective per agent. Multiple focused agents beat one overloaded agent.
- **Tools:** skills like search or scraping (module 2).
- **Cooperation:** agents talk, give feedback, delegate (`allow_delegation`).
- **Guardrails:** human-in-the-loop plus limits (max iterations, max RPM, max execution time). Keeps agents off rabbit holes.
- **Memory:** short-term (RAG-style store of recent executions, shared during a run), long-term (SQLite-backed learnings across runs, with self-critique), entity (facts about people/places/concepts), contextual (carried between tasks).

The **manager mental model**: design like a manager assembling a team, not a programmer writing steps. Define the outcome, decide the roles, equip each role with tools, then decide how they collaborate.

## Why it matters
- Role-playing with a backstory is a near-free performance lever, worth trying before any heavier intervention.
- Guardrails as framework primitives (iteration/time/rate caps) are the difference between a demo and something shippable.
- Memory types map to real system choices: short-term for in-run context, long-term SQLite for cross-run learning.

## How I'd use it
- **Roadmap Phase 2 (judge):** per-agent evals. If each agent has a crisp role and expected output, you can judge subtasks independently instead of only end to end.

## Open questions
- How much of the role-playing gain survives when the underlying model gets stronger? Worth an A/B on a real task.
