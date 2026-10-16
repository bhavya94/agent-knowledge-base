# Module 4: Practical Tips for Building Agentic AI

**Course:** Agentic AI (DeepLearning.AI, Andrew Ng) **Date:** 2026-10-16 **Verdict:** the module the whole course exists for. Evals, error analysis, component-level evals, and the fix repertoire, with real percentages throughout. If I re-read one module before building an agent system, it is this one.

## Lesson 31: Evaluations (evals)

Core argument: you cannot predict in advance where an agentic workflow will fail, so build a quick-and-dirty prototype first, eyeball a small batch of outputs (10-20 examples), note failure modes in a document or spreadsheet, and only then invest in systematic evaluation. Do not theorize for weeks. Keep early prototypes safe (no data leaks).

Three worked examples:

1. **Invoice processing (extract the due date).** The prototype confused the issue date with the due date. The fix loop: hand-annotate due dates on 10-20 invoices in standard Y-M-D format, prompt the model to always emit that format, extract with regex, and track percent-correct while iterating.
2. **Marketing caption assistant (10-word limit).** Outputs ran long (17, 14, 11 words). No per-example ground truth is needed because the target is uniform; measure word counts in plain Python.
3. **Research agent omitting key points** (a black-hole article missing a breakthrough; a fruit-harvesting-robotics piece missing a leading company). Many valid phrasings exist, so regex cannot judge. Define 3-5 gold-standard discussion points per prompt; an LLM-as-judge returns a JSON score (0-5) with an explanation of which points were covered.

The taxonomy is a 2x2 grid with two axes: how you judge (code-based objective checks vs LLM-as-judge subjective checks) and ground truth (each example has its own vs one global target). The four quadrants map to the examples: code plus per-example ground truth (invoice dates), code plus uniform target (caption length), LLM judge plus per-example annotations (gold talking points), LLM judge plus shared rubric (grading generated charts on criteria like clear axis labels).

Practical tips: keep early evals quick and dirty, because teams paralyze themselves imagining multi-week eval projects; iterate on the eval itself as the workflow evolves; blend human eyeballing with metric-based evals and gradually shift trust toward metrics; when the system visibly improves but the score does not move, the eval set is stale and needs enlarging or redesign; compare against an expert human on failing cases to aim effort.

## Lesson 32: Error analysis and prioritizing next steps

Classical error analysis applied to agents: look at outputs, categorize errors, quantify frequency per category, prioritize the biggest, and brainstorm fixes targeted at categories rather than random fixes.

Invoice example (18 invoices): wrong due date 12 (67%), missing due date 4 (22%), wrong biller address 3 (17%). Percentages exceed 100% because one invoice can carry multiple errors. Priority: the 67% due-date bucket. Category-specific fixes: tweak the system prompt, or buy thinking time by having the model first list every date on the invoice, then decide which is the due date (a cheap chain-of-thought step to test).

Research agent over 7 long articles (fewer examples suffice when outputs are multi-page): excessive length and verbosity 5 of 7 (71%), missing important content 4 of 7 (57%), then hallucination, missed latest updates, formatting, irrelevant content, bad citations, biased perspectives. Fixes per category: "keep it concise" in the system prompt for verbosity; plan 5-6 key points before writing to fight missing content; a verification and search cross-check step for hallucinations (expensive but effective).

