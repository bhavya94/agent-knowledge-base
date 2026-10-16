# Module 3: Tool Use

**Course:** Agentic AI (DeepLearning.AI, Andrew Ng) **Date:** 2026-10-16 **Verdict:** the module that demystifies function calling. The keeper insight: a tool is mostly its description, and the docstring is what the model actually programs against.

## Lesson 22: What are tools?

(Note: this lesson was captured from slide storyboards; the narration was unavailable in the extraction session. The concepts below are what the slides establish.)

Tools are functions an LLM can invoke to interact with the outside world. The "simple tool execution" architecture diagram shows the loop: user prompt, LLM, a function call (the example is get_current_time()), the result returned to the LLM, then the final output to the user.

An examples table maps natural-language prompts (for example, finding the cheapest flight from Mountain View, CA) to the tool invoked and the output produced. A "multiple tools" diagram extends the pattern: the LLM is given several tools (weather, flight search) and learns to choose the appropriate one per request.

Core concept: tools let LLMs act, retrieving live data and triggering real-world effects, rather than only generating text.

## Lesson 23: Creating a tool

A tool has three ingredients: a description of what it does, an input format the model must conform to, and executable code whose output is returned to the model.

Writing good tool descriptions is like writing good API documentation: describe what the tool does, include example inputs and outputs, and say when to use it. The concrete example is a company-information lookup tool. Its description states that it retrieves detailed company info (domain, industry) via search; an example input/output pair shows the expected JSON shape; and a "when to use" note tells the model to use it whenever the task needs information not already in the conversation (company overview, domain, industry).

Inputs are specified by the model: providers let the model structure arguments within a declared schema. Outputs can be long strings or JSON that the model reads. The interaction pattern: the user asks something the model cannot know from training (for example, a current AI funding round); the model requests a tool call; the application layer runs the code and appends the result as a tool-result message; the model then answers from that context, sometimes over multiple model, tool, model rounds.

## Lesson 24: Tool syntax

The mechanics underneath tool calling. Everything remains text in the conversation history, but the model's output can contain special structured syntax declaring a tool call. Each model provider defines its own input schema and message format. The application layer detects the tool-call syntax, parses the arguments, invokes the function, and appends the tool's result as a new message in the history.

The course deliberately teaches the underlying syntax instead of hiding it behind a framework, so learners understand the mechanism. With function definitions plus docstrings and descriptions, an LLM API can automatically convert them into the provider's native tool format (the videos show OpenAI's; the course notebook uses a local-model library supporting the same standard syntax). After results come back, the model reads them and either answers or issues another tool call; multiple tool calls can appear in one turn, and the loop continues.

Practical note: syntax varies across providers, so hand-coding one provider's schema creates lock-in. Generating the syntax from Python functions and docstrings keeps things portable.

## Lesson 25: Ungraded lab, turning functions into tools (notebook M3_UGL_1)

The notebook uses a local Mistral-based tool-calling helper. A small ChatAgent class wraps the model: its chat() method takes plain chat messages plus a list of tool-callable Python functions, then loops: get the model's response; if it contains tool calls, execute each and append tool messages; repeat until the model gives a final answer, with a max-iterations guard against infinite loops.

First demo: a current-job-openings task. One function returns a mock list of job records; the agent calls it with no arguments and presents a concise summary. A second function filters by company and/or role, letting the agent answer narrower queries, which demonstrates how the model selects arguments. Then docstrings are added to the functions (usage guidance, example invocation) and behavior is compared. The docstring text changes how the model uses the tool: given a vague "what's the weather" request, the agent declines to call the tool when the docstring says a location is required, whereas a default parameter makes it guess "New York".

Exercises: rewrite a docstring to guide interpretation, add a company filter to the search function, extend the chat loop to handle multiple tool calls in one turn. Takeaway: turning a function into a tool is mostly about its description and docstring; that is the channel through which the model decides when and how to call it. Notebook downloaded locally, referenced by name only.

