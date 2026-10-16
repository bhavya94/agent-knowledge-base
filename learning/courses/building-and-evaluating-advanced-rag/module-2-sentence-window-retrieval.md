# Module 2 — Sentence-Window Retrieval

**Course:** Building and Evaluating Advanced RAG (DeepLearning.AI, with LlamaIndex and TruEra) **Date:** 2026-10-15 **Verdict:** a clean, cheap technique. Precision retrieval with coherence restored at query time.

## What problem?
Naive fixed-size chunking splits semantically related sentences arbitrarily and hands the LLM incoherent context. Small chunks retrieve precisely but lack surrounding meaning; large chunks are coherent but dilute relevance and waste context budget.

## What idea?
**Sentence-window retrieval** decouples retrieval granularity from context granularity:
- Parse documents into individual sentences. Embed and retrieve at the sentence level, where precision is highest.
- Each sentence node carries window metadata: the surrounding sentences.
- At query time, a metadata-replacement postprocessor swaps each retrieved sentence for its full window before generation.

Implementation is two LlamaIndex pieces: `SentenceWindowNodeParser` to build the sentence nodes with window metadata, and `MetadataReplacementPostProcessor` to perform the swap. The course builds baseline and sentence-window indexes over the same document, queries both, and compares RAG triad scores on a leaderboard.

## Why it matters
- Window size is the tuning knob: too small loses coherence, too large wastes context and dilutes relevance.
- The technique changes only parsing and post-processing. Same embedding model, same LLM, so it is cheap to A/B against a baseline.
- It shines when answers hinge on specific sentences that need nearby context to interpret, which is most factual QA.

## How I'd use it
- **Roadmap Phase 2 (judge):** Phase A of my replay plan is RAG faithfulness on self-generated prompts. Sentence-window retrieval is a candidate retrieval upgrade to test against the baseline with triad scoring.
- **Project work:** any doc-QA build gets sentence-window as the first retrieval experiment, measured before and after.

## Open questions
- Optimal window size is corpus-dependent. The course does not give a selection procedure beyond tuning; I would sweep window sizes against the triad on my own eval set.
