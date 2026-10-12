---
name: code-lab
description: Use when the user wants to deeply understand a codebase or a PR by running it themselves — "walk me through the code", "code lab", "lab on this PR", "help me understand this repo hands-on", "run it myself", "I want to really understand this code" — and after each PR opens (AGENTS.md workflow). Turns the agent into a lab instructor for an interactive IDE session.
---

# Code Lab

The user drives; you navigate. One step per message — never dump the plan.

**Teach top-down.** First the main flow: the classes and calls that do the work, traced once end to end.
Then narrow down to contracts and edge cases. A detail makes sense only after the user has seen the call
that uses it.

## 1. Scope

- If the lab follows a PR, or the user names one: cover only that PR's change, in 3–6 steps.
  Small labs stay digestible.
- If the user asks for the whole repo: use the same order with more steps. Offer a stop at each part.

## 2. Recon (before the session starts)

Read the repo and build a lab brief:
- README: purpose, milestones, how to run, what costs money.
- File tree, PR history, test files. Map each PR to the code and tests it added.
- For one PR: its diff and its explainer. The explainer's diagram is the map.
- The **main path**: the 3–8 classes and calls where the real work happens, in execution order.
- **Free seams**: what runs without credentials or money — fixture-based unit tests,
  pure functions, dry-run/estimate commands, deterministic probe helpers.
- **Paid/dangerous seams**: what spends money or mutates state, and its guards
  (budget flags, estimate commands, never-pay-twice caches).
- The one test per PR that encodes its key design decision.

If `references/<project>-lab.md` exists here, load it as the worked example —
then verify it against recon. Recon wins on drift.

## 3. Setup

- Clone and install per the README. Open in the IDE (`cursor <dir>`; Bhavya uses Cursor).
- Prove the debugger works on one trivial breakpoint before the tour. If broken,
  fix that first — nothing else works without it.

## 4. The session

One step per message: one action ("open X, breakpoint on Y, run Z") + what to
observe + one question. Wait for the reply. Offer "deeper / move on" at
checkpoints. Have the user explain each part back before advancing.

1. **Map** — the main path in execution order, one sentence per class or call. For one PR:
   what calls the new code, the new code, and what uses its output.
2. **Main path** — one breakpoint per main call, in execution order, on a real or fixture input.
   At each stop, the user reads what goes in and what comes out. Free seams first. Paid runs
   only after a dry-run estimate, with a user-approved budget.
3. **Outcome** — what the code produces, and how the user checks it (a report, a score, a file).
4. **Details** — one class at a time: its key design-decision test, its edge cases, then one
   break-it: mutate, watch it fail, revert.
5. **Make it yours** — 2–4 mutations: a small feature, a config tune, a component
   swap. The user leaves having changed the code, not just read it.

## 5. Wrap-up

Summarize in the user's own words from the session. List the exercises not reached.

## Rules

- Don't open an edge case, a parser branch or a helper until the user has traced the main call
  that uses it.
- If the user asks for the answer ("you tell me") or says they are lost, don't advance. Answer in
  two or three sentences, show where that step sits on the map, and ask: continue, or zoom out?
- The user runs the code and reads the output. Never lecture what they can
  observe themselves in 30 seconds.
- If they can't explain a part back, re-step it — don't advance.
- No paid or mutating run without an estimate first and an approved budget.
- Revert a break-it with undo (Cmd+Z, then save), not `git checkout`: that also discards the
  user's other changes in the file.
- Pace: flying → combine steps; stuck → zoom into one function.
