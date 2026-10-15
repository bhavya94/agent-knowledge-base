# Building and Evaluating Advanced RAG

**Source:** DeepLearning.AI short course, taught by Jerry Liu (LlamaIndex co-founder/CEO) and Anupam Datta (TruEra co-founder/Chief Scientist), intro by Andrew Ng. **Date distilled:** 2026-10-15. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://learn.deeplearning.ai/courses/building-and-evaluating-advanced-rag

## Verdict
Short and dense. The RAG triad alone justifies it; the two retrieval techniques are clean, measurable upgrades over naive chunking. This is the course most directly connected to my Phase 2 judge work.

## Modules
1. [The RAG Triad (Evaluation Framework)](module-1-rag-triad-eval.md) — baseline pipeline with TruLens instrumentation; context relevance, groundedness, answer relevance as per-stage judges.
2. [Sentence-Window Retrieval](module-2-sentence-window-retrieval.md) — retrieve at sentence precision, expand to a surrounding window at query time.
3. [Auto-Merging Retrieval](module-3-auto-merging-retrieval.md) — hierarchical chunk tree; merge child fragments into parent context when the query needs breadth.

## Key takeaways
- Instrument before optimizing: baseline, eval questions, triad scores, leaderboard.
- The triad localizes failure. Low context relevance: fix retrieval. Low groundedness: the model is hallucinating. Low answer relevance: generation drift.
- Retrieval granularity and context granularity are separate decisions. Sentence-window and auto-merging each decouple them differently.
- Every retrieval change is an experiment with a score, never a vibe.

## Builds to steal
- **Triad judge set:** three LLM judges (context relevance, groundedness, answer relevance) with CoT reasons, run against a fixed eval set. Direct input to my Phase 2 judge design.
- **Retrieval experiment protocol:** baseline vs sentence-window vs auto-merging on identical questions, triad leaderboard picks the winner. This is my Phase A replay shape.

## Notebooks
Four course notebooks (baseline pipeline + eval setup, triad implementation, sentence-window, auto-merging) downloaded to my local workspace `browser_downloads/sess-55229930/`. Not committed here; they are course IP. The patterns above capture what matters.

## Extraction note
Lesson 6 (an 80-second conclusion video) could not be retrieved due to a platform transcript outage during extraction. Nothing of substance is missing; lessons 2-5 were covered via their full notebooks plus transcripts where available.
