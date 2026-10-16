# Module 2: Reflection Design Pattern

**Course:** Agentic AI (DeepLearning.AI, Andrew Ng) **Date:** 2026-10-16 **Verdict:** the highest value-per-line-of-code pattern in the course, with the right warning attached: measure it, because reflection costs latency and does not always help.

## Lesson 13: Reflection to improve outputs of a task

Reflection, defined plainly: after the model produces an initial output, it is prompted a second time to critique and improve its own output before anything is shown to the user.

Main demo: drafting an email about a new AI startup's product launch. The first draft is serviceable but generic. The post-reflection version adds concrete specifics: a named launch event with venue and date, guest speakers, live demos, an RSVP call to action. Second demo revisits a coffee-machine-sales visualization: the first attempt is a stacked bar chart with a confusing color mapping and legend; a reflection prompt asking whether the plot clearly answers the question leads to a much clearer single-color bar chart.

Ground rules stated here and repeated all module: reflection usually but not always improves quality; it adds an extra step and therefore latency; implementation effort is small, but weigh the quality gain against the slowdown and use evals to decide whether to keep it.

## Lesson 14: Why not just direct generation?

"Direct generation" means prompting an LLM once and taking its first output in a single pass. It is also called zero-shot prompting (no examples in the prompt; contrast one-shot, one example, and few-shot, several examples).

Core claim: adding a reflection step reliably beats direct generation. The lesson cites research by Madaan et al. showing reflection outperforming direct generation across multiple tasks and models (GPT-3.5 and GPT-4). Reflection is especially valuable for structured outputs (HTML tables, complex JSON), multi-step instruction sequences, and open-ended creative tasks.

Applied example: on Ng's teams, reflection was used to brainstorm company and product domain names, asking the model to check candidates for awkward pronunciation and unintended negative connotations. Two reusable reflection prompt templates are shown: one reviewing domain-name candidates against explicit criteria, one reviewing a draft email (tone, factual claims, promises made) before producing the next draft.

Practical tips: explicitly instruct the model to review and reflect on its first draft rather than hoping it self-corrects, and give clear, specific review criteria. General prompt-engineering tip worth keeping: reading other practitioners' prompts in open-source projects is a fast way to improve.

## Lesson 15: Chart generation workflow

Reflection applied to generating matplotlib charts of a patient's exercise habits over 12 months. A single direct-generation attempt produces a broken chart: overlapping, illegible text and labels.

The reflection workflow:

1. Generate an initial chart.
2. Ask the LLM to critique the chart image against explicit visual criteria ("Are all text, labels, and numbers legible? Do any visual elements overlap?").
3. Have it write concrete feedback.
4. Generate a revised chart incorporating the feedback.
5. Repeat until the chart meets the criteria.

This works because modern LLMs accept image inputs and can reflect on visual artifacts, not just text. After a few iterations the chart becomes clean and publication-quality. Takeaway: decomposing a task and adding a reflection loop lets LLMs accomplish things they do poorly in a single shot.

## Lesson 16: Ungraded lab, chart generation (notebook M2_UGL_1)

The Lesson 15 workflow as code: generate chart code via an LLM, render it, feed the image back to the model with legibility and overlap criteria, iterate on the code until the visual passes review. An automated reflection loop over chart code. Notebook downloaded locally, referenced by name only.

## Lesson 17: Evaluating the impact of reflection

Motivation: reflection slows the system down, so verify how much it actually helps before keeping it.

Objective-eval example: a retail-store QA system where an LLM writes a SQL query to answer questions like which product color has the highest total sales. The workflow: a first model writes query v1; a second model reflects on and revises it; the revised query executes against the database; a final answer is produced. Evaluation recipe: build a small ground-truth set (roughly 10-15 questions with known answers, such as how many items sold in May 2025, the most expensive inventory item, the number of styles carried), run the pipeline with and without reflection, and compare percent correct. The cited result: **87% correct without reflection vs 95% with reflection.** With evals like this in place, you can also systematically compare prompt variants (rewriting the generation or reflection prompt, adding an instruction to make the query faster or clearer) and re-measure each time.

