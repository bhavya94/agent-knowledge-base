# Pull Request Conventions

A PR should be easy to review and verifiable on its own. A project's existing conventions win.

## Size and scope
- **One purpose per PR:** modular and focused, reviewable in one sitting.
- **Aim for about 300 changed lines or fewer.** Count hand-written code, tests, configs and README changes.
  Lockfiles and generated files don't count.
- **If it can't fit, use a stacked PR set, not one big PR:** for example data layer → feature → wiring.
  - The first PR targets `main`; each later PR targets the branch of the PR below it, so every diff shows
    only its own change.
  - Every PR description starts with its position, e.g. "Stack 2/3, based on #12".
  - Merge bottom-up. After each merge, retarget the next PR to `main`.
- **Each PR is independently verifiable:** it builds, its tests pass, and its demo runs without any later PR.

## What gets merged
Only what the code needs: code, tests, configs, and the README. PR artifacts never enter the codebase:
- **Screenshots** live on the repo's `pr-assets` pre-release (below).
- **Explainers** live in `~/agent-knowledge-base/projects/<repo>/explainers/<YYYY-MM-DD>-<topic>.md`, with code
  cited as commit-pinned links (`scripts/explainer-permalinks.py`). The knowledge base is public: for a private
  or employer repo, post the explainer as a PR comment instead.
- **Demo reports** are the PR description's Proof section; transcripts stay local.

## Proof, captured when the PR is created
Run the demo skill. Screenshots go in the PR description, never in the code.
- **UI:** screenshots of the affected screens, with before and after for a change.
- **Testable from a terminal:** run it in a local terminal and capture an image showing the command,
  the function or API call being exercised, and its output. Highlight the call and the result that matters.
  Text transcripts can go alongside, but the PR shows images.
  Helper: `~/agent-knowledge-base/scripts/term-shot.sh <out.png> '<command>' ['<highlight regex>']`.
- **Data:** use a local database (SQLite, or Postgres in Docker), never a shared or production one.
  Show the query and the rows before and after.
- **Include at least one failure or edge case.**
- **Host images on a `pr-assets` pre-release:** GitHub has no API for uploading images into a PR description,
  so images need a URL. Release files have an official upload command, stay out of git history, aren't
  downloaded by `git clone`, and are only as visible as the repo itself.
  1. Once per repo: `gh release create pr-assets --prerelease --target main --title "PR assets (not a release)"
     --notes "Screenshots embedded in pull request descriptions. Not a software release."`
  2. Open the PR, then upload with the PR number in each name: `gh release upload pr-assets pr<N>-<k>-<slug>.png`.
  3. Embed `https://github.com/<owner>/<repo>/releases/download/pr-assets/pr<N>-<k>-<slug>.png`, then
     `gh pr edit <N> --body-file ...`.
  These files are served as generic downloads; Chrome displays them inline (verified 2026-10-09).

## Description: concise and proof-driven
Show what the PR achieves; don't narrate it. Use this template:

```markdown
## What
One or two sentences: what this PR achieves and why.

## Proof
![short alt text](<pr-assets release URL>)
One line per image: what it shows.

## Verify
The command(s) a reviewer runs to see it themselves.

## Notes
Optional. Only what the reviewer must know: follow-ups, risks, decisions needing sign-off.
Link the explainer in the knowledge base for the why.
```

- No changelogs or file-by-file lists. The diff and the explainer already cover them.
