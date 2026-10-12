# reflective-qa: worked example for the code-lab skill

> This is the worked example backing the `code-lab` skill's Phase 1–5 for the
> `bhavya94/reflective-qa` repo (the experiment and the package refactor, PRs #19–#23, all
> merged). The skill verifies this against the repo before each session. If the repo moved on,
> recon wins.

# reflective-qa: Hands-On Code Lab

A guided walkthrough for running the code yourself in your IDE (Cursor), setting
breakpoints, and learning how the reflection agent actually works — plus what each
PR's unit tests prove.

**Assumes:** the repo is cloned on your laptop, `uv sync` is done, `data/` is
downloaded (`uv run rqa download`), and `.env` holds your `ANTHROPIC_API_KEY`.
Most of this lab is **free** (no API calls); the few paid steps are marked with
their cost guard. Every command runs through one entry point, `uv run rqa <command>`.

**Debugger basics (Cursor):** click the gutter left of a line number (or F9) to
set a breakpoint, F5 to start debugging, F10 step over, F11 step into, and use
the Debug Console to evaluate expressions like `context.draft` live. To debug a
single test, open the test file and use "Debug Test" above the test function, or
create a `launch.json` with `"module": "pytest"` and `"args": ["tests/test_checks.py"]`.

---

## Part 1 — The map (10 minutes, read-only)

The code is one package per responsibility under `src/reflective_qa/`, and imports only
point down (`tests/test_layers.py` enforces it). In the order things execute:

```
data/download.py       fetch QASPER + the official evaluator, checksum-verified
data/qasper.py         QasperSplit: typed loader, lookup by paper, seeded question sample
retrieval/bm25.py      BM25 over one paper's paragraphs; Retriever keeps one index per paper
agent/writer.py        Writer: answer prompt, revise prompt, JSON reply parsing, fingerprint
agent/checks.py        CodeChecks: free deterministic checks on a draft (bad_citation,
                       yes_no_format, too_long)
agent/critic.py        Critic: fixed checklist, schema-bound verdict
agent/reflection.py    ReflectionAgent: one setup's critic and revise requests, fingerprint
runs/                  RunStore (files named by fingerprint), BatchRunner (Batch API,
                       never pay twice, budget guard), Costs and CostEstimator
eval/metrics.py        answer-F1 (official) + paragraph-ID evidence-F1, pure functions
eval/analysis.py       Revision and RevisionAnalysis: paired-bootstrap CI, change by kind
experiments/           BaselineExperiment, ReflectionExperiment: wire it all together
site/                  the public results page
cli.py                 the `rqa` command, the only module that parses arguments or prints
```

The one sentence to carry: **the baselines write first answers, the reflection agent
reviews and revises them once, and the experiment measures whether that was worth it.**
(Answer: mostly no — the README's results table is the punchline. Understanding *why* is
the real lesson.)

