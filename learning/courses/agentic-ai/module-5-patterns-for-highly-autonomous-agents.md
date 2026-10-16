# Module 5: Patterns for Highly Autonomous Agents

**Course:** Agentic AI (DeepLearning.AI, Andrew Ng) **Date:** 2026-10-16 **Verdict:** powerful patterns with the costs stated honestly. Planning and multi-agent buy generality and pay for it in predictability; the module's job is to teach when that trade is worth making.

## Lesson 40: Planning workflows

Module 5 covers systems where the agent decides its own steps instead of the developer hard-coding the sequence. First pattern: planning (multi-agent comes later in the module).

Motivating example: a sunglasses retailer. A customer asks for round sunglasses in stock under $100, which needs product-description lookup, inventory checks, and price filtering. The agent is given tools (get item descriptions, check inventory, process item returns, get item price, check past transactions, process item sale) and prompted with "You have access to the following tools..." plus an instruction to return a step-by-step plan. Resulting plan: (1) get item descriptions to find round sunglasses, (2) check inventory, (3) get item price to filter under $100. Execution: each plan step plus context (tools, user query, background) is fed to an LLM that carries it out, typically by calling a tool; each step's output feeds the next until the final output becomes an answer. (Real plans are more detailed than these simplified one-liners.)

The payoff is generality: a different request (returning gold-frame, not metal-frame, glasses) produces a different plan (check past transactions, get item descriptions, process the return), so one planning agent handles a wide range of tasks with many tools in many orders. Second example: an email assistant handling a dinner invitation from "Bob Mould" (search email, draft and send a confirmation, archive the thread).

Status check: planning is already proven in highly agentic coding systems, but outside coding it remains more experimental and harder to control, since the developer cannot know at runtime what plan will be produced. Adoption is growing anyway.

## Lesson 41: Creating and executing LLM plans

Plan representation: how to get an LLM to emit plans that downstream code can execute reliably. Recommended practice: ask for the plan in JSON, because downstream code can parse steps clearly and unambiguously, and current leading models generate JSON well.

System prompt pattern: "You have access to the following tools..." plus an instruction to create a step-by-step plan in JSON format, with the schema described in enough detail. The JSON is a list whose items carry the step description, the tool to use, and the arguments to pass, so an executor can walk the steps systematically; later steps' arguments can reference earlier results (the second step's arguments cite "results from step 1").

Format comparison: XML with delimiters and tags is also a good option; Markdown is slightly more ambiguous to parse; plain text is least reliable. Either JSON or XML is recommended. The lesson ends by teeing up the next idea: letting the LLM write code, with the code itself expressing the plan.

## Lesson 42: Planning with code execution

The alternative to JSON plans: have the LLM write code, where the code itself captures multiple plan steps, so executing the code carries out a fairly complex plan.

Example: answering questions about coffee-machine sales from a spreadsheet. With only fixed tools (get column max/mean/min/median, filter rows, sum rows), a query like "which month had the highest sales of hot chocolate?" becomes a long, brittle twelve-iteration procedure, and some queries are impossible without inventing new tools (counting unique transactions last week needs a new get_unique_entries tool). Teams that keep adding tools for edge cases end up with brittle tool soup.

Better approach: prompt the model to "write code to solve the user's query and return your answer as Python code" (delimited, for example with execute-python XML tags). The LLM loads the spreadsheet into pandas; the code is the plan: parse the date column, sort, select the last five transactions, show prices. This works because Python plus libraries like pandas give the LLM an enormous vocabulary of functions it has seen extensively in training, composable into plans for complex queries. A second query (unique transactions last week) yields code whose comments reveal a four-step plan: read CSV, parse dates, define the time window, filter, drop duplicates, count.

Caveat: generated code needs a safe sandboxed execution environment, a step many developers skip though it is not best practice.

Research evidence (diagram adapted from a paper by Xinyao Wang and colleagues): a bar chart comparing successful task-completion rates across eight models (gpt-4-1106-preview, gpt-4-0613, claude-2, two gpt-3.5-turbo variants, gemini-pro, text-davinci-003, Llama-2-70b-chat-hf). For every model, Code as Action outperforms JSON as Action, which outperforms Text as Action: roughly 75% vs 55% vs 50% on gpt-4-1106-preview.

