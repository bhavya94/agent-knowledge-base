---
name: learn-org-patterns
description: Study an org's codebase and its Senior/Staff engineers' review comments to extract recurring patterns, conventions, and review standards, then record them for future work. Use when starting in a new repo or team, or before tackling an unfamiliar area.
---

# Learn Org Patterns

## 1. Codebase patterns
Survey the repo, sampling rather than reading everything: module layout, error handling, config,
logging, testing style, data/ML pipeline structure, and naming. Note one canonical example file for each.

## 2. Review comments
- Identify senior reviewers (CODEOWNERS, frequent approvers, or names the user provides).
- Pull their comments: `gh api "repos/{owner}/{repo}/pulls/comments?per_page=100"` and
  `gh pr list --state merged --search "reviewed-by:<user>"`, then each PR's review comments.
- Cluster the comments into recurring themes: what they push back on, what they praise, what
  they ask for before approving.

## 3. Record
- Repo-specific findings go in that repo's own docs (or `CLAUDE.md`), not here.
- General lessons that transfer go into `~/agent-knowledge-base/conventions/` or a memory via the
  `remember` skill, with **no** proprietary code, names, or confidential details, because this repo is public.

## 4. Apply
When planning new work in that repo, cite the patterns and review themes that apply, and have the
`reviewer` skill check the diff against them.