Subjective tasks (judging which plot looks better) are the trap. Naive LLM-as-a-judge pairwise comparison works poorly: results are sensitive to wording, rank orderings often do not match human expert judgment, and many models exhibit position bias, favoring whichever option is presented first. The recommended alternative is rubric-based grading: prompt a multimodal model with a single image plus explicit binary criteria (clear title present, axis labels present, appropriate chart type, and so on), score each criterion 0 or 1, and sum. Five binary scores are better calibrated than asking for one 1-5 score. Build roughly 10-15 visualization queries, generate outputs with and without reflection, score each with the rubric, compare, then reuse the eval to tune prompts.

Closing guidance: objective criteria mean code-based evaluation, which is easiest to manage; subjective criteria mean LLM-as-a-judge with careful calibration, meaning a well-designed rubric. Good evals are central to building agentic workflows effectively.

## Lesson 18: Using external feedback

Core idea: self-reflection is a strong baseline, but reflection improves much more when the model can pull additional information from outside the conversation, querying a database or calling a function or tool to check whether its output is actually correct. This is reflection with external feedback.

The worked example extends the retail-store QA system. Without reflection, the model writes one SQL query, executes it, and answers. With external feedback, the agent first tests and validates the query against the real database, spots the error by examining the returned data (for example, the wrong product attribute was queried), revises the query, and produces the corrected answer.

The memorable visual is a return-on-investment curve: performance against time spent prompt-engineering, with three curves, no reflection (lowest plateau), with reflection (higher), and with reflection plus external feedback (highest). All three flatten, meaning prompt tinkering alone hits diminishing returns, while each reflection stage lifts the achievable ceiling. Each milestone is easy to implement yet yields large accuracy gains, so expect to iterate through these stages when building systems. Other feedback-source examples: competitor watching for a monitoring task, web search results for fact-checking an essay, a word-count tool for enforcing length guidelines.

## Lesson 19: Ungraded lab, improving SQL generation with reflection (notebook M2_UGL_2)

A text-to-SQL pipeline over a sales database demonstrating both reflection regimes side by side.

First, generate_sql produces a v1 query computing total sales with a subtle sign error: it returns a negative total because qty_delta is stored negative for sales rows. A text-only refine_sql step (the LLM critiques the SQL and returns feedback plus a revised query) fails to catch the bug. Then refine_sql_external_feedback runs the query, feeds the actual result DataFrame back to the model as external feedback, and the model spots the implausible negative total and fixes the query by wrapping the quantity in ABS(qty_delta). A run_sql_workflow function chains the pipeline: generate, execute, reflect with results, regenerate.

The lesson, mirroring Lesson 18 exactly: introspective reflection misses errors that execution feedback makes obvious. Grounding the critique loop in real tool outputs is what makes reflection reliable. Notebook downloaded locally, referenced by name only.

## Not extracted

- Item 20, Module 2 quiz, and item 21, M2 graded lab: graded, membership-gated.

## How I'd use it

- Reflection is my default second step for any generation task with checkable quality criteria: structured outputs, code, SQL, charts. The pattern is generate, critique against explicit criteria, revise, and cap the rounds.
- I never keep a reflection step on faith. The 87% vs 95% recipe is the template: a small ground-truth set (10-15 cases), run with and without, compare percent correct, and let the delta decide whether the latency is worth paying.
- For subjective quality, I skip pairwise LLM judging entirely. Binary rubric criteria summed into a score is the calibrated option, and position bias is the reason pairwise comparisons mislead.
- Wherever a step's output can be executed or looked up, I ground reflection in that external signal (run the SQL, render the chart, call the tool) rather than letting the model grade its own homework from memory. The negative-total SQL bug is the story I remember: the text-only critic missed it, the executed result made it obvious.
- This module is the theory under my reflective-qa project: a writer, a critic, and one revise round. Its null result (critics fixing some errors while rewording correct answers lost points) is exactly the failure mode this module predicts when reflection is unmeasured and ungrounded.
