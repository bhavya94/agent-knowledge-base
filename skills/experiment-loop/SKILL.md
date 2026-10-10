---
name: experiment-loop
description: Run an autonomous keep-or-discard experiment loop against one fixed metric — judge or prompt optimization, training and hyperparameter sweeps, performance tuning. Use when the user gives a metric to improve and a budget, or asks to "run experiments overnight".
---

# Experiment Loop

Pattern from Karpathy's [autoresearch](https://github.com/karpathy/autoresearch/blob/master/program.md):
the agent changes one surface, runs a fixed-budget experiment, and keeps the change only if the metric improves.

## Setup — agree on these with the user before the loop starts
1. **Metric** — one number and its direction, e.g. judge–human agreement (κ, higher is better) or
   validation loss (lower is better). The evaluation harness that computes it is read-only: never edit
   the harness, its data, or its seeds.
2. **Editable surface** — the one file or config the agent may change, e.g. `judge_prompt.md` or
   `train.py`. Everything else is read-only. No new dependencies.
3. **Per-run budget** — a fixed wall-clock or token budget, so runs are comparable. A run that takes more
   than 2× the budget is killed and logged as a crash.
4. **Total budget and stop condition** — maximum runs, hours, or dollars, and an early stop after N runs in
   a row without improvement. Write these down before starting.
5. **Branch** — work on `exp/<YYYY-MM-DD>-<tag>`, never on `main`.
6. **Baseline** — the first run uses the unchanged code. Record it.

## Loop
1. Change the editable surface with one idea. Commit.
2. Run the experiment and send all output to a log file, not into context. Read only the metric lines.
3. Append a row to `results.tsv` (tab-separated, not committed):
   `commit  metric  cost  status  description`, where status is `keep`, `discard`, or `crash`.
4. If the metric improved, keep the commit. If it is equal or worse, `git reset` to the last kept commit.
5. On a crash, fix trivial errors (a typo, a missing import) and rerun. Otherwise log `crash` and move on.
6. Repeat until the stop condition. Don't pause to ask whether to continue.

## Keep rule
Weigh the gain against the complexity it adds. A tiny gain that adds hacky code: discard. The same metric
with less code: keep.

## Guard against overfitting
Optimize on a dev split. Report the final result on a held-out split that the loop never saw — select on
held-out agreement, not on the optimization set (`learning/roadmap.md`).

## Report
Hand back `results.tsv`, the best commit, baseline vs. best on held-out data, total cost, and the three
changes that mattered most. Run the explainer skill if the winning change is non-trivial.
