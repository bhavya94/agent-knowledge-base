# Module 4 — Collaboration Patterns

**Course:** Multi AI Agent Systems with crewAI (DeepLearning.AI) **Date:** 2026-10-15 **Verdict:** the payoff module. Three complete builds, each a reusable template.

## What problem?
A fixed sequential pipeline does not fit every problem. Long chains also suffer **context fade**: the original goal gets diluted as intermediate outputs pass agent to agent. And some problems need multi-perspective critique (analyst vs strategist vs risk), not a conveyor belt.

## What idea?
**Process is a first-class design decision.** Two patterns:
- **Sequential:** tasks run in order, outputs feed forward. Simple; fine for straightforward pipelines. Watch for context fade on long chains.
- **Hierarchical:** a manager agent holds the overall objective, decomposes and delegates to specialists, reviews results, requests improvements. Switching is roughly a one-line change, so experiment.

Orthogonal to process: agents can delegate to each other and ask questions, going off the predefined path when needed. Async execution stays available under either process.

Three builds (all notebooks downloaded to my workspace):
1. **Event planning** (3 agents: venue coordinator, logistics manager, marketing): the canonical shape. Independent research tasks run async, wired via context into the dependent task; `VenueDetails` Pydantic output for structured venue data.
2. **Financial analysis** (4 agents: data analyst, strategy developer, trade advisor, risk advisor): hierarchical with a manager LLM. Manager quality largely determines the outcome, so use a strong model there. Grounded in live retrieved data (search/scrape), not model memory.
3. **Job application tailoring** (4 agents: researcher, profiler, resume strategist, interview preparer): `FileReadTool` ingests local files (resume, job posting), bridging the crew to the operator's own documents. Context-chained pipeline producing a tailored resume plus interview-prep guide.

## Why it matters
- "Treat process as a deliberate choice" is the staff-level answer to multi-agent design questions.
- The hierarchical pattern generalizes to any domain needing coordinated expert review. My judge work is exactly this: a panel of specialist critics with a synthesizer.
- File-reading tools turn a generic crew into a personal assistant on your own documents. The research-plus-personalization template applies to sales outreach, grant writing, eval dataset curation.

## How I'd use it
- **Roadmap Phase 2 (judge):** hierarchical judge panel. Specialist critics (faithfulness, completeness, tone) under a synthesizer, all grounded in retrieved context.
- **Interview prep:** EvenUp's ambiguous-ML-question round and Cresta's system design both invite a "here is how I would structure the agent team" answer.
- **Course capstone for me:** reimplement the job-application crew against my own resume and a real posting as a build-fast exercise.

## Open questions
- The course claims real Fortune 500 usage of crewAI for financial analysis. Unverified; treat as marketing until I see a case study.
