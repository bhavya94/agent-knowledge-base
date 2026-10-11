---
name: debug
description: Use when a bug, test failure, crash, flaky test, wrong metric, or other unexpected behavior appears, before proposing or making a fix. Also use when a fix did not work.
---

# Debug

Find the root cause before you change code. A fix for a symptom is not a fix.
This rule applies when the bug looks simple, when time is short, and when the user says "just fix it".

## 1. Investigate
1. Read the full error and stack trace. Note the files, lines, and error codes.
2. Reproduce it and write down the exact steps. If you can't reproduce it, collect more data. Don't guess.
3. Check what changed: `git diff`, recent commits, dependencies, config, and environment.
4. If the system has several components, log what goes in and out at each boundary. Run it once to find
   the component that breaks. Then investigate only that component.
5. Trace the bad value back up the call chain to where it starts. Fix it there.

For ML results (a metric moved, two runs differ), fix the seed and the data sample first. Then compare the
inputs, config, and data version before you suspect the model or the code.

## 2. Compare
1. Find similar code that works in the same repo.
2. If you follow a reference implementation, read all of it.
3. List every difference between the working case and the broken case. Don't skip a difference because it
   "can't matter".

## 3. Test one hypothesis
1. Write it down: "X causes this because Y."
2. Make the smallest change that tests it. Change one thing at a time.
3. If the hypothesis is wrong, form a new one. Don't stack fixes.
4. If you don't understand something, say so.

## 4. Fix
1. Write a test that fails because of the bug (`AGENTS.md` → Success criteria first).
2. Make one fix at the root cause. No "while I'm here" changes (`AGENTS.md` → Surgical diffs).
3. Show that the test passes, the other tests pass, and the original symptom is gone
   (`AGENTS.md` → Evidence before claims).
4. If the fix fails, go back to step 1 with what you learned.
5. **After three failed fixes, stop.** When each fix exposes a new problem somewhere else, the design is
   probably wrong. Tell the user what you tried and ask before you try a fourth fix.

## Live incidents
Mitigate first with a known-safe action, such as a rollback or a feature flag. A mitigation is not a fix.
Keep the issue open and do steps 1–4 after. Don't ship a guess (a retry, a longer timeout) as the mitigation.

## Stop signs
If you think or see one of these, go back to step 1:
- "Quick fix now, investigate later."
- "Let me try X and see."
- "It's probably X," with no evidence.
- "I'll change a few things and run the tests."
- A `sleep` or a longer timeout makes a test pass. Wait for the real condition instead.
- "One more fix" after two fixes failed.
- The user says "stop guessing" or asks "is that actually happening?".
- A senior person says "trust me". Their idea is a hypothesis. Test it like any other.

## No root cause
Sometimes the cause is outside your control, such as timing or an external service. Then say what you
checked, add handling (a retry, a timeout, a clear error), and add logging for next time. Most "no root
cause" results are an incomplete investigation, so check step 1 again first.

## After the fix
If bad data passed through several layers, add a check at each layer. Then another path can't bring the
bug back.

---
Adapted from [obra/superpowers](https://github.com/obra/superpowers) `skills/systematic-debugging` at commit
`bb92a77` (MIT). See `THIRD_PARTY_NOTICES.md`.
