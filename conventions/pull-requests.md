# Pull Request Conventions

A PR should be easy to review and verifiable on its own. A project's existing conventions win.

## Size and scope
- **One purpose per PR:** modular and focused, reviewable in one sitting.
- **Aim for about 300 changed lines or fewer.** Count hand-written code, tests, configs and docs.
  Lockfiles, generated files and raw captures (transcripts, images) don't count.
- **If it can't fit, use a stacked PR set, not one big PR:** for example data layer → feature → wiring.
  - The first PR targets `main`; each later PR targets the branch of the PR below it, so every diff shows
    only its own change.
  - Every PR description starts with its position, e.g. "Stack 2/3, based on #12".
  - Merge bottom-up. After each merge, retarget the next PR to `main`.
- **Each PR is independently verifiable:** it builds, its tests pass, and its demo runs without any later PR.

## Proof, captured when the PR is created
Run the demo skill and commit its screenshots to `docs/demos/<YYYY-MM-DD>-<topic>/`.
- **UI:** screenshots of the affected screens, with before and after for a change.
- **Testable from a terminal:** run it in a local terminal and capture an image showing the command,
  the function or API call being exercised, and its output. Highlight the call and the result that matters.
  Text transcripts can go alongside, but the PR shows images.
  Helper: `~/agent-knowledge-base/scripts/term-shot.sh <out.png> '<command>' ['<highlight regex>']`.
- **Data:** use a local database (SQLite, or Postgres in Docker), never a shared or production one.
  Show the query and the rows before and after.
- **Include at least one failure or edge case.**
- **Embed images by commit SHA:** `https://github.com/<owner>/<repo>/raw/<commit-sha>/docs/demos/<dir>/<file>.png`.
  Relative paths don't render in PR descriptions, and branch URLs break once the branch is deleted.

## Description: concise and proof-driven
Show what the PR achieves; don't narrate it. Use this template:

```markdown
## What
One or two sentences: what this PR achieves and why.

## Proof
![short alt text](<sha-pinned image URL>)
One line per image: what it shows.

## Verify
The command(s) a reviewer runs to see it themselves.

## Notes
Optional. Only what the reviewer must know: follow-ups, risks, decisions needing sign-off.
Link the explainer for the why.
```

- No changelogs or file-by-file lists. The diff and the explainer already cover them.
