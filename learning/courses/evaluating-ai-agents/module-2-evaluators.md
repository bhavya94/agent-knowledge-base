# Module 2 — Evaluators: Code, LLM Judges, Humans

**Course:** Evaluating AI Agents (DeepLearning.AI, with Arize AI) **Date:** 2026-10-15 **Verdict:** the practical core. The evaluator-selection rules and the judge caveats are the keepers.

## What problem?
Once an agent is decomposed and traced, each skill needs a grader. Different skills need different grading: some checks are mechanical, some are judgment calls, and picking the wrong evaluator family gives either false confidence or unaffordable cost.

## What idea?
Three evaluator families:
1. **Code-based:** regex matches, JSON parseability, keyword containment, comparison against ground truth, cosine similarity. Closest to traditional integration tests. Deterministic and cheap.
2. **LLM-as-a-judge:** a separate LLM grades outputs against a prompt template (input + output + context → label). Caveats stated plainly: only the strongest models (GPT-4o, Claude 3.5 Sonnet class) align closely with human judgment; judges are never 100% accurate, mitigated by prompt tuning or judge swaps; and judges must return **discrete labels** ("correct"/"incorrect"), never 1-100 scores, because models cannot meaningfully distinguish 83 from 79.
3. **Human annotation:** annotation queues over real runs, or end-user feedback (thumbs up/down). Most flexible and treated as ground truth, but labor-intensive and, for user feedback, selection-biased. Not a scale technique.

Selection rule: how qualitative is the metric, and how accurate must it be? Qualitative (summarization quality, analysis clarity) → LLM judge or humans. Mechanical (regex, validity, ground-truth comparison) → code. Need 100% accuracy → code or humans, never a judge.

**Router evaluation** has two dimensions, and the course's example shows why both matter: function-calling choice (did the router pick the right tool?) and parameter extraction (did it pass the right parameters?). An agent can call the shipping-status tool correctly, then pass an order number where a tracking ID belongs: right function, wrong parameters, failed task. The judge template for routing includes the question, the chosen tool call, and all tool definitions so the judge can compare against every option.

**Skill evals** mirror the families: SQL-generation correctness for the database skill (judge it, compare to ground-truth SQL, or compare query results to ground truth), analysis clarity plus entity correctness for the analysis skill, a runnable-code check for the visualization skill. Evals can target a whole skill or a single step inside it.

**The Phoenix pattern** (Lab 3): export spans from traces → apply evaluators to label each row → upload labels back as span evaluations. Router eval via a built-in tool-calling template and `llm_classify` (rails snap verdicts to "correct"/"incorrect", explanations captured, a 1/0 score column for visualization). The hardest part is not the judging; it is filtering down to the right spans and defining the right criteria. The lab ends with four live evaluators: tool calling, SQL generation, response clarity, runnable code, and the runnable-code eval immediately catches a real defect (generated code that does not run).

## Why it matters
- "Discrete labels, never numeric scores" is a judge-design rule I will not relearn the hard way.
- Router eval's two dimensions (choice + parameters) generalize: any tool-using agent needs both graded separately.
- Evaluator selection by qualitative-ness and accuracy requirement is a decision procedure, not a taste call.

## How I'd use it
- **Roadmap Phase 2 (judge):** my judges emit discrete labels with explanations; code-based checks run first wherever ground truth exists; humans reserved for calibration sets that measure judge agreement (Kappa).
- **Project 01 (extraction eval lab):** extraction correctness gets code-based checks where schemas allow, judges for faithfulness, exactly per this selection rule.

## Open questions
- Judge improvement (model swaps, rubrics, few-shot examples, calibration against human labels) is covered in module 4.
