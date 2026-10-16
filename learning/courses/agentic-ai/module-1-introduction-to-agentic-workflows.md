# Module 1: Introduction to Agentic Workflows

**Course:** Agentic AI (DeepLearning.AI, Andrew Ng) **Date:** 2026-10-16 **Verdict:** the framing module. Degrees of autonomy and task decomposition are the two ideas I will reuse constantly; the rest is a map of the course.

## Lesson 1: Welcome!

Ng notes he coined the term "agentic" for a fast-growing way of building on base AI models. Marketers then plastered the label on nearly everything and hype skyrocketed, but genuinely valuable agentic applications have grown rapidly alongside the hype. Applications previewed: customer-support agents, deep-research agents that write reports, legal-document processing, systems that take patient input and suggest possible medical diagnoses. On his own teams, many projects would have been impossible without agentic workflows.

The central thesis, stated up front: the biggest difference between people who build agentic workflows well and poorly is not prompt cleverness but a disciplined development process centered on evals and error analysis. Mastering that process is the point of the course.

## Lesson 2: What is agentic AI?

The contrast that defines everything else. One-shot generation ("write an essay on topic X" in a single pass) is like writing an essay without ever using backspace. Models do surprisingly well under that constraint, but it is not how humans do their best work. The agentic loop instead: draft an outline, do web research, write a first draft, read it back, decide what needs revision or further research, revise.

Definition: an agentic AI workflow is a process in which an LM-based application executes multiple steps to complete a task. The running example is a research agent (topic: building a rocket company) that plans its research, calls a web-search API, downloads pages, synthesizes and ranks findings, drafts an outline, has an editor agent check coherence, and produces a comprehensive Markdown report. An optional human-in-the-loop step has the model request human review of key facts before finalizing. Multiple sources plus deep reasoning produce far more thoughtful output than a single-pass essay.

Ng has built specialized research agents for legal compliance, healthcare, and business research, but he stresses that much simpler, less autonomous workflows are also extremely valuable. The key skill introduced here is task decomposition, covered properly in Lesson 6.

## Lesson 3: Degrees of autonomy

Agents vary in autonomy. The research agent is highly autonomous: it decides its own plan and step sequence. Other agents are far less autonomous: the engineer hard-codes the steps and the LLM plays a small role in a fixed pipeline. The split between hard-coded steps and LLM-decided steps is a deliberate design choice, not a default.

The framework is a 2x2 matrix. Vertical axis: task complexity. Horizontal axis: degree of autonomy, meaning how much the developer trusts the agent to decide on its own. Plotting an application on the grid gauges its difficulty. High complexity plus high autonomy (the research agent) is hardest but most interesting; low complexity plus low autonomy (invoice processing, fixed steps, small LLM role) is easiest to build reliably.

My takeaway: choose the autonomy level deliberately. More autonomy unlocks capability but multiplies failure modes, and the grid is a scoping tool for estimating difficulty before committing to build.

## Lesson 4: Benefits of agentic AI

The centerpiece is a performance chart comparing approaches as base-model capability improves, with successive model generations on the x-axis. The non-agentic curve (prompt the LLM for the final answer directly) rises slowly. The agentic curve (the model wrapped in an agentic loop) sits substantially higher, and the gap widens as models improve. Conclusion: agentic reasoning is likely to remain important even as models grow more powerful; better models amplify agentic workflows rather than replacing them.

His framework for finding applications: look for work with these characteristics: knowledge work, creativity, decision-making, interaction with people, and tasks requiring many steps. Where these cluster, AI adds the most value. His teams applied this lens to invoice processing, legal document review, medical diagnosis assistance, and customer support.

## Lesson 5: Agentic AI applications

Invoice processing as a concrete, simple agentic workflow. The example document on screen is an invoice from TechFlow Solutions LLC for $3,000, due August 20, 2025. Workflow steps: convert the PDF to Markdown, use an LLM to determine whether the document is actually an invoice, extract the required fields, record them in a database.

A companion slide distills it to two essential steps: (1) identify the required fields, (2) record them in the database. The four required fields: Biller, Biller address, Amount due, Due date. The pattern underneath: the human specifies the fields up front, the LLM handles the judgment-laden extraction, and deterministic code handles conversion and storage.

Methodological lesson: many business processes decompose this way. Prefer tasks with crisp, verifiable success criteria when starting out, because you can tell objectively whether the workflow got the right answer, which also makes them easy to evaluate (this foreshadows the evals lesson).

## Lesson 6: Task decomposition: identifying the steps in a workflow

