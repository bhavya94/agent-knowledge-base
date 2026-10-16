# Agentic AI

**Source:** DeepLearning.AI course, taught by Andrew Ng. **Date distilled:** 2026-10-16. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://www.deeplearning.ai/courses/agentic-ai

## Verdict

Andrew Ng's course on building agentic workflows, and the part that sticks is not the patterns, it is the process. His central claim: the biggest difference between people who build agentic workflows well and poorly is not prompt cleverness, it is a disciplined development loop of evals and error analysis. The patterns (reflection, tool use, planning, multi-agent) are the vocabulary; Module 4's build-and-analyze loop is the actual skill. This is the course that most directly feeds my agent eval harness work.

## The course in one page

An agentic AI workflow is a process in which an LLM-based application executes multiple steps to complete a task, instead of answering in a single forward pass. Ng's running analogy: one-shot generation is writing an essay without ever using backspace. The agentic version drafts an outline, does research, writes, reads it back, and revises. Three mental models organize everything:

- **Degrees of autonomy.** Autonomy is a dial, not a binary. At one end the developer hard-codes every step and the LLM plays a small role in a fixed pipeline (invoice processing); at the other, the agent decides its own plan and step sequence (a research agent). Plot task complexity against autonomy on a 2x2 grid and you get a scoping tool: high complexity plus high autonomy is the hardest quadrant to build reliably, and more autonomy always multiplies failure modes.
- **Four design patterns.** Reflection (the model critiques and revises its own output), tool use (the model decides when to call functions, search, or code execution), planning (the model writes an explicit multi-step plan, then executes it), and multi-agent collaboration (specialized agents with distinct roles working together). Real systems combine them; the research agent uses planning plus tool use plus a reflection-like editor step.
- **The build-and-analyze loop.** Build a rough end-to-end prototype, examine traces, measure with evals, run error analysis to find the weakest component, improve that component, repeat. Analysis (evals, error analysis) is half the loop and the half inexperienced teams skip. Get quality right first; latency and cost optimization come last.

Why bother: Ng's performance chart shows an agentic loop sitting substantially above direct prompting at every model generation, with the gap widening as base models improve. Better models amplify agentic workflows rather than replacing them.

## Modules

1. [Introduction to Agentic Workflows](module-1-introduction-to-agentic-workflows.md): what agentic AI is, degrees of autonomy, benefits, applications, task decomposition, first look at evals, the four design patterns.
2. [Reflection Design Pattern](module-2-reflection-design-pattern.md): reflection vs direct generation, chart generation, measuring reflection's impact (87% vs 95%), external feedback, reflection grounded in execution results.
3. [Tool Use](module-3-tool-use.md): what tools are, the three ingredients of a good tool, tool syntax under the hood, code execution, and MCP as the standard connector.
4. [Practical Tips for Building Agentic AI](module-4-practical-tips-for-building-agentic-ai.md): evals, error analysis with real percentages, component-level evals, the fix repertoire, latency and cost, the development process summary.
5. [Patterns for Highly Autonomous Agents](module-5-patterns-for-highly-autonomous-agents.md): planning workflows, JSON plans, planning with code execution (Code as Action beats JSON beats Text), multi-agent workflows, communication patterns.

## Key takeaways

- Decompose tasks by shadowing a human doing them; do not aim for the perfect workflow on the first try, the eval loop will improve it.
- Reflection is cheap to implement and reliably helps, but verify it with evals, because it costs latency. Reflection grounded in external feedback (executed queries, tool results) beats introspection alone.
- A tool is mostly its description. The docstring is the channel through which the model decides when and how to call it.
- Start with end-to-end evals, even quick and dirty ones over 10-20 examples. When the system visibly improves but the score does not move, the eval is stale, not the system.
- Error analysis means counting: attribute failures to components, tabulate percentages, fix the biggest bucket you have a remedy for.
- Code as Action outperforms JSON plans, which outperform text plans. Python plus libraries like pandas is a bigger, more composable action vocabulary than any hand-built tool set.
- Default multi-agent systems to linear or single-manager hierarchical communication. All-to-all is experimental and unpredictable by design.

## How this connects to my roadmap

- **Agent eval harness project:** Module 4 is the blueprint. End-to-end evals first, traces and spans for diagnosis, error analysis to pick the component, component-level evals for a tight improvement loop, rubric-based judges with binary criteria instead of one vague 1-5 score. This is the development discipline the harness has to support.
- **reflective-qa project:** Module 2 is the theory behind it. My reflection agent (writer, critic, one revise round) found that critics fixed some errors while rewording correct answers lost points elsewhere; Ng's framing explains why measuring the delta (his 87% vs 95% SQL example) matters more than assuming reflection helps, and his external-feedback lesson points at grounding the critic in verifiable signals rather than pure self-critique.
- **Red-team harness project:** the degrees-of-autonomy grid is a scoping tool for it. Higher autonomy multiplies failure modes, so the harness should concentrate adversarial pressure where autonomy and task complexity are both high, and the all-to-all communication pattern is the obvious stress case.

## Notebooks

Seven ungraded lab notebooks were downloaded locally and are referenced by name only in these notes, never committed (course IP): M2_UGL_1 (chart generation), M2_UGL_2 (SQL generation with reflection), M3_UGL_1 (turning functions into tools), M3_UGL_2 (email assistant workflow), M4_UGL_1 (component-level eval), M5_UGL_1_R (customer service agent), M5_UGL_2 (market research team). The patterns above capture what matters from each.

## Coverage caveats

- The course has 50 syllabus items: 31 videos, 8 ungraded code examples, 3 readings, 5 graded quizzes, and graded labs/assignments. All video lessons and all seven downloadable ungraded notebooks are covered in these notes.
- Graded quizzes and graded labs sit behind the course membership and were not extracted; each module file notes them in one line.
- Item 11, "Try the research agent" (Module 1 code example), is also membership-gated and could not be retrieved; the research agent itself is described in detail in the Module 1 videos.
- Item 12 (join the course forum) is administrative and is not distilled.
- Two lessons rest on partial sources: item 22 (What are tools?) was captured from slide storyboards only, and items 17 and 18 were first captured slide-only, then re-extracted from full transcripts in a gap-fill pass, which is the version used here.
