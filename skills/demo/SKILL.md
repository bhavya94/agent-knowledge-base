---
name: demo
description: Prove a change works end to end by running the real thing and capturing evidence (terminal output, screenshots, API responses). Step 4 of the Build → Explainer → Reviewer → Demo workflow; nothing is done until this passes.
---

# Demo

Show the change working in the real system, not just in unit tests.

1. **Plan** — name the user-visible behavior to prove and the exact steps that exercise it,
   including at least one edge or failure case.
2. **Run** — launch the actual app, CLI, service, notebook, or pipeline. Use realistic inputs.
   For a web UI, drive it with the Playwright plugin's browser tools: each step of the flow and the edge case,
   with a screenshot of each (setup in `visualize` → Check).
3. **Capture** — save evidence outside the project repo (e.g. the scratchpad): screenshots, command
   transcripts, request/response pairs, metrics or plots for ML work. The screenshots are the PR's proof,
   so follow `~/agent-knowledge-base/conventions/pull-requests.md`. Use UI screenshots for UI. For a
   terminal-testable change, capture an image of the command, the function or API call, and its output,
   with the call and result highlighted (`~/agent-knowledge-base/scripts/term-shot.sh`). Use a local
   database for data changes.
4. **Report** — the PR description's Proof and Verify sections are the report: one line per screenshot
   saying what it shows, and the commands to reproduce. Upload screenshots to the repo's `pr-assets`
   release as the convention describes; nothing from the demo is committed to the project.

If the demo fails, say so plainly, with the output — then fix and re-run. Don't call it done
on a partial or simulated run.

Proof for common claims (`AGENTS.md` → Evidence before claims). Adapted from Superpowers'
`verification-before-completion`; see `THIRD_PARTY_NOTICES.md`.

| Claim | Proof | Not proof |
|---|---|---|
| Tests pass | A fresh run with 0 failures | An earlier run; "should pass" |
| Bug fixed | The original symptom is gone when you re-run it | "The code changed" |
| Regression test works | It fails without the fix and passes with it | It passes once |
| Build works | The build command exits 0 | The linter passes |
| A subagent finished | Its diff, checked by you | Its report |
| Requirements met | Each item in the spec, checked | The tests pass |

For visual output (UI, HTML, plots, renders), mark the result "needs human eyes" and attach the
screenshots. Agents still can't audit visual work well, so don't claim it looks right from the code.
