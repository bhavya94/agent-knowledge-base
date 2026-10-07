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

## Tests
- Test behavior through public interfaces; avoid mocking internals.
- Each bug fix gets a regression test that fails without the fix.