The practical "how" of decomposition. The essay example again, as a diagram: the non-agentic baseline is a single box (prompt, LLM, document, everything in one forward pass with no chance to reconsider) versus the agentic decomposition (outline, research, draft, critique, revise). More decompositions: a customer-email workflow (1. read the email and determine intent, 2. search the codebase for relevant context, 3. draft the response), where some steps are LLM-driven and some deterministic. Invoice processing needs only two steps. Workflows vary in granularity and in the hard-coded vs model-driven mix.

Four building-block questions for designing any workflow:

1. What are the steps to get done?
2. What information does each step need?
3. What context must be provided?
4. What tools are available (web search, code execution, databases, APIs)?

Practical advice: do not overthink the initial decomposition. Shadow a human performing the task and note their discrete steps. Do not aim for the perfect workflow on the first try, because the eval-driven iteration process taught later will improve it.

## Lesson 7: Evaluating agentic AI (evals)

The development-process principle: start with an end-to-end evaluation of the whole system. A single top-level number is the leading indicator of whether you are making progress. Evals plus error analysis form the disciplined loop from Lesson 1.

Three evaluation methods:

- **Human evaluation:** the gold standard, but slow and expensive.
- **LLM-as-a-judge:** prompt a model to grade outputs against stated criteria; fast, cheap, scalable. The narration walks through a judge prompt for the invoice task, checking the extracted fields.
- **Code-based checks:** deterministic tests for what can be verified mechanically.

Recommendation: use multiple methods and track metrics over time. Caveats: evals must be representative of real usage, or optimizing them will not move real-world performance; and the eval itself should be iterated on, not treated as fixed. This end-to-end eval is only the start; component-level evals arrive in Module 4.

## Lesson 8: Agentic design patterns

Four reusable design patterns, each illustrated with its own diagram:

1. **Reflection:** an LLM examines its own output and iterates. Example: generate code, execute it, feed the error message back, fix the bug.
2. **Tool use:** give the LLM tools (web search, code execution, calculators, APIs) and let the model decide when to invoke them.
3. **Planning:** the LLM first devises an explicit multi-step plan, then executes it, as the research agent does.
4. **Multi-agent collaboration:** multiple agents with distinct roles work together. Illustrated by ChatDev, a virtual software company where CEO, programmer, tester, and designer agents converse to build software.

The patterns are not mutually exclusive; real systems combine them (the research agent uses planning plus tool use plus a reflection-like editor step). Each pattern gets a full module later: reflection in Module 2, tool use in Module 3, planning and multi-agent in Module 5. Practical message: reach for these patterns as starting templates rather than designing from scratch.

## Lesson 9: Set up your local environment for the ungraded labs (reading)

Setup guide for running the ungraded labs locally. Requirements: Python 3.10+, with a virtual environment recommended. The requirements.txt package set spans agent and LLM tooling (aisuite pinned at 0.1.11, anthropic, openai, mistralai, tavily-python, docstring-parser, markdown, textstat, vertexai), a web and API stack (fastapi, pydantic, python-dotenv, requests, sqlalchemy, uvicorn), notebook tooling (ipywidgets, jupyter_server, notebook), and optional data extras (duckdb, pandas, matplotlib, seaborn, scikit-learn, tinydb, Wikipedia).

It also explains downloading lab files from the platform: open the lesson with the code, find the embedded Jupyter notebook, use File, Open, and download the notebook plus everything it depends on (helper scripts, config files, data files). Emphasis: do not forget the dependency files or the labs fail locally.

## Not extracted

- Item 10, Module 1 quiz: graded, membership-gated.
- Item 11, "Try the research agent" (code example): membership-gated, could not be retrieved. The agent itself is the running example in Lessons 2 and 8 above.
- Item 12, join the DeepLearning.AI forum: administrative reading, not distilled.

## How I'd use it

- The degrees-of-autonomy grid goes at the front of any agent project I scope. Before writing code, I place the system on the complexity-by-autonomy grid and let that placement decide how much evaluation and guardrail effort the project needs up front.
- Task decomposition by shadowing is my default first step for a new workflow: watch the human process, write down the discrete steps, answer the four building-block questions per step, and only then decide which steps are LLM-driven and which stay deterministic.
- For first projects in a new domain, I copy the invoice-processing bias: crisp, verifiable success criteria, a small field set specified by a human, judgment work to the LLM, storage and conversion to plain code. If I cannot state how success is checked, the workflow is not ready to build.
- The essay-without-backspace framing is the one-liner I use to explain to anyone why a single prompt is the wrong default for multi-step work.
