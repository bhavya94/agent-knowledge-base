---
name: demo
description: Prove a change works end to end by running the real thing and capturing evidence (terminal output, screenshots, API responses). Step 4 of the Build → Explainer → Reviewer → Demo workflow; nothing is done until this passes.
---

# Demo

Show the change working in the real system, not just in unit tests.

1. **Plan** — name the user-visible behavior to prove and the exact steps that exercise it,
   including at least one edge or failure case.
2. **Run** — launch the actual app, CLI, service, notebook, or pipeline. Use realistic inputs.
3. **Capture** — save evidence outside the project repo (e.g. the scratchpad): screenshots, command
   transcripts, request/response pairs, metrics or plots for ML work. The screenshots are the PR's proof,
   so follow `~/agent-knowledge-base/conventions/pull-requests.md`: UI screenshots for UI;
   for terminal-testable changes, an image of the command, the function or API call, and its output,
   with the call and result highlighted (`~/agent-knowledge-base/scripts/term-shot.sh`); a local database
   for data changes.
4. **Report** — the PR description's Proof and Verify sections are the report: one line per screenshot
   saying what it shows, and the commands to reproduce. Upload screenshots to the repo's `pr-assets`
   release as the convention describes; nothing from the demo is committed to the project.

If the demo fails, say so plainly, with the output — then fix and re-run. Don't call it done
on a partial or simulated run.
