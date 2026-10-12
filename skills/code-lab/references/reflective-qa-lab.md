# reflective-qa: worked example for the code-lab skill

> This is the worked example backing the `code-lab` skill's Phase 1–5 for the
> `bhavya94/reflective-qa` repo (M0–M3, all merged). The skill verifies this
> against the repo before each session — if the repo moved on, recon wins.

# reflective-qa: Hands-On Code Lab

A guided walkthrough for running the code yourself in your IDE (Cursor), setting
breakpoints, and learning how the reflection agent actually works — plus what each
PR's unit tests prove.

**Assumes:** the repo is cloned on your laptop, `uv sync` is done, `data/` is
downloaded (`uv run python -m reflective_qa.download`), and `.env` holds your
`ANTHROPIC_API_KEY`. Most of this lab is **free** (no API calls); the few paid
steps are marked with their cost guard.

**Debugger basics (Cursor):** click the gutter left of a line number (or F9) to
set a breakpoint, F5 to start debugging, F10 step over, F11 step into, and use
the Debug Console to evaluate expressions like `context.draft` live. To debug a
single test, open the test file and use "Debug Test" above the test function, or
create a `launch.json` with `"module": "pytest"` and `"args": ["tests/test_checks.py"]`.

---

## Part 1 — The map (10 minutes, read-only)

The data flow, in the order things execute. Each module is one PR-sized idea:

```
download.py      fetch QASPER + official evaluator, checksum-verified        (M0)
data.py          typed loader: Paper / Paragraph / Question dataclasses      (M0)
retrieval.py     BM25 over one paper's paragraphs                            (M1)
answering.py     writer prompt + JSON-schema reply parsing                   (M1)
baselines.py     Batch API runner: fingerprint cache, budget guard, report   (M1)
scoring.py       answer-F1 (official) + paragraph-ID evidence-F1             (M1)
checks.py        free deterministic checks on a draft (bad_citation,         (M2)
                 yes_no_format, too_long)
critic.py        LLM critic: fixed checklist, schema-bound verdict            (M2)
reflection.py    the loop: contexts -> critic -> revise -> report            (M2/M3)
```

The one sentence to carry: **M1 writes drafts, M2 reflects on them once, M3
measures whether reflection was worth it.** (Answer: mostly no — the README's
M3 table is the punchline. Understanding *why* is the real lesson.)

**PR → code → tests map** (all PRs merged on main):

| PR | What | Tests that prove it |
|----|------|---------------------|
| #2–4 (M0) | download, typed loader, evaluator parity | test_download, test_data, test_evaluator_parity |
| #6 (M1) | BM25 retrieval + recall@k | test_retrieval |
| #7 (M1) | answer-F1 + evidence-F1 | test_scoring |
| #8 (M1) | answer prompt + parsing | test_answering |
| #9 (M1) | batch runner, cache, budget guard | test_baselines |
| #10 (M1) | citation IDs without brackets | test_answering |
| #12 (M2) | code checks | test_checks |
| #13 (M2) | critic | test_critic |
| #14 (M2) | setups, contexts, requests | test_reflection |
| #15 (M2) | run stages, budget guards, report | test_reflection_run |
| #16 (M3) | bootstrap CI, change-by-kind analysis | test_reflection_run |

---

## Part 2 — The free tour (no API key, ~45 minutes)

### Exercise 1: checks — the cheapest feedback in the system

1. Open `src/reflective_qa/checks.py`, function `run_checks`.
2. Set a breakpoint on the `findings = []` line.
3. Debug the test: `tests/test_checks.py::test_citing_a_paragraph_that_was_not_given_is_flagged_once_per_id`.
4. In the Debug Console, evaluate `cited`, `passage_ids`, and `unknown` as you step.

**What to notice:** findings use names from the critic's checklist
(`bad_citation`, `yes_no_format`, `too_long`) — the same vocabulary the LLM
critic speaks, so the critic can confirm or reject each one. That's the design
move: deterministic checks and the LLM critic share one language.

**Break-it exercise:** in the yes/no regex `_YES_NO_QUESTION`, add `what` to the
alternation. Run `uv run pytest tests/test_checks.py` — which test fails, and
why is flagging "what" questions wrong? (Hint: the comment above the regex cites
train-split measurements.) Revert after.

