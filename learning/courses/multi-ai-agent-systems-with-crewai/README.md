# Multi AI Agent Systems with crewAI

**Source:** DeepLearning.AI short course, taught by João Moura (crewAI founder/CEO), intro by Andrew Ng. **Date distilled:** 2026-10-15. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://learn.deeplearning.ai/courses/multi-ai-agent-systems-with-crewai

## Verdict
Foundational vocabulary plus three reusable build templates. The mental models (manager mindset, process as design choice, tool design principles) are the durable part; the crewAI API specifics are already dated (course uses GPT-3.5/GPT-4 era defaults). Modules 2 and 4 are the ones I would re-read.

## Modules
1. [Agents and Roles](module-1-agents-and-roles.md) — agent anatomy (role/goal/backstory, focus, tools, cooperation, guardrails, memory), the manager mental model.
2. [Tools](module-2-tools.md) — versatile, fault-tolerant, cached tools; custom `BaseTool`; agent-level vs task-level scoping.
3. [Tasks](module-3-tasks.md) — description + expected output + agent; async execution; context chaining; Pydantic/JSON structured outputs.
4. [Collaboration Patterns](module-4-collaboration-patterns.md) — sequential vs hierarchical process; three builds: event planning, financial analysis, job-application tailoring.

## Key takeaways
- Design like a manager: define the outcome, staff the roles, equip them, choose how they collaborate.
- Role-playing with a backstory is a near-free performance lever.
- Tool descriptions are routing signals; write them like API docs.
- Structured outputs (Pydantic) are the interface between fuzzy agents and deterministic code.
- Hierarchical process with a strong manager model for anything needing multi-perspective critique.

## Builds to steal
- **Event planning crew:** async research + context chaining + Pydantic outputs. Template for any parallel-then-synthesize pipeline.
- **Financial analysis crew:** hierarchical expert team (analyst, strategist, advisor, risk). Template for my judge panel work.
- **Job application crew:** FileReadTool bridging agents to local documents.

## Notebooks
Six course notebooks (research article, customer support, outreach, event planning, financial analysis, job application) downloaded locally. Not committed here; they are course IP. The patterns above capture what matters.
