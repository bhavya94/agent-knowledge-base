# Module 3 — Trajectory Evaluation and Structured Experiments

**Course:** Evaluating AI Agents (DeepLearning.AI, with Arize AI) **Date:** 2026-10-15 **Verdict:** the scaling module. Convergence is a neat metric; structured experiments are the real deliverable.

## What problem?
Skill evals say each part works. They do not say the agent takes a sane path (production agents carry 10-30 tools, and multi-agent systems compound the paths), nor do they let you compare two agent versions or two prompts without rerunning everything by hand.

## What idea?
**Trajectory evaluation** grades the path itself. A trajectory is the route through router, tools, and logic for one input. The course's metric is **convergence**: run the agent over a set of similar queries (similar enough that it should take the same path, different enough to show variation), record steps per run, take the minimum as the optimal path length, and score how often the agent achieves it (0-1, 1 = always optimal). Why it matters: fewer steps means fewer LLM calls, less output variability, lower cost, lower latency. Two honest caveats: convergence cannot catch an unnecessary step the agent takes every time (optimal is defined as the observed minimum), and it should only run on completed runs, since errored runs skew the data. Lab 4 implements it as a Phoenix experiment: a dataset of 17 phrasing variations, a task that runs the agent and returns path length, and a code-based evaluator scoring each run against the observed minimum (the demo run hit a perfect 1, with the note that non-determinism makes scores vary).

**Phoenix experiments** are the harness: dataset (inputs, optionally expected outputs) → task (a function run per example) → evaluators (applied to outputs). Expected outputs unlock ground-truth evaluator types.

**Evaluation-driven development** (lesson 11, implemented in Lab 5) structures all of it: instead of one monolithic end-to-end check, attach one purpose-built evaluator per architectural component. Lab 5 builds the full suite against a dataset with expected outputs: router → LLM-judge function-calling eval (choice + parameters); database tool → code-based SQL correctness; analysis tool → two LLM judges (clarity, entity correctness); visualization tool → code-based runnable check. The same experiment then runs Agent v1 vs Agent v2, and a second experiment swaps the SQL-generation prompt and measures the change with identical evaluators. Prompt iteration becomes a measured comparison instead of a vibe.

## Why it matters
- Convergence operationalizes "the agent is wasting steps" into a number, and its blind spot (a universally taken wasteful step) is exactly the kind of limitation worth knowing about your own metrics.
- One evaluator per component, mixed families by ground-truth availability, is the structured form of the module 2 selection rule.
- Version-vs-version and prompt-vs-prompt experiments on one harness are how agent development becomes engineering.

## How I'd use it
- **Roadmap Phase 2 (judge):** adopt the experiment shape (dataset → task → evaluator suite) for my harness; add a convergence-style path-length metric for any multi-step agent I evaluate.
- **Roadmap Phase 3 (harness):** prompt changes ship only with a same-evaluators comparison run. This is the Flywheel discipline at prompt scale.
- **Interview prep:** trajectory evaluation plus convergence is a distinctive, concrete answer for agent-eval depth questions.

## Open questions
- Minimum-observed-path as "optimal" is a proxy; a hand-specified golden trajectory would be stricter for critical flows. Worth combining both where the stakes justify it.
