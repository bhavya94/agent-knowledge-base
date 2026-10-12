# Code Structure Conventions

Starter conventions — refine as patterns emerge. A project's existing conventions always win.

## General
- Match the surrounding code: naming, comment density, error handling, module layout.
- Small, focused modules and functions; one responsibility each.
- DRY, but don't abstract until there are at least two real call sites.
- No dead code, commented-out blocks, or speculative flags.

## Python / ML
- Typed function signatures; dataclasses or pydantic models for configs and records.
- Separate data loading, feature/transform logic, modeling, and evaluation into distinct modules.
- Configs in files (YAML/TOML), not hard-coded constants; seed everything for reproducibility.
- Notebooks for exploration only — logic that ships moves into importable modules with tests.

## Layout and classes
Bhavya prefers an object-oriented design with a clear home for each piece of logic (reflective-qa refactor,
PRs #19–#23, 2026-10-11).
- **One package per responsibility**, named for what it owns: data, retrieval, agent, runs (files, API, money),
  eval, experiments, site, and one `cli.py`.
- **Imports point down only.** Write the layers in the README, and enforce them with a test that parses imports
  (reflective-qa `tests/test_layers.py`).
- **When several functions take the same state** (a config, rates, a client), make an object that owns it, and
  make the functions its methods.
- **A class must own state or a contract**, such as its config and collaborators. A `Writer` owns its run config and
  fingerprint. A `BatchRunner` owns its client and the budget guard. Don't make a class that only wraps one function.
- **Pure math stays functions** (metrics, normalization). **Records stay frozen dataclasses**, and they serialize
  themselves (`to_row()`).
- **Loaders are class methods:** `from_config()` for one object, `load_all()` for a named set.
- **Inject collaborators in the constructor.** Make one optional only when some methods don't need it (a report needs
  no API client), and say so in the docstring.
- **Only the CLI parses arguments or prints.** One entry point with subcommands (`[project.scripts]`), not
  `python -m` on library modules.

## Refactors
A refactor changes structure, not behavior. Prove that, don't assert it.
1. **Before the first edit, save golden outputs:** every command's output and every generated artifact.
2. **Pin identity hashes in a test:** cache keys, file-name fingerprints, anything that finds paid or slow results.
3. **After each step, compare byte for byte** with the golden outputs. Fix any difference before going on.
4. **Mutation-check new tests:** break the behavior on purpose and confirm the test fails.
5. **Run the suite at every commit in a fresh clone**, so each stacked PR stands on its own.

## Tests
- Test behavior through public interfaces; avoid mocking internals.
- Each bug fix gets a regression test that fails without the fix.
- **Use realistic test data**, not `foo`, `bar`, or `test1`. Pick values the code meets in real use: a real
  question, text with punctuation and Unicode, an ID in the real format. For example, write
  `question="Which datasets do they evaluate on?"`, not `question="foo"`. Realistic data shows what the code is for,
  and it finds bugs that placeholders hide. Keep each value as small as the test allows. Never copy customer or
  employer data: take values from a public dataset or write your own.
