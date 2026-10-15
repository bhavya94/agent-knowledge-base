# Module 2 — Data Capabilities and Observability

**Course:** Building and Evaluating Data Agents (DeepLearning.AI, with Snowflake) **Date:** 2026-10-15 **Verdict:** two halves. The Cortex wrapping pattern is vendor-specific; the triad-over-traces evaluation is general and valuable.

## What problem?
A web-research agent is a demo. Real data agents must answer over internal enterprise data (structured CRM records, unstructured meeting notes), and once they do, nobody can tell whether an answer is good, or which step failed when it is not.

## What idea?
**Capabilities:** the enterprise data landscape splits in two, and Snowflake Cortex covers both. Cortex Analyst does text-to-SQL against a semantic model for structured data (deals, values, companies). Cortex Search does semantic search over unstructured data (meeting transcripts). The course's key architectural move: Cortex is itself an agent that chooses between its Analyst and Search tools, and the course wraps that whole Cortex Agent as a single LangChain tool, builds a ReAct agent around it, then wraps that as a LangGraph node routing back to the executor, indistinguishable from the other sub-agents. Agents all the way down, with a uniform node interface at each level. The honest failure mode is named: the Cortex agent sometimes picks Search (meeting notes) when Analyst (deals data) was needed.

**Observability:** because data agents fundamentally research and generate, the **RAG triad** maps onto them directly: research steps get context relevance, synthesis gets groundedness, end-to-end output gets answer relevance, all scored by an LLM judge. Implementation is TruLens over OpenTelemetry: tracing enabled via environment flag, a TruSession storing traces and evaluations as events in SQLite, and custom instrumentation decorators on the research nodes emitting RETRIEVAL spans that capture the sub-query text and the retrieved contexts, which is what makes per-step context relevance computable at all. Groundedness compares retrieved contexts (source) against the final answer (statement); answer relevance compares the user query against the final answer; context relevance scores each retrieval chunk against its sub-query and aggregates by mean. The agent graph is registered with TruLens as a named, versioned app, queries are recorded, and a dashboard separates per-query traces from aggregate feedback scores.

## Why it matters
- The triad-over-traces pattern is the Advanced RAG course's framework operationalized on agents: same three judges, now fed by span data instead of a static pipeline.
- Instrumentation is the prerequisite, not an afterthought. No RETRIEVAL spans, no context relevance. The eval design constrains the tracing design.
- The wrap-an-agent-as-a-tool pattern recurs everywhere in production agent systems (and in MCP architectures). Recognizing it is half of reading any agent codebase.

## How I'd use it
- **Roadmap Phase 2 (judge):** my judge harness should consume traces, not just final outputs. Per-step judges on retrieval spans are the design.
- **Tempo-style roles:** an MCP hub wrapping specialist servers is this same nesting pattern. The failure mode to name in interviews: the router picks the wrong specialist tool.
- **Project work:** any agent I build gets retrieval instrumentation from day one, because retrofitting spans is miserable.

## Open questions
- TruLens is the course's stack (the instructor is TruEra's co-founder). The pattern is portable to Phoenix or a hand-rolled harness; the span schema is the part to keep.
