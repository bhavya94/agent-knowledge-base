---
name: visualize
description: Build a transient, single-file HTML page to explain or visualize something — a data flow, a pipeline run, eval results, a before/after, a design trade-off — check it with headless Chrome, and open it in the user's browser. Use when a picture or interactive view would explain faster than text or a Mermaid diagram.
---

# Visualize

Quick, throwaway web pages for understanding — not products. They can beat Mermaid when the idea has
many states, real data, comparisons, or something to click through.

## When to use
- Flows with branches or state over time (an agent loop, a retry path, a pipeline run).
- Real data: eval scores, distributions, confusion matrices, cost vs. quality.
- Before/after comparisons of outputs, prompts, or diffs.
- Anything the user would otherwise read three paragraphs to understand.
Use Mermaid when a static box-and-arrow diagram is enough.

## Build
1. **One question per page.** Put the answer in the title, e.g. "Why recall@5 drops on long papers".
2. **One self-contained `index.html`.** Inline CSS and JS. Libraries from a CDN are fine (D3, Chart.js,
   Mermaid). No build step, no server.
3. **Real data only.** Load or inline the actual numbers, files, or outputs. Never invent sample data; if
   data is missing, say so on the page.
4. **Readable at a glance.** Text at about 80% of ASD-STE100 (`AGENTS.md` → Communication), labeled axes
   and units, light and dark mode, works at laptop width.
5. **Location.** The session scratchpad if the harness provides one; otherwise `/tmp/agent-views/<topic>/`.
   Don't commit it to a project repo. It is transient by design.

## Check
Render it with headless Chrome and look at the screenshot before showing the user:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --window-size=1440,900 --screenshot=<dir>/shot.png "file://<dir>/index.html"
```

Fix anything broken or empty. For a PDF instead of a screenshot, use `--print-to-pdf=<file>`.
Visual quality still needs human eyes (`demo` skill), so say what you checked and what you couldn't.

## Show
Open it for the user with `open <dir>/index.html`, and give one or two sentences on what to look at.
Share it outside the machine (for example as a published Artifact) only when the user asks.
If the page proves useful beyond this session, offer to keep it next to the explainer (`explainer` skill).