### Exercise 2: scoring — how a "0.512" is actually computed

1. Open `src/reflective_qa/scoring.py`, breakpoint in `token_f1`.
2. Debug `tests/test_scoring.py::test_best_reference_wins_and_its_type_is_reported`.
3. Watch `normalize()` strip case, punctuation, and articles, then the
Counter-overlap math.

**What to notice:** `answer_f1` takes the *best* reference and reports its
*type* — that's how the README breaks F1 down by answer type. And
`evidence_f1` is deliberately *not* the official QASPER metric (paragraph IDs,
not evidence strings) — the README says so explicitly. Knowing which numbers
are comparable to published work and which aren't is part of reading this repo.

### Exercise 3: the critic's contract

1. Open `src/reflective_qa/critic.py`. Read `CHECKLIST`, then `SCHEMA`.
2. Debug `tests/test_critic.py::test_revise_without_problems_counts_as_pass_and_pass_drops_stray_problems`.

**What to notice:** this test encodes the key design decision — a "revise"
verdict with no actionable problems is *useless* to the writer, so the parser
downgrades it to "pass". The schema *enforces* the checklist (the enum is
`list(CHECKLIST)`), and `test_the_checklist_is_both_explained_and_enforced_by_the_schema`
proves the human-readable checklist and the machine-enforced schema can't drift
apart. If you add a checklist item later, that test forces you to keep them in sync.

**Break-it exercise:** add `"hallucinated_number": "..."` to CHECKLIST but not
to SCHEMA. Run the critic tests — see which one catches the drift. Revert.

### Exercise 4: the fingerprint — cache invalidation made explicit

1. Open `src/reflective_qa/reflection.py`, functions `fingerprint` and `_probe`.
2. Debug `tests/test_reflection.py::test_fingerprint_changes_with_the_writer_the_critic_and_any_prompt`.

**What to notice:** `_probe()` builds a *fixed fake question* whose draft trips
several checks, then `fingerprint()` hashes the *actual requests* that setup
would send for it. Change any prompt, schema, model setting, or check behavior
→ new hash → new files, never mixed results. And the subtle bit the test name
tells you: `max_words` only enters the hash where findings are actually shown —
a critic that never sees findings keeps its paid reviews when the word limit
changes. That's money-aware engineering.

**Break-it exercise:** change one word in `REVISE_INSTRUCTION`. Run the
reflection tests — the fingerprint test fails because the hash changed. This is
the test *working as designed*: it noticed your prompt edit. Revert.

---

## Part 3 — The reflection loop, breakpoint by breakpoint (~60 minutes)

This is the core session. You have two ways to run it; do the free one first.

### 3a. Free: walk the loop with the built-in lab rat (no API calls)

`_probe()` in reflection.py exists for exactly this — a fixed Context you can
drive through the whole loop without spending a cent. In your Debug Console
(or a scratch script under `/tmp`, never committed):

```python
from reflective_qa.reflection import _probe, critic_requests, problems, revise_request
from reflective_qa.reflection import Setup
from reflective_qa.critic import CriticConfig
from reflective_qa.answering import load_runs

probe = _probe(35)                      # fixed Context; draft trips several checks
probe.findings                           # read these first: what did the checks flag?
setup = Setup("lab", "sonnet-k20", CriticConfig("claude-sonnet-5-5", "medium", 4000, True))
critic_requests(setup, {"probe": probe}) # inspect the exact prompt the critic would get
```

Set breakpoints and step through, in execution order:

1. **`build_contexts`** — the assembly line. For each sampled question it pulls
   the M1 draft, re-runs BM25 (`writer.k` paragraphs), and runs the checks.
   Inspect: `draft["predicted_answer"]`, `passages` (do the top-k look relevant?),
   `findings`. *This is where you'd spot a retrieval problem vs. a writing problem.*
