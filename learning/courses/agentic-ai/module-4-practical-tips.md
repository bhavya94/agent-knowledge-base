# Module 4 — Practical Tips

**Course:** Agentic AI (DeepLearning.AI)  **Date:** 2026-10-15

## What problem?
Once an agentic workflow runs end to end, it's hard to know *where* it falls short. It's also easy to waste effort
improving the wrong step, or to ship something too slow or too expensive.

## What idea?
**Evals: start rough, then localize.**
1. Build a **quick-and-dirty LLM-as-a-judge prototype** early, rather than waiting for a polished eval.
2. Do **error analysis on component traces.** Inspect each step's output, not just the final answer, to find
   which component causes most failures. That tells you where to focus.

**Levers to improve performance**, roughly from cheapest to most expensive:
1. Improve the prompts.
2. Try a different model.
3. Split a step into smaller steps.
4. Fine-tune.

**Cost and latency: measure per step.**
- **Latency:** time each step of the workflow. Then use parallelism, smaller models, or faster providers where a step dominates.
- **Cost:** a function of input and output tokens. It can be computed for each step, so you know which one to optimize.

## Why it matters
- Without error analysis by component, improvements are guesses. The step you suspect is often not the bottleneck.
- A rough judge early gives a feedback signal for every later change. You refine the judge as you learn what fails.
- The order of the levers matters. Prompt and model changes take hours; fine-tuning takes weeks and needs data.
  Use the cheap levers first.
- Measuring cost and latency per step turns "it's too slow or expensive" into a specific step to fix.

## How I'd use it
- **reflective-qa looked at this the other way round:** one end-to-end metric (answer-F1) showed no reflection
  setup helped, and the reason only appeared from reading the revisions. Abstention-to-answer fixes gained, while
  rewording correct drafts lost, and the two cancelled out. Per-component scoring would have found that directly:
  retrieval (evidence recall@k), the draft, the critic's verdict, and the revision. That's the case for scoring
  each step separately next time.
- **Next step, building evals:** start with a quick, meaning-aware LLM judge prototype on the 200 existing
  questions and answers. Validate it against human labels later (roadmap Track A), not before using it.
- **Cost tracking already works per run** (the `cost` column, $3.77 total so far). Break it down per step
  (writer, critic, revision) to see whether the critic pass is worth its tokens.
- **Roadmap Track B:** fine-tuning comes last. Only start it after prompt, model and step-splitting changes
  have plateaued, which matches the roadmap's "prompt/harness first, weights later".

## Open questions
- How rough can the first judge be? At what point does judge noise hide the real differences between setups?
- How do you attribute cost and latency across parallel or retried steps?