Wrap-up: the most powerful current use of planning is agentic coding assistants that make detailed build-and-test checklists and execute them step by step; outside coding, planning is still maturing. The trade-off is control: you give up prescribing exact behavior, so runtime behavior is less predictable, but the range of things the model can attempt grows.

## Lesson 43: Ungraded lab, customer service agent (notebook M5_UGL_1_R)

A Jupyter notebook implementing planning with code execution for a simulated sunglasses store. It builds small inventory and transaction datasets with an inv_utils helper module (create_inventory, create_transactions, seed_db, build_schema_block, get_current_balance, next_transaction_id), stored in TinyDB, a lightweight pure-Python document-oriented DB using JSON documents. Two tables: inventory_tbl (item_id, name/style, description, quantity_in_stock, price) and transactions_tbl (transaction_id, customer_name, transaction_summary, transaction_amount, balance_after_transaction, timestamp).

Core loop: generate_llm_code() builds a live schema block from the tables, formats the prompt, calls the model (o4-mini), and returns a response containing an <execute_python> code block; execute_generated_code() extracts that block, runs it in a controlled namespace with the TinyDB tables and safe helpers, and captures stdout, errors, and answer variables while rendering before/after table snapshots. Worked scenarios: a read-only query ("round sunglasses in stock under $100?") and a mutation ("return 2 Aviator sunglasses," which inserts a transaction and moves stock from 23 to 25). A customer_service_agent() function ties generation and execution together; "Try It Out" prompts cover single-item, return, and multi-item purchases, and reseed=True resets the demo data.

Takeaways: let code be the plan; prefer the rich, familiar Python and TinyDB toolbox over brittle tool soup; keep runs safe and visible via a controlled namespace, captured logs and errors, and before/after snapshots. Notebook downloaded locally, referenced by name only.

## Lesson 44: Multi-agentic workflows

A multi-agent workflow is a collection of multiple agents collaborating, as opposed to a single agent doing everything. Organizational analogy: just as developers decompose work on one machine into processes or threads to make code easier to write, complex tasks decompose naturally into roles; hire a team rather than one person. Examples: marketing assets (researcher, graphic designer, writer), a research article (researcher, statistician, lead writer, editor), a legal case (associates, paralegals, investigator).

Running example, a sunglasses summer-marketing campaign: a researcher agent (web-search tools) analyzes market trends and competitors; a graphic designer agent (image-generation APIs, or code execution to produce charts) creates visuals; a writer agent (plain LLM text generation, no tools needed) writes the brochure. Each agent is built by prompting an LLM into its role ("you are a research agent, expert at analyzing market trends...").

The simplest topology is linear: the researcher's report feeds the graphic designer, whose assets feed the writer, who produces the final brochure. Advantages: each agent focuses on one thing, different collaborators can build agents in parallel, and agents can be reused or generalized (a brochure designer generalized to social posts or webpage illustrations).

Beyond linear, an orchestrator (manager) agent can plan with agents as its "tools": prompted as "a marketing manager" with descriptions of its team, it writes a step-by-step plan (research, then design, then write, then a reflection step to review and improve) and executes it by calling on each agent in turn, making the orchestrator itself a fourth agent.

Key design decision for multi-agent systems: the communication pattern between agents, an active research area covered in the next video.

## Lesson 45: Ungraded lab, market research team (notebook M5_UGL_2)

A Jupyter notebook building a four-agent creative pipeline for a sunglasses summer campaign, framed as the work of a technical AI lead at a fashion brand. Tools are declared upfront so the action space is unambiguous: tavily_search_tool for live web search and product_catalog_tool for the internal sunglasses catalog.

The agents: (1) Market Research Agent: scans the web for trends and cross-checks the catalog, returns a brief with top insights and matching products. (2) Graphic Designer Agent, in two stages: o4-mini crafts an image prompt plus caption, gpt-image-1-mini generates the image. (3) Copywriter Agent: multimodal, taking the generated image and trend summary to produce a quote plus a short justification. (4) Packaging Agent: compiles everything into an executive-ready Markdown report (trend summary, styled image with quote overlay, justification, timestamp) saved to ./campaign_report.md. A run_sunglasses_campaign_pipeline() function chains the agents end to end, and a "Try It Out" section executes the full pipeline.

Takeaways: multi-agent LLM pipelines can automate a creative workflow end to end; they combine reasoning, tool-calling, and external data; multimodal models let agents process text and images together; tools extend what agents can do; transparent, debuggable execution ends in an executive-ready artifact. Notebook downloaded locally, referenced by name only.

