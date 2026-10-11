---
name: write-skill
description: Use when creating a skill, editing a skill, or adapting a skill from another repo into ~/agent-knowledge-base/skills.
---

# Write a skill

A skill is a reusable technique, not a story about one session. Treat it like code: test it first.

## 1. Baseline (red)
1. Write 2–3 scenarios where the skill should change what an agent does. For a rule that agents skip under
   pressure, combine pressures: time, sunk cost, authority, and a user who says "just do it".
2. Prefer a real task in a scratch repo over a multiple-choice question. A labeled menu shows the right
   answer, so a strong model usually picks it.
3. Run each scenario with a subagent that doesn't have the skill. Record its choice and reasons word for word.
4. If the baseline already does the right thing, make the scenario harder. If it still passes, you don't
   need the skill for that case.

When you adapt a skill from another repo, reuse its tests if it has them. Say which ones you skipped and why.

## 2. Write (green)
1. Address only the failures you saw. Every line costs context in each session that loads the skill.
2. Pick the form from the failure:

   | Failure in the baseline | Write | Not |
   |---|---|---|
   | Knows the rule, skips it under pressure | A firm rule, the excuses you saw, and stop signs | Soft advice ("consider…") |
   | Output has the wrong shape | A recipe: the parts of the output, in order | A list of "don't" |
   | Leaves out a required part | A required slot in the template | A reminder near the template |
   | Depends on a condition | "If <something you can observe>, do X" | A rule with exceptions |

3. Don't add "unless it matters" clauses. They reopen the rule. Write a real exception as its own condition.
4. Frontmatter: `name` matches the folder (lowercase and hyphens). `description` starts with "Use when" and
   lists triggers and symptoms. Don't summarize the steps there: an agent may follow the summary and skip the body.
5. Write at about 80% of ASD-STE100 (`AGENTS.md` → Communication), and check it with `scripts/ste-check.py`.
   One good example beats several weak ones.
6. Link to other skills and `AGENTS.md` rules by name. Don't repeat them.

## 3. Verify (refactor)
1. Run the same scenarios with the skill. A pass means the agent picks the right action for the skill's reasons.
2. If the agent finds a new excuse, close it in the skill and run again.
3. When output quality matters more than discipline, use `skill-creator` (synced from claude.ai) to run evals
   and tune the description.
4. Report the baseline and the with-skill result for each scenario. Say what you didn't test.

## 4. Ship
1. Link it: `ln -s ~/agent-knowledge-base/skills/<name> ~/.claude/skills/<name>`. New sessions load it.
2. Add it to the skills list in `README.md` and to Core skills in `notes/ai-coding.md`.
3. Before you adapt a skill from another repo, check its license. For MIT or Apache-2.0, rewrite it in our
   words, end with a source line that names the commit, and add the license to `THIRD_PARTY_NOTICES.md`.
   For no license or a proprietary one, link to it and don't copy. The repo is public (`AGENTS.md`).
4. Use one commit per skill. Test each skill before you start the next.

---
Adapted from [obra/superpowers](https://github.com/obra/superpowers) `skills/writing-skills` at commit
`bb92a77` (MIT). See `THIRD_PARTY_NOTICES.md`.
