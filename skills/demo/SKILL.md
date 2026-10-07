---
name: demo
description: Prove a change works end to end by running the real thing and capturing evidence (terminal output, screenshots, API responses). Step 4 of the Build → Explainer → Reviewer → Demo workflow; nothing is done until this passes.
---

# Demo

Show the change working in the real system, not just in unit tests.

1. **Plan** — name the user-visible behavior to prove and the exact steps that exercise it,
   including at least one edge or failure case.
2. **Run** — launch the actual app, CLI, service, notebook, or pipeline. Use realistic inputs.
3. **Capture** — save evidence to `docs/demos/<YYYY-MM-DD>-<topic>/` in the project: command
   transcripts, screenshots, request/response pairs, metrics or plots for ML work.
4. **Report** — a short `README.md` in that folder: what was demonstrated, steps to reproduce,
   expected vs. observed results, links to captures.

If the demo fails, say so plainly, with the output — then fix and re-run. Don't call it done
on a partial or simulated run.