The trace-level version of the same discipline: collect intermediate outputs (traces; each single step's output is a span, borrowing observability terminology) on poorly handled cases, and judge each step against what a human expert would have produced given the same input. A step counts as an error source only if it did substantially worse than the expert. Research-agent walkthrough: for a black-hole-science essay, the search terms look reasonable to an expert, but the search results are full of low-rigor pop-science blogs rather than scientific papers, so the "pick the five best sources" step cannot be blamed for choosing poorly from a bad pool. Tabulate across many failing cases in a spreadsheet (rows are prompts, columns are components, count how often each component was the weak link): search-term quality disappoints roughly 5% of the time, search-result quality roughly 45%. Fix search first, after sanity-checking that the terms really are fine.

Prioritization weighs two factors: how often a component fails, and whether you have ideas to improve it efficiently. A badly failing component with no plausible fix ranks below a moderately failing one with a clear remedy. Even rough counts in 5-10 minutes focus effort on the largest error buckets; that is the most efficient way to choose next steps.

## Lesson 33: More error analysis examples

The next discipline: attribute an error category to the responsible component before fixing anything.

Invoice case: due-date errors could come from PDF-to-text garbling or from the LM pulling the wrong date. Counting 10-100 failures in a spreadsheet showed LM extraction responsible for far more, so tuning PDF-to-text (potentially weeks or months of work) would have been wasted.

Customer-email workflow (read email, query order DB, draft reply for human review): failures split three ways: bad SQL query (wrong table), corrupted data in the DB, or a wrong drafted email despite correct info. Tabulating bad outputs showed SQL-query writing dominant at roughly 75%, email drafting secondary at roughly 30%. Priority is improving query writing first, then the email prompt.

Two closing points: category percentages need not sum to 100%, because a single failure can involve multiple components; and once error analysis picks the component, the natural next step is a component-level eval for it (next lesson).

## Lesson 34: Component-level evaluations

End-to-end evals are the gold standard but expensive and noisy: changing one component forces a full rerun, and randomness elsewhere can mask small genuine improvements. The remedy is an eval scoped to the component being worked on.

Running example: the research agent's web-search step. An expert lists gold-standard reference sources for a handful of queries; code measures overlap between the search outputs and the gold set with standard IR metrics like F1. That gives a tight loop for testing hyperparameters (search provider, number of results, date ranges), then you confirm with an end-to-end eval before declaring victory.

Benefits: clearer signal on specific errors, no noise from the rest of the pipeline, and different team members can each own a component with its own metric and move faster in parallel. Rule of thumb: once error analysis flags a component, consider a component-wise eval to go faster.

## Lesson 35: Ungraded lab, adding a component-level eval to the research workflow (notebook M4_UGL_1)

The Lesson 34 idea as code, applied to the tool-using research agent (three-step workflow: search the web, reflect, publish an HTML report). The eval compares URLs returned by the agent's search tool (Tavily) against a predefined list of preferred trustworthy domains (arxiv.org, nature.com, nasa.gov) on the topic "recent developments in black hole science".

It is an objective, per-example ground-truth check: a single function parses the Tavily output, identifies URLs on preferred domains, computes the preferred-to-total ratio, and returns a PASS/FAIL flag plus a Markdown summary that can be embedded in reports. Notebook sections: introduction, lab overview, building the eval as a reusable function, a "try it yourself" section with adjustable topic and ratio parameters, takeaways. It uses AISuite for tool-calling and reminds the model of the current date for recency-sensitive queries.

The emphasized takeaway: component-level evals give a tight, cheap feedback loop for improving one step without rerunning the whole agent. Notebook downloaded locally, referenced by name only.

## Lesson 36: How to address problems you identify

The fix repertoire, once evals and error analysis point at a problem, split by component type.

**Non-LLM components** (web search, RAG retrieval, code execution, trained models like speech recognition or people detection): tune hyperparameters (number of search results, date ranges, RAG similarity thresholds and chunk sizes, detection thresholds trading false positives against false negatives) or swap the component entirely (a different RAG or search provider).

**LM-based components**, as a ladder, cheapest first:

1. Make prompts more explicit.
2. Add few-shot examples.
3. Try a different model. AISuite makes swapping easy; evals decide the winner.
4. Decompose a complex step into smaller steps, such as generation plus reflection.
5. Fine-tune only as a last resort: complex and expensive in developer time, worth it mainly near 90-95% on a mature application that needs the final points.

Demo: a PII-redaction task contrasting models. The smaller model (Llama 3.1 8B) returns extra unrequested lists, misses a name, and leaves part of an address unredacted; a more capable model redacts everything correctly. Larger frontier models follow instructions better, which is why model swaps sit high on the ladder.

Closing advice on building model intuition: regularly try new model releases (closed and open-weight), keep a personal eval set to calibrate models across task types, and read other practitioners' prompts (published examples, colleagues at frontier labs, respected open-source projects).

## Lesson 37: Latency, cost optimization

Sequencing advice first: get output quality right, optimize cost and latency later; quality is usually the hardest part. Anecdote: a team whose workflow attracted so many users that cost became a problem, "a good problem to have." Cost comes last (not ignored); latency matters somewhat more but still less than quality.

When ready, benchmark each step. The research-agent timing breakdown on the slide (search-term generation 7s, web search 5s, then 3s, 11s, and the final essay step 18s) reveals where speedups are possible. Levers: parallelism (parallel web fetches), smaller or less intelligent models for slow LM steps, faster LM providers on specialized hardware.

Cost gets the same per-step treatment. Providers charge per token (LM steps) and per call (APIs); compute each step's average cost. The slide shows LM steps at hundredths of a cent versus web-search API calls at roughly 1.6 cents each. Measurement also tells you which components are immaterial and not worth optimizing. Measure first, then optimize.

## Lesson 38: Development process summary

Ng closes Module 4 by describing disciplined agentic-AI development as two alternating activities: building (writing code to improve the system) and analysis (deciding where to focus build effort next). The process is a loop, not a line: build, examine traces, run evals, do error analysis, make a targeted component improvement, and back around. The analysis half often does not feel like progress but is equally important.

Staged progression: start with a quick, even rough, end-to-end implementation so you can examine final outputs and read execution traces (that alone often gives a gut sense of which components deserve tuning). As the system matures, add evals over a small dataset (on the order of 10-20 examples) for end-to-end metrics, then graduate to disciplined error analysis (counting how often each component produces subpar outputs), and finally component-level evals that make component improvement efficient. Each round of analysis sharpens where the next round of building goes.

Warning: less experienced teams over-invest in building and under-invest in analysis (error analysis, eval construction), exactly backwards, since analysis is what focuses build effort. On tooling: plenty of products exist for trace monitoring, runtime logging, and cost computation, and they work well, but agentic workflows are highly custom, so he usually ends up building custom evals fitted to his specific application and observed failure modes. Encouraging close: implementing even a fraction of this discipline puts you ahead of most practitioners.

## Not extracted

- Item 39, Module 4 quiz: graded, membership-gated.

## How I'd use it

- This module is the operating loop for my agent eval harness project: prototype, trace, end-to-end eval on 10-20 examples, error analysis with counted buckets, component-level eval for the flagged step, fix from the ladder, re-measure end to end. The harness exists to make each of those steps cheap.
- Error analysis is a spreadsheet habit, not a vibe: rows are failing cases, columns are components, and a component only gets blamed when it did substantially worse than an expert would have with the same input. The 5% vs 45% search-terms-vs-results split is the example I keep in mind; without the count, I would have "fixed" the wrong step.
- The 2x2 eval grid is my first design decision for any new eval: code or judge, per-example ground truth or one global target. Uniform targets (word counts, schema validity) never get an LLM judge; open-ended quality never gets a regex.
- The fix ladder keeps me honest about sequencing: explicit prompts, few-shot, model swap, decompose, and fine-tuning only near 90-95% on something mature. Most agent problems I have seen are prompt or decomposition problems wearing a fine-tuning costume.
- Latency and cost are per-step measurements, not system-level guesses. I profile the steps (the 18s essay step, the 1.6-cent search call), optimize the outliers with parallelism or a smaller model, and leave the immaterial steps alone.
- For red-teaming work, this module's discipline cuts both ways: the same trace and error-analysis machinery that finds quality failures is how I would categorize and prioritize adversarial failures, by counted bucket rather than by scariest anecdote.
