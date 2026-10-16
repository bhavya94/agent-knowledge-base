# Module 1 — Multi-Agent Architecture for Data Work

**Course:** Building and Evaluating Data Agents (DeepLearning.AI, with Snowflake) **Date:** 2026-10-15 **Verdict:** a concrete, opinionated reference architecture. Planner-executor with specialized sub-agents, built in LangGraph.

## What problem?
A single agent with every tool and every data source becomes an undifferentiated blob: hard to prompt, hard to debug, hard to evaluate. Data work also spans heterogeneous sources (structured databases, documents, the live web) that need different handling.

## What idea?
A **data agent** answers questions by connecting to data sources, and the course builds it as a hierarchical multi-agent workflow in LangGraph with three layers:
- **Planner:** decomposes the user query into a numbered sequence of sub-goals, each assigned to a named sub-agent with a described action. Uses a reasoning model with structured JSON output. Prompt discipline: smallest subqueries answerable by a single data source, explicit output schema, replan guidance that prefers simpler unblocking alternatives.
- **Executor:** reads the plan and conversation state, decides which sub-agent acts next, and writes the exact standalone sub-question for it. Its JSON output carries whether to replan, which agent, the reason, and the query. Replanning is capped (MAX_REPLANS=3) so the agent cannot loop forever.
- **Sub-agents:** specialists. A Web Researcher (ReAct agent with web search), a Chart Generator (ReAct agent with a Python REPL that writes and executes chart code), a Chart Summarizer (ReAct, no tools, captions chart images), and a Synthesizer (a direct LLM call composing the final answer from only the worker messages, excluding planner/executor chatter).

State is a custom class extending LangGraph's MessagesState (user query, enabled agents, current step, sub-query, plan, replan bookkeeping). Nodes communicate via the Command pattern, returning state updates plus the next node to visit. Prompt design is treated as a first-class artifact: prompts live in their own file, versioned like code.

## Why it matters
- Planner-executor separation is the crewAI hierarchical pattern implemented in a different framework. The pattern is stable across tools; the implementation details are not.
- The replan cap is a guardrail worth stealing verbatim: bounded replanning prevents the classic infinite-loop failure.
- The synthesizer seeing only worker outputs (not orchestration chatter) is a clean context-hygiene rule.

## How I'd use it
- **Roadmap Phase 3 (harness):** my agent harness gets the planner-executor split with a hard replan cap and a synthesizer that reads only worker outputs.

## Open questions
- LangGraph vs crewAI for this shape: the course does not compare. My take: the framework matters less than the eval discipline in modules 2 and 3.
