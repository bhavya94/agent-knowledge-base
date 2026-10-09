# Module 2 — Reflection

**Course:** Agentic AI (DeepLearning.AI)  **Date:** 2026-10-08

## What problem?
Direct generation, whether zero-shot or few-shot, produces one answer with no chance to catch its own mistakes.

## What idea?
**Reflection:** after generating, the model (or a dedicated reflection prompt or agent) assesses the output
for the task at hand at runtime, and then revises it.

- **External feedback** makes it stronger. Feeding real signals into the reflection step, such as tool output,
  test results or execution errors, improves results over time more than a fixed reflection prompt does.

## Why it matters
- Studies show a performance boost over zero-shot and few-shot prompting.
- **How well it works depends on whether the task is objective:**
  - **Objective tasks** (SQL generation, code generation) have a definitive right answer. Reflection reliably
    improves scores, and its effect is easy to measure against a ground-truth set.
  - **Subjective tasks** (e.g. judging which of two plots is better) have no objective measure. Pairwise LLM
    comparison suffers from **position bias**, so you need a **rubric**, which is the LLM-as-a-judge approach.
- **Measuring the impact always needs ground truth:** definitive answers for objective tasks, and a rubric
  with human labels for subjective ones.
- **Cost:** every reflection pass adds latency, and tokens.

## How I'd use it
- **Roadmap Phase 1–2:** QASPER mixes both kinds of answer. Extractive, yes/no and unanswerable answers are
  objective, so score them with answer-F1 against gold. Abstractive answers are subjective, so use a
  rubric-based judge. Use pointwise rubric scoring rather than pairwise comparison to avoid position bias.
- **Roadmap Phase 4:** the self-correction step is reflection with external feedback. The judge's score
  and critique are the feedback, not the student critiquing itself.
- **Latency budget:** measure the quality gain per reflection pass, and keep only passes that pay for their cost.

## Open questions
- How many reflection rounds before returns diminish? Does it depend on task type?
- Does position bias go away if you swap the order of the pair and average the two scores, or is a rubric still needed?
