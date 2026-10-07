---
name: kb-sync
description: Commit and push pending changes in ~/agent-knowledge-base (memory, skills, notes) to GitHub. Use when the user says "sync the knowledge base", "push my notes", or runs /kb-sync.
disable-model-invocation: true
---

# KB Sync

The repo is public. Review before pushing.

1. `cd ~/agent-knowledge-base && git pull --rebase --autostash && git status --short`.
   If nothing changed, say so and stop.
2. Read the diff (`git diff` plus any new files). Stop and flag anything that is secret, confidential,
   customer data, or personal (job search, compensation, opinions about people). Don't commit it.
3. Check every new memory file has a line in `memory/MEMORY.md`, and every index line points to a file
   that exists.
4. `git add -A && git commit -m "<summary of what changed>"`, then `git push`.
5. Report the commit hash and the files changed.
