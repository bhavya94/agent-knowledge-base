# Module 1 — Intro to Agentic Workflows

**Course:** Agentic AI (DeepLearning.AI)  **Date:** 2026-10-08  **Verdict:** basic. A vocabulary module.

## What problem?
Single-shot prompting (zero-shot or few-shot, with one response) caps what an LLM can do. The model gets one pass,
with no tools, no iteration, and no way to check its own work.

## What idea?
**Agentic workflows** run the LLM over multiple steps and turns, with tool use and longer-running sessions.

- **Autonomy is a spectrum.** At the low end, a human fixes the sequence of steps and tools. At the high end,
  the LLM decides which tools to use and in what order.
- **Task decomposition:** break the task down the way a human would, then decide the tools and workflow for each step.
- **Four design patterns:**
  1. **Reflection:** the LLM critiques its own output and revises it. Can use a dedicated critic agent.
  2. **Tool use:** the LLM calls external functions or APIs.
  3. **Planning:** the LLM decides the sequence of actions up front.
  4. **Multi-agent collaboration:** specialized agents, each with its own tools, work on one task.
     My example (not from the course): OpenAI Dots, launched at OpenAI Dev Day 2026.

## Why it matters
- Decomposition makes the system **evaluable per subtask**, not only end to end.
  - Subtask evals can be deterministic (discrete pass/fail) or score-based.
  - Reading the reasoning trace shows *where* a run went wrong.
- Independent subtasks can run in **parallel**.
- Trade-off: more autonomy means more flexibility, but less predictability and harder evaluation.

## How I'd use it
- **Roadmap Phase 2 (judge):** per-subtask evals map directly onto per-criterion judges.
  Reading reasoning traces is how I'd debug judge disagreements.
- **Roadmap Phase 4 (post-train):** reflection with a dedicated critic is the self-correction step:
  a critic panel repairs low-scoring answers.
- **My own workflow:** Build → Explainer → Reviewer → Demo is low-autonomy decomposition.
  The `reviewer` skill is the reflection pattern with a separate critic.

## Open questions
- Agentic applications: the module covered examples, but I didn't capture them.
