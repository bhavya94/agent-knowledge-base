---
name: code-lab-breakpoint-print
description: In code labs Bhavya explores with breakpoint() and print in the terminal, not the IDE debugger UI
type: feedback
---

In code labs, Bhavya explores code by adding `breakpoint()` or `print(...)` lines and running from the terminal,
not by setting breakpoints in the Cursor debugger UI.

**Why:** Bhavya, 2026-10-16, at the start of the metrics-from-scratch PR #1 lab: "I am now adopting the
breakpoint() and print way of exploring code".
**How to apply:** Each lab step names the file and line to add `breakpoint()` (or a print) on, the exact
`uv run pytest ... -k <test>` or CLI command to run, and the pdb commands to type (`p x`, `pp x`, `n`, `s`, `c`).
Remind Bhavya to delete the added line (undo) before moving on. The `code-lab` skill holds this. Related:
[[teach-code-top-down]].
