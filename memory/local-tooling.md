---
name: local-tooling
description: Bhavya's Mac tooling quirks — where freeze lives, why Homebrew tap installs fail, no `timeout` command
type: reference
---

- `freeze` v0.2.2 (terminal screenshots, used by `scripts/term-shot.sh`) is installed from its GitHub release at
  `~/.local/bin/freeze`. `~/.local/bin` is not on PATH, so call it by full path.
- As of 2026-10-09, Homebrew refuses third-party tap installs because the Xcode Command Line Tools are out of date
  for macOS 15. Updating them needs `sudo`, so that's Bhavya's call; until then, prefer verified release binaries.
- macOS has no `timeout`; use `perl -e 'alarm N; exec @ARGV' <cmd>`.

See [[reflective-qa-project]].
