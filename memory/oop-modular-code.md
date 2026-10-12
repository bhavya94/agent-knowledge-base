---
name: oop-modular-code
description: Bhavya prefers an object-oriented design with a clear module for each responsibility over flat modules of free functions
type: feedback
---

Bhavya likes an object-oriented approach, with a clear modular division of where each piece of logic lives.
Group code into subpackages by responsibility (data, retrieval, agent, runs, eval, site, cli). Give classes the
state and behavior that belong together (a batch runner owns its client, costs and run directory). Keep the
command-line entry points out of library modules.

**Why:** Bhavya, 2026-10-11, on reflective-qa's flat package: "i like Object oriented appraoch and clear modular
division of where each logic lives".
**How to apply:** Design new projects this way from the start, and propose the class layout before building it.
Keep it Pythonic: pure, stateless math (token F1, normalization) stays as functions, and frozen dataclasses stay the
records. A class must own state or a contract, not only wrap one function. Related: [[reflective-qa-project]],
[[user-profile]].
