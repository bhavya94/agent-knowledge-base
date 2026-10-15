# Module 3 — Auto-Merging Retrieval

**Course:** Building and Evaluating Advanced RAG (DeepLearning.AI, with LlamaIndex and TruEra) **Date:** 2026-10-15 **Verdict:** the complement to sentence-window. Dynamic context granularity based on what the query actually needs.

## What problem?
Some questions need a precise sentence; others need a whole section. Fixed chunking forces one granularity on every query, so broad questions get fragmented context and narrow questions get bloated context.

## What idea?
**Auto-merging retrieval** organizes documents into a tree and lets retrieval decide the granularity:
- A `HierarchicalNodeParser` splits documents into nested chunks (the course uses 2048 → 512 → 128). Leaf nodes hold small chunks and get embeddings; parent nodes hold the merged text of their children.
- Retrieval runs over leaf nodes.
- The `AutoMergingRetriever` merges upward: when several retrieved children share a parent, the parent's fuller text replaces the fragments as context.

The course builds the hierarchical index, queries it, and compares RAG triad scores against the baseline and sentence-window approaches on the same leaderboard.

## Why it matters
- Context granularity adapts to the query: narrow questions stay at leaf level, broad questions bubble up to parent context.
- The chunk-size hierarchy is a tuning decision, and over-merging can inject irrelevant text that hurts precision. The triad scores tell you when you have over-merged.
- It complements rather than replaces sentence-window retrieval. Different failure modes, different fixes, same eval harness to choose between them.

## How I'd use it
- **Roadmap Phase 2 (judge):** second retrieval experiment in the replay plan, after sentence-window. Triad scores decide which survives.
- **Interview prep:** "how do you handle questions that need different amounts of context?" is now an answered question with a mechanism, not a hand-wave.

## Open questions
- The hierarchy depths and chunk sizes are presented as given. On a real corpus I would want a selection heuristic; likely corpus structure (headings, sections) should drive it rather than fixed token counts.