2. **`run_checks`** (checks.py) — you already know this from Exercise 1.
3. **`build_critic_request`** (critic.py) — read the full prompt text in the
   debugger. Notice the critic sees *everything the writer saw* ("They are
   everything the writer saw") plus the draft plus, optionally, the check
   findings — and is told the automatic checks "can be wrong."
4. **`parse_critique`** — verdict → problems. Feed it a fake "revise with no
   problems" reply and watch it become "pass" (you saw the test).
5. **`problems()`** — the routing decision: critic's problems, or the raw check
   findings when there's no critic (`sonnet-code-feedback` setup), or `[]`
   when the critic passed. **Only drafts with a non-empty list get revised.**
6. **`revise_request`** — the money shot. Read the assembled prompt: original
   request + draft + REVISE_INSTRUCTION + findings. Notice the comment at the
   top of the file: the instruction is repeated because the 20-question pilot
   showed revisions drifting long and hedged. *Prompt engineering driven by
   observed failure, not vibes.*
7. **`final_answers`** — revision wins if it succeeded, else the draft stands.
   Cost counted is *reflection only*, not the draft.
8. **`report`** + **`analyze`** — per-question F1 deltas, better/worse counts,
   and the paired-bootstrap 95% CI. This is where the M3 conclusion comes from.

### 3b. Paid: three real questions, pocket money

Once the free walk makes sense, run the real thing small. This needs your M1
draft files on disk (they're under `data/runs/`, gitignored — from your earlier
paid runs) and `.env` with the key:

```bash
uv run python -m reflective_qa.reflection estimate sonnet-code-feedback --questions 3
uv run --env-file .env python -m reflective_qa.reflection run sonnet-code-feedback --questions 3 --max-dollars 0.50
uv run python -m reflective_qa.reflection report sonnet-code-feedback --questions 3
```

**Why this is safe:** `estimate` prints the cost before anything is spent;
`run` *refuses* if the estimate exceeds `--max-dollars`; samples are prefixes,
so these 3 questions are the first 3 of your 200-question sample — nothing is
wasted. Then open `data/runs/reflect-sonnet-code-feedback-*.jsonl` and read the
actual critic/revise request/response pairs. There's no substitute for reading
three real trajectories.

**Breakpoint for the paid run:** `submit_and_collect` in baselines.py — watch
the Batch API submit → poll → collect cycle, and the "never pay twice" resume
logic (answered questions are skipped; a submitted batch ID is saved before
waiting).

---

## Part 4 — Understand the M3 result yourself (the payoff)

The README's M3 table says reflection didn't move answer-F1. Don't take it on
faith — reproduce the reasoning:

1. Run `uv run python -m reflective_qa.reflection report` (free — reads your
   existing run files).
2. Look at the `better / worse` columns and the `revision_kind` split
   (`abstain_to_answer` vs `reworded`) in the analysis output.
3. The story the numbers tell: critics *do* catch wrong "Unanswerable" answers
   (those revisions gain +0.07 to +0.18), but rewording already-given answers
   usually scores lower (−0.07 to −0.14). The two effects cancel.
4. Open `analyze()` in reflection.py and trace how the bootstrap CI is built —
   5000 resamples of the per-question deltas. Every CI including zero is why
   the README says "no setup changed answer-F1 measurably."

**The deep lesson:** this is what a *negative result done right* looks like —
same questions, same drafts, paired comparison, quantified uncertainty, and a
mechanistic explanation (not just "it didn't work" but *which* revisions help
and which hurt). That's the standard your replay's Phase A judge work should
be held to.

---

## Part 5 — Make it yours (pick any)

1. **Write a new code check.** E.g., flag answers that copy the question back
   (`echo_check`). Add it to `run_checks`, add a test in test_checks.py, run
   the checks `__main__` analysis to see how often it fires on M1 drafts.
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
| `uv run python -m reflective_qa.download` | free | data provenance |
| `uv run python -m reflective_qa.retrieval_eval …` | free | BM25 recall@k |
| `uv run python -m reflective_qa.scoring … …` | free | the metrics |
| `… reflection estimate <setup>` | free | what a run *would* cost |
| `… reflection run <setup> --max-dollars X` | paid, capped | the real loop |
| `… reflection report` | free | scoring the runs |

Total suggested time: ~2.5 hours across Parts 2–4. Do it in one sitting if you
can — the loop only clicks when the whole thing is in your head at once.
