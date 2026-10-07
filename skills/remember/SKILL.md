---
name: remember
description: Save a durable fact (user preference, feedback, project context, reference) to the shared agent knowledge base so every agent sees it. Use when the user says "remember", corrects how you work, or you learn something non-obvious that future sessions need.
---

# Remember

Memory lives in `~/agent-knowledge-base/memory/`, shared by all agents.

1. Read `memory/MEMORY.md`. If an existing memory covers the fact, update that file instead of adding one.
   Delete memories that turn out to be wrong.
2. Write one fact per file, `memory/<kebab-slug>.md`:

   ```markdown
   ---
   name: <kebab-slug>
   description: <one-line summary used to judge relevance>
   type: user | feedback | project | reference
   ---

   <the fact>
   **Why:** <reason — feedback/project only>
   **How to apply:** <when it matters — feedback/project only>
   ```

   Link related memories with `[[other-slug]]`. Use absolute dates, not "next week".
3. Add one line to `memory/MEMORY.md`: `- [Title](<slug>.md) — hook`.

Don't save: what the code or git history already records, one-conversation details, or anything
secret, confidential, or personal (job search, compensation, opinions about people) — this repo is public.
