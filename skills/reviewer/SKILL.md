---
name: reviewer
description: Adversarially review a change before it is called done — hunt for correctness bugs, missing tests, and design flaws at a Senior/Staff bar. Step 3 of the Build → Explainer → Reviewer → Demo workflow.
---

# Reviewer

Review the diff as a skeptical Staff engineer whose job is to block the merge.
If you can spawn a fresh subagent, do so, so the review isn't biased by having written the code.

## Checklist
1. **Correctness** — edge cases, error paths, concurrency, off-by-one, null/empty inputs, data leakage
   (train/test, PII).
2. **Tests** — do they test behavior rather than implementation? Would they fail if the feature broke?
   Run them.
3. **Design** — does it follow existing patterns in the codebase? Is it DRY? Is there a simpler design?
4. **Repo bar** — check past Senior/Staff review comments in the repo history
   (`gh pr list --state merged`, `gh api repos/{owner}/{repo}/pulls/{n}/comments`) and apply them.
5. **Cost & ops** — performance, infra cost, observability, rollback.

## Output
A ranked list of findings — `severity | file:line | issue | concrete failure scenario | fix`.
Verify each finding before reporting it; drop anything you can't back up. Fix the confirmed ones,
then re-run tests. An empty list is a valid result.
