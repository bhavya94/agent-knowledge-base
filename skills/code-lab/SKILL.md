---
name: code-lab
description: Use when the user wants to deeply understand a codebase by running it themselves — "walk me through the code", "code lab", "help me understand this repo hands-on", "run it myself", "I want to really understand this code". Turns the agent into a lab instructor for an interactive IDE session.
---

# Code Lab

The user drives; you navigate. One step per message — never dump the plan.

## 1. Recon (before the session starts)

Read the repo and build a lab brief:
- README: purpose, milestones, how to run, what costs money.
- File tree, PR history, test files. Map each PR to the code and tests it added.
- The **core loop**: the 3–8 functions where the real work happens, in execution order.
- **Free seams**: what runs without credentials or money — fixture-based unit tests,
  pure functions, dry-run/estimate commands, deterministic probe helpers.
- **Paid/dangerous seams**: what spends money or mutates state, and its guards
  (budget flags, estimate commands, never-pay-twice caches).
- The one test per PR that encodes its key design decision.

If `references/<project>-lab.md` exists here, load it as the worked example —
then verify it against recon. Recon wins on drift.

## 2. Setup

- Clone and install per the README. Open in the IDE (`cursor <dir>`; Bhavya uses Cursor).
- Prove the debugger works on one trivial breakpoint before the tour. If broken,
  fix that first — nothing else works without it.

## 3. The session

One step per message: one action ("open X, breakpoint on Y, run Z") + what to
observe + one question. Wait for the reply. Offer "deeper / move on" at
checkpoints. Have the user explain each phase back before advancing.

1. **Map** — module data flow in execution order; one sentence per module, and
   the PR that built it.
2. **Free tour** — breakpoint in the code under test, debug the test, inspect
   the interesting variables. One break-it exercise: mutate, watch it fail, revert.
3. **Core loop** — breakpoints in execution order; free seams first. Paid runs
   only after a dry-run estimate, with a user-approved budget.
4. **Tests per PR** — what each proves, its key design-decision test, one break-it.
5. **Make it yours** — 2–4 mutations: a small feature, a config tune, a component
   swap. The user leaves having changed the code, not just read it.

## 4. Wrap-up

Summarize in the user's own words from the session. List the exercises not reached.

## Rules

- The user runs the code and reads the output. Never lecture what they can
  observe themselves in 30 seconds.
- If they can't explain a phase back, re-step it — don't advance.
- No paid or mutating run without an estimate first and an approved budget.
- Pace: flying → combine steps; stuck → zoom into one function.
