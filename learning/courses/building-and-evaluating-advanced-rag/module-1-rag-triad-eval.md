# Module 1 — The RAG Triad (Evaluation Framework)

**Course:** Building and Evaluating Advanced RAG (DeepLearning.AI, with LlamaIndex and TruEra) **Date:** 2026-10-15 **Verdict:** the most valuable part of the course. The triad is a diagnostic framework I can apply to any RAG system immediately.

## What problem?
RAG answers go wrong in vague ways ("the answer seems off") with no signal about which stage failed. Teams iterate blind: tweak prompts when the real problem is retrieval, or swap embedding models when the real problem is hallucination. Without per-stage measurement, RAG quality is un-debuggable.

## What idea?
Instrument the pipeline first, then improve it. Build a baseline RAG (LlamaIndex `VectorStoreIndex` over a document set), wrap the query engine with a TruLens recorder, run a fixed set of eval questions, and score three metrics, one per stage of RAG execution. This is the **RAG triad**:
1. **Context relevance:** is each retrieved chunk relevant to the question? Low score means fix retrieval.
2. **Groundedness:** are the answer's claims supported by the retrieved context? Low score means the LLM is hallucinating beyond its context.
3. **Answer relevance:** does the answer actually serve the question? Low score means generation drift.

Each metric is an LLM-as-judge feedback function with chain-of-thought reasons, so scores come with explanations. Run baselines and candidate improvements against the same eval questions and compare on a leaderboard instead of eyeballing outputs.

## Why it matters
- The triad localizes failure to a stage, turning RAG debugging into error analysis instead of guesswork.
- LLM-as-judge with CoT reasons is the practical eval pattern: cheap, interpretable, repeatable.
- Baseline first, instrument second, optimize third. Any other order wastes effort on unmeasured changes.

## How I'd use it
- **Roadmap Phase 2 (judge):** the triad IS a judge design. Context relevance judges retrieval, groundedness judges faithfulness, answer relevance judges utility. My RAG faithfulness replay plan maps one to one onto this.
- **Flywheel memory:** the Flywheel's judge-scored datasets are the same shape. Per-criterion judges with reasons, not a single holistic score.
- **Interview prep:** EvenUp's HM call covers eval metrics and embeddings. The triad gives me a crisp framework answer for "how do you evaluate a RAG system?"

## Open questions
- TruLens is the course's tool; the framework is tool-agnostic. Worth checking whether my own harness should adopt TruLens or keep the triad as hand-rolled judges. Leaning hand-rolled for control, triad for the metric definitions.
