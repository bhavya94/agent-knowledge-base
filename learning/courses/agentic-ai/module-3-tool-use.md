# Module 3 — Tool Use

**Course:** Agentic AI (DeepLearning.AI)  **Date:** 2026-10-11

## What problem?
An LLM on its own can only produce text. To act or fetch fresh facts (search, run code, query a database,
call an API), it needs a reliable way to know which tools exist and to request a call in a form a program can execute.

## What idea?
- **Then:** earlier models had tool names and the calling syntax written into the prompt. The application parsed
  the model's free-text output to work out which tool to run and with what arguments.
- **Now:** tools are a structured API parameter. Each tool is described by a JSON schema: name, description,
  and typed parameters. Libraries can generate that schema directly from a function. The model reads the
  schemas, decides whether and which tool to call, and returns a structured JSON tool call. The application
  executes it and feeds the result back.
- **MCP (Model Context Protocol):** products publish ready-made tools through MCP servers. Agents can use
  them directly, without anyone writing and maintaining a tool wrapper for each product.

## Why it matters
- **Reliability:** structured tool calls replace brittle parsing of free-form text.
- **The description is the interface:** the model picks tools from their names and descriptions, so a vague
  description leads to wrong or missed calls. Writing tool descriptions is effectively prompt engineering.
- **Reuse:** MCP turns integration into configuration. That saves engineering time, but you inherit the
  provider's tool design, and you're trusting their server with your data and actions.

## How I'd use it
- **Roadmap Phase 3 (agentic judge):** give the judge an evidence-lookup tool, so it checks claims against the
  paper instead of trusting the answer's citations. Compare it against the plain judge on agreement and cost.
- **reflective-qa M3:** the code checks (F1, quote-in-context, unanswerable) could be exposed as tools the critic
  calls, rather than run as a fixed pre-step. That's worth trying only if M4 shows the fixed pipeline falls short.
- **Learning queue — decision models:** tool selection is the decision those models aim to make fast and cheap.

## Open questions
- How many tools can you offer before tool-selection accuracy drops? When should you route to a subset instead?
- How do you evaluate tool choice itself (right tool, right arguments), separately from the final answer?