## Lesson 46: Communication patterns for multi-agent systems

Designing how agents communicate is as complex as designing a human org chart. Four patterns, in order of complexity:

1. **Linear:** agents work a fixed sequence, each handing its output to the next (researcher, graphic designer, writer). One of the two most common patterns in practice.
2. **Hierarchical:** a manager agent assigns tasks and coordinates the work, with team members reporting back to the manager, who routes results onward. Implementation guidance: channel results through the manager rather than letting team members message one another directly. Also one of the two most common patterns.
3. **Deeper hierarchy** (advanced, less used): the manager's team members themselves have sub-agents. The researcher oversees a web researcher and a fact checker; the writer oversees an initial style writer and a citation checker. Nesting is more complex and used less often.
4. **All-to-all:** any agent can contact any other agent at any time. Implemented by prompting every agent that it may call on the others, and delivering messages by inserting them into the receiving agent's context; the group collaborates until each agent declares itself done (or the writer judges the output good enough). Behavior is hard to predict, so the pattern is still somewhat experimental and best suited to applications that can tolerate unpredictability (if the brochure is not good, just run it again).

Software frameworks now exist that make implementing these patterns relatively easy. The practical ladder: default to linear or single-manager hierarchical patterns for controllable, predictable systems, and reserve deeper hierarchies and all-to-all communication for cases where their complexity is justified.

## Lesson 49: Conclusion

A recap of the full course, module by module. Module 1: applications of agentic AI that were not possible before this technology. The core design patterns: reflection highlighted as a simple technique that delivers a noticeable performance boost; tool use (function calling) framed as the capability that expands what language-model applications can do, with code execution called out as a particularly important special case of tool use.

Module 4 (evals, error analysis, and the disciplined build-and-analyze development process) is singled out as some of the most useful content in the course for anyone who will keep building agentic AI systems long-term: systematically measuring performance and prioritizing fixes is what converts prototypes into reliable products. Module 5's planning and multi-agent techniques are acknowledged as more powerful but also harder to control and harder to predict, a clear-eyed trade-off rather than a pure upgrade. The lesson also notes that these skills are assessed in job interviews.

The course's prioritized mental model, worth keeping whole: get the basics (decomposition, reflection, tools) working, lean on evals and error analysis as the engine of improvement, and treat high-autonomy patterns (planning, multi-agent) as power tools to adopt deliberately, with their predictability costs in mind.

## Lesson 50: Acknowledgments (reading)

Credits page. Instruction and course design: Andrew Ng, Tommy Nelson, Brendan Brown. Curriculum development: Daniel Villarraga, Lesly Zerna, Hesus Garcia. Lab development and engineering: Elias Nino-Ruiz, Andres Zarta, Ryan Chen, Sherry Lin, Joe Chen, Jerry Huang. Alpha testing and mentorship: Giovanni Lignarolo. Thanks also to the alpha testers and the learners.

## Not extracted

- Item 47, Module 5 quiz, and item 48, M5 graded assignment (Agentic Workflows): graded, membership-gated.

## How I'd use it

- Planning earns its place when the task mix is too varied to hard-code: one agent, many tools, requests arriving in unpredictable shapes. If the workflow is fixed, I keep the fixed workflow; planning's generality is wasted there and its unpredictability is pure cost.
- Plans default to JSON with an explicit schema (step, tool, args, with later args allowed to reference earlier results). The moment the action space needs loops, conditionals, or data manipulation, I switch to code as the plan and lean on pandas-style libraries instead of growing a tool set one edge case at a time. The 75% vs 55% vs 50% chart is the evidence I cite for that ordering.
- Any code-executing agent I build runs in a sandbox with a controlled namespace, captured stdout and errors, and before/after state snapshots, copied from the customer service lab's shape. Skipping the sandbox is the course's named anti-pattern.
- Multi-agent designs start linear. I add an orchestrator only when task routing itself needs judgment, keep results flowing through the manager, and treat all-to-all as an experiment for rerun-tolerant outputs, never for anything with side effects I cannot undo.
- For eval work, autonomous systems raise the grading problem: the plan itself becomes an artifact to evaluate (is the plan valid, minimal, executable?) alongside step-level and end-to-end checks. In a red-team harness, planning and all-to-all communication are where I would concentrate adversarial cases, because that is where the developer's control is thinnest.
