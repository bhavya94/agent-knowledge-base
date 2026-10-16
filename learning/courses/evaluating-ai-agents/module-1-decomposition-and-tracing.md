# Module 1 — Decomposing Agents and Tracing Them

**Course:** Evaluating AI Agents (DeepLearning.AI, with Arize AI) **Date:** 2026-10-15 **Verdict:** the methodology module. Decompose, trace, then evaluate: in that order.

## What problem?
Agents are non-deterministic software that acts on a user's behalf through reasoning. They behave differently by context and sometimes decide wrong. Traditional software testing (deterministic assertions, a train on a track) does not fit a system that drives itself through a busy city. Running the agent and eyeballing the result does not scale, and a single end-to-end score cannot say which part failed.

## What idea?
**Evaluate the system, not just the model.** Model benchmarks (MMLU, HumanEval) help choose a base model. System evaluation grades the whole application (prompts, tools, memory, routing) on datasets built from real-world data. The course's method:
- **Decompose the agent into skills.** An agent is reasoning (LLM) + routing (choosing the tool or skill) + action (executing it). Every skill has a **core** (its job) and a **context** (what it is given: user request, history, other skills' outputs). The router's core is routing each request to the right skill; richer context enables more thorough evaluation.
- **Evaluate at three levels.** Skill-level: did the skill do its core job (correct search results, correct API call, handled errors)? Trajectory: did the agent combine skills correctly (right sequence, right number of calls, no redundancy)? End-to-end: was the user's request fulfilled?
- **Trace everything.** Traces capture a full run; spans record individual steps (LLM calls, tool calls, chain logic, DB lookups), nested hierarchically. OpenTelemetry is the standard; OpenInference adapts it for LLMs; Arize Phoenix collects, visualizes, and evaluates traces. Instrumentation can be automatic (an instrumentor wraps the OpenAI library, every call becomes an LLM span) or manual (`@tracer.tool`, `@tracer.chain`, an outer "Agent Run" span). Nested spans localize failures precisely: if the inner "execute SQL" span fails but the outer tool span succeeds, the problem is the database connection, not the tool.

The course builds its running example in Lab 1 (a conversational agent over a dummy sales dataset with three tools: SQL lookup, data analysis, visualization) and instruments it in Lab 2. The eval runner pattern is set here too: an experiment plus a dataset, with traces supplying each skill's span inputs and outputs as eval material.

## Why it matters
- Decomposition is what makes agent evals diagnostic. A failing end-to-end score plus per-skill scores tells you where to intervene.
- Traces are the bedrock: in production they are a database of every run, and they export directly into evaluation at scale.
- Small prompt or code changes ripple through agent systems. A representative test set, rerun on every change, is the only regression defense.

## How I'd use it
- **Roadmap Phase 2 (judge):** my eval harness adopts the three levels explicitly: skill judges, trajectory checks, end-to-end judges. The Data Agents course's GPA framework slots in as the trajectory layer (plan adherence is trajectory evaluation with a plan).
- **Roadmap Phase 3 (harness):** instrument first, with an outer run span and per-tool spans, so evals have material to consume from day one.

## Open questions
- Phoenix is the course's platform (Arize built it). The method is platform-agnostic; my harness choice stays open, with span structure as the portable part.
