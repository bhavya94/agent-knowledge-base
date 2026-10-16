# Module 2 — Tools

**Course:** Multi AI Agent Systems with crewAI (DeepLearning.AI) **Date:** 2026-10-15 **Verdict:** the most transferable module. Tool design principles outlive any framework.

## What problem?
Without tools an agent is a text generator. With bad tools it is a text generator that fails slowly: exceptions kill runs, redundant calls burn rate limits, and a confused agent picks the wrong tool.

## What idea?
Three properties of a great agent tool:
1. **Versatile:** fuzzy LLM inputs in, strongly-typed behavior out. One search tool handling many query types beats five single-purpose gadgets.
2. **Fault-tolerant:** exceptions are reported back to the agent for retry instead of crashing the run. crewAI's deliberate design decision: a tool exception never stops execution. The course showed an agent calling a file tool on a URL, getting the error back, and recovering via web search.
3. **Caching:** cross-agent cache on repeat calls. Saves rate limits and makes crews faster.

Mechanics: **custom tools** subclass `BaseTool` with a name, a description (the description is what tells the agent *when* to use it), and a `_run` method. **Agent-level tools** are available to everything an agent does; **task-level tools** scope to one task and override.

## Why it matters
- The tool description as a routing signal is the same mechanism as MCP tool definitions and function-calling schemas. Writing good descriptions is writing good agent UX.
- Fault tolerance as a framework-level choice (never crash on tool error) is a production reliability pattern, not just a demo convenience.
- Caching across agents is a free latency/cost win in any multi-step system.

## How I'd use it
- **Roadmap Phase 3 (harness):** my agent harness tool definitions should carry the same discipline: precise descriptions, typed inputs, graceful errors returned to the agent.
- **Project 01 (extraction eval lab):** the extraction tools get the versatility/fault-tolerance treatment; measure how often the agent recovers vs gives up.

## Open questions
- None. This module was complete.