## Lesson 26: Ungraded lab, email assistant workflow (notebook M3_UGL_2)

A ReAct-style email triage agent. An Email dataclass and a mock inbox (get_unread_emails()) of roughly 10 messages spanning categories: work notifications (a failed build), promotions and newsletters (discounts, new releases), suspicious urgent-looking messages (phishing-style), a meeting invitation, and personal notes.

Tools, each wrapped with a @tool decorator: fetch_unread_emails (ID, subject, sender, preview), get_full_email (full body), search_emails (filter by query or folder), send_email (prints to stdout), summarize_email (LLM summary), trash_email (prints). The agent's system prompt prescribes a Thought, Action, Observation loop and defines five categories with handling rules: notify on important or urgent work emails and reply to the failed-build notice by emailing the DevOps team; trash phishing; archive promotions and newsletters; reply to the meeting invite; summarize personal emails.

The executed trace shows multi-step reasoning (fetching previews, opening full bodies, summarizing, searching the inbox, sending notifications, trashing phishing, replying) and also shows a model limitation being worked around: the model initially claims it "cannot reply" and summarizes instead, but the loop is resilient. The run ends with a final summary printing category counts and example messages. Notebook downloaded locally, referenced by name only.

## Lesson 27: Code execution

A second way to give LLMs tools: let the model write code (Python, say) and have it executed in an environment, with results fed back into the conversation.

Motivating case: data analysis over customer reviews. An analyst asks which product categories get poor ratings, which the model cannot answer from memory and must compute over a dataset. Workflow: the model writes code to load the CSV and compute average rating per category; the code executes; the model reads the output and answers, even doing follow-on numeric reasoning (for example, how many more five-star reviews would lift a category's average).

The loop is the same as tool calling: model, code block, execution-result message, model, final answer. Environments can be local or sandboxed cloud runtimes. Caution, stated plainly: running model-generated code has security implications, so use sandboxed environments and control what the code can access. This lesson is the bridge to Module 5's planning with code execution.

## Lesson 28: MCP

MCP (Model Context Protocol, introduced by Anthropic) is an open standard for connecting models to external tools and data sources uniformly, presented as analogous to a USB-C port for AI applications.

The problem it solves: without it, every integration is custom. Each model provider has its own tool syntax and each data source needs bespoke wiring, an N by M problem. MCP defines a client-server protocol: an MCP client lives in the host application (the agent), and MCP servers expose tools, resources, and prompts with standardized schemas. Benefits: an integration written once against the protocol works with any MCP-compatible model or app; servers can wrap databases, APIs, file systems, or browsers; and the ecosystem grows because tool builders and app builders each target one interface.

In course terms, an MCP server is just another way to supply the same three tool ingredients (description, input schema, executable code), discovered and invoked through the protocol rather than hand-wired. This video closes Module 3.

## Not extracted

- Item 29, Module 3 quiz, and item 30, M3 graded lab: graded, membership-gated.

## How I'd use it

- I write tool descriptions like API docs, because that is what they are: what the tool does, an example input and output, and an explicit when-to-use note. When an agent misuses a tool, my first fix is the description, not the prompt around it.
- I treat docstrings as behavior controls. The weather example is the proof: a required location in the docstring makes the model decline vague requests, a default parameter makes it guess. Defaults and required-field wording are policy decisions, and I make them deliberately.
- I generate tool schemas from Python functions and docstrings rather than hand-writing provider JSON, so swapping providers or models does not mean rewriting every tool definition.
- Code execution is my escape hatch when the tool set keeps growing edge cases: give the model a dataset and a sandbox instead of a new bespoke function per question. Sandbox first, always, with controlled access; the course's caution on this is not boilerplate.
- For anything I expect to reuse across projects, I reach for MCP servers instead of hand-wired integrations, so the same tool surface works across hosts and models.
- In an eval harness, tool use splits into two gradeable questions, did the agent pick the right tool, and did it pass the right arguments, and the email-assistant lab's category rules are a good model for writing those checks as explicit handling rules rather than vibes.