**PR → code → tests map** (all PRs merged on main). The refactor (#19–#23) moved the code
into packages; the tests below still prove what each original PR built.

| PR | What | Tests that prove it |
|----|------|---------------------|
| #2–4 (setup) | download, typed loader, evaluator parity | test_download, test_data, test_evaluator_parity |
| #6 (baselines) | BM25 retrieval + recall@k | test_retrieval |
| #7 (baselines) | answer-F1 + evidence-F1 | test_scoring |
| #8 (baselines) | answer prompt + parsing | test_writer |
| #9 (baselines) | batch runner, cache, budget guard | test_baselines |
| #10 (baselines) | citation IDs without brackets | test_writer |
| #12 (agent) | code checks | test_checks |
| #13 (agent) | critic | test_critic |
| #14 (agent) | setups, contexts, requests | test_reflection |
| #15 (agent) | run stages, budget guards, report | test_reflection_run |
| #16 (experiment) | bootstrap CI, change-by-kind analysis | test_analysis |
| #17–18 (results page) | page data and the page | test_site_collector, test_site_page |
| #19–23 (refactor) | packages, `rqa`, fingerprint pins, layers | test_fingerprints, test_layers, test_cli |

---

## Part 2 — The free tour (no API key, ~45 minutes)

### Exercise 1: checks — the cheapest feedback in the system

1. Open `src/reflective_qa/agent/checks.py`, method `CodeChecks.run`.
2. Set a breakpoint on the `findings = []` line.
3. Debug the test: `tests/test_checks.py::test_citing_a_paragraph_that_was_not_given_is_flagged_once_per_id`.
4. In the Debug Console, evaluate `cited`, `passage_ids`, and `unknown` as you step.

**What to notice:** findings use names from the critic's checklist
(`bad_citation`, `yes_no_format`, `too_long`) — the same vocabulary the LLM
critic speaks, so the critic can confirm or reject each one. That's the design
move: deterministic checks and the LLM critic share one language.

**Break-it exercise:** in the yes/no regex `_YES_NO_QUESTION`, add `what` to the
alternation. Run `uv run pytest tests/test_checks.py` — which tests fail, and
why is flagging "what" questions wrong? (Hint: the comment above the regex cites
train-split measurements.) Revert after.

### Exercise 2: scoring — how a "0.512" is actually computed

1. Open `src/reflective_qa/eval/metrics.py`, breakpoint in `token_f1`.
2. Debug `tests/test_scoring.py::test_best_reference_wins_and_its_type_is_reported`.
3. Watch `normalize()` strip case, punctuation, and articles, then the
Counter-overlap math.

**What to notice:** `answer_f1` takes the *best* reference and reports its
*type* — that's how the README breaks F1 down by answer type. And
`evidence_f1` is deliberately *not* the official QASPER metric (paragraph IDs,
not evidence strings) — the README says so explicitly. Knowing which numbers
are comparable to published work and which aren't is part of reading this repo.

### Exercise 3: the critic's contract

1. Open `src/reflective_qa/agent/critic.py`. Read `CHECKLIST`, then `SYSTEM` and `SCHEMA`.
2. Debug `tests/test_critic.py::test_revise_without_problems_counts_as_pass_and_pass_drops_stray_problems`.

**What to notice:** this test encodes the key design decision — a "revise"
verdict with no actionable problems is *useless* to the writer, so the parser
downgrades it to "pass". Both the prompt (`SYSTEM`) and the schema (its enum is
`list(CHECKLIST)`) are *built from* `CHECKLIST`, so the human-readable checklist and the
machine-enforced schema can't drift apart. `test_the_checklist_is_both_explained_and_enforced_by_the_schema`
guards that.

**Break-it exercise:** add an item to `CHECKLIST` and run the critic tests: they pass,
because the prompt and the schema both pick it up. Now replace `list(CHECKLIST)` in
`SCHEMA` with a hand-written list of the old names, and run again — the drift test fails.
That's why the code derives both from one dict. Revert.

### Exercise 4: the fingerprint — cache invalidation made explicit

1. Open `src/reflective_qa/agent/reflection.py`, `ReflectionAgent.fingerprint` and `_probe`.
2. Debug `tests/test_reflection.py::test_fingerprint_changes_with_the_writer_the_critic_and_any_prompt`.

**What to notice:** `_probe()` builds a *fixed fake question* whose draft trips
several checks, then `fingerprint` hashes the *actual requests* that setup
would send for it. Change any prompt, schema, model setting, or check behavior
→ new hash → new files, never mixed results. And the subtle bit the test name
tells you: `max_words` only enters the hash where findings are actually shown —
a critic that never sees findings keeps its paid reviews when the word limit
changes. That's money-aware engineering.

**Break-it exercise:** change one word in `REVISE_INSTRUCTION` (in `agent/writer.py`).
Run `uv run pytest tests/test_reflection.py tests/test_fingerprints.py`. The reflection
test still passes: it compares two hashes computed in the same run. The pin in
`test_fingerprints.py` fails, because the hash no longer matches the files your paid runs
are stored under. This is the test *working as designed*: it noticed your prompt edit.
Revert.

---

## Part 3 — The reflection loop, breakpoint by breakpoint (~60 minutes)

This is the core session. You have two ways to run it; do the free one first.

### 3a. Free: walk the loop with the built-in lab rat (no API calls)

`_probe()` on `ReflectionAgent` exists for exactly this — a fixed Context you can
drive through the whole loop without spending a cent. In your Debug Console
(or a scratch script under `/tmp`, never committed):

```python
from reflective_qa.agent.checks import CodeChecks
from reflective_qa.agent.critic import CriticConfig
from reflective_qa.agent.reflection import ReflectionAgent, Setup
from reflective_qa.agent.writer import Writer

setup = Setup("lab", "sonnet-k20", CriticConfig("claude-sonnet-5-5", "medium", 4000, True))
agent = ReflectionAgent(setup, Writer.load_all()["sonnet-k20"], CodeChecks.from_config())
probe = agent._probe()                   # fixed Context; draft trips several checks
probe.findings                           # read these first: what did the checks flag?
agent.critic_requests({"probe": probe})  # inspect the exact prompt the critic would get
```

`ReflectionAgent.load_all()` gives you the six configured setups instead.

Set breakpoints and step through, in execution order:

1. **`ReflectionExperiment.contexts`** (experiments/reflection.py) — the assembly line.
   For each sampled question it pulls the first answer, re-runs BM25 (`writer.k`
   paragraphs), and calls `ReflectionAgent.context`, which runs the checks. Inspect:
   `drafts[q.id]["predicted_answer"]`, the retrieved passages (do the top-k look
   relevant?), the findings. *This is where you'd spot a retrieval problem vs. a writing
   problem.*
2. **`CodeChecks.run`** (agent/checks.py) — you already know this from Exercise 1.
3. **`Critic.request`** (agent/critic.py) — read the full prompt text in the
   debugger. Notice the critic sees *everything the writer saw* ("They are
   everything the writer saw") plus the draft plus, optionally, the check
   findings — and is told the automatic checks "can be wrong."
4. **`Critic.parse`** — verdict → problems. Feed it a fake "revise with no
   problems" reply and watch it become "pass" (you saw the test).
5. **`ReflectionAgent.problems`** — the routing decision: critic's problems, or the raw
   check findings when there's no critic (`sonnet-code-feedback` setup), or `[]`
   when the critic passed. **Only drafts with a non-empty list get revised.**
6. **`Writer.revise_request`** (agent/writer.py) — the money shot. Read the assembled
   prompt: original request + draft + `REVISE_INSTRUCTION` + findings. Notice the comment
   above `REVISE_INSTRUCTION`: the instruction is repeated because the 20-question pilot
   showed revisions drifting long and hedged. *Prompt engineering driven by observed
   failure, not vibes.*
7. **`ReflectionExperiment.final_answers`** — revision wins if it succeeded, else the
   draft stands. Cost counted is *reflection only*, not the draft.
8. **`ReflectionExperiment.report`** + **`analyze`** — per-question F1 deltas,
   better/worse counts, and the paired-bootstrap 95% CI (`RevisionAnalysis` in
   eval/analysis.py). This is where the experiment's conclusion comes from.

### 3b. Paid: three real questions, pocket money

Once the free walk makes sense, run the real thing small. This needs the first-answer
files on disk (under `data/runs/`, gitignored — from your earlier paid runs) and `.env`
with the key:

```bash
uv run --env-file .env rqa reflect estimate sonnet-code-feedback --questions 3
uv run --env-file .env rqa reflect run sonnet-code-feedback --questions 3 --max-dollars 0.50
uv run rqa reflect report sonnet-code-feedback --questions 3
```

**Why this is safe:** `estimate` prints the cost before anything is spent (it counts
tokens with the free `count_tokens` endpoint); `run` *refuses* if the estimate exceeds
`--max-dollars`; samples are prefixes, so these 3 questions are the first 3 of your
200-question sample. If your 200-question runs are on disk, `estimate` shows $0.00 and
`run` submits nothing — the fingerprint cache at work. Then open
`data/runs/reflect-sonnet-code-feedback-*.jsonl` and read the actual revisions. There's no
substitute for reading three real trajectories.

**Breakpoints for the paid run:** `BatchRunner.run` in runs/batch.py — the budget guard,
which refuses before anything is submitted — then `_submit_and_collect`, the Batch API
submit → poll → collect cycle and the "never pay twice" resume logic (answered questions
are skipped; a submitted batch ID is saved before waiting).

---

## Part 4 — Understand the experiment's result yourself (the payoff)

The README's results table says reflection didn't move answer-F1. Don't take it on
faith — reproduce the reasoning:

1. Run `uv run rqa reflect report` (free — reads your existing run files).
2. Look at the `better / worse` counts and the change-by-kind split
   (`abstain to answer`, `answer to abstain`, `reworded`) on each setup's last line.
3. The story the numbers tell: critics *do* catch wrong "Unanswerable" answers
   (those revisions gain +0.07 to +0.18), but rewording already-given answers
   usually scores lower (−0.07 to −0.14). The two effects cancel.
4. Open `RevisionAnalysis.analyze` in eval/analysis.py and trace how the bootstrap CI is
   built — 5000 resamples of the per-question deltas, and `Revision.kind` for the split.
   Every CI including zero is why the README says "no setup changed answer-F1 measurably."

**The deep lesson:** this is what a *negative result done right* looks like —
same questions, same drafts, paired comparison, quantified uncertainty, and a
mechanistic explanation (not just "it didn't work" but *which* revisions help
and which hurt). That's the standard your replay's Phase A judge work should
be held to.

---

## Part 5 — Make it yours (pick any)

1. **Write a new code check.** E.g., flag answers that copy the question back
   (`echo_check`). Add it to `CodeChecks.run`, add a test in test_checks.py, and run
   `uv run rqa checks` to see how often it fires on the first answers.
2. **Tune `max_answer_words`.** It's 35, set on the train split (see the comment
   in reflection.toml). Try 25 and 50 in a scratch config — which drafts newly
   get flagged? What does the fingerprint do to your cached files?
3. **Read three full trajectories** from the JSONL files and write down, in
   your own words, one case where the critic was right and one where it
   hurt. That's your error-analysis muscle for Phase A.
4. **Swap the critic.** The `haiku-sonnet-critic` setup uses a stronger critic
   than writer — the config makes this a one-line change. The README shows it
   still didn't move F1. Ask yourself why before reading the analysis.

---

## Quick reference

| Command | Cost | What it teaches |
|---|---|---|
| `uv run pytest` | free | the whole contract, per PR |
| `uv run rqa download` | free | data provenance |
| `uv run rqa recall` | free | BM25 recall@k |
| `uv run rqa score <predictions.jsonl>` | free | the metrics |
| `uv run --env-file .env rqa reflect estimate <setup>` | free (token counts) | what a run *would* cost |
| `uv run --env-file .env rqa reflect run <setup> --max-dollars X` | paid, capped | the real loop |
| `uv run rqa reflect report` | free | scoring the runs |

Total suggested time: ~2.5 hours across Parts 2–4. Do it in one sitting if you
can — the loop only clicks when the whole thing is in your head at once.
