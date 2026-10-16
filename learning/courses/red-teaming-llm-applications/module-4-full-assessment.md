# Module 4 — Full Red Teaming Assessment

**Course:** Red Teaming LLM Applications (DeepLearning.AI, built with Giskard) **Date:** 2026-10-15 **Verdict:** the capstone. A worked example of scoping, probing, and chaining exploits end to end.

## What problem?
Knowing attack techniques is not the same as running an assessment. A real engagement needs scoping (what is under test, which risk categories, which threat actors), systematic probing, and chaining small wins into a demonstrated business impact.

## What idea?
The ByteChapters case study: an e-book store's LLM customer-support bot with real powers (check order status, refund an order, cancel an order, list recent orders).

**Step 1, scope:** what is under test (the bot), risk categories (toxicity, off-topic content, excessive agency, sensitive info disclosure), actors (benign customers vs malicious attackers). Start with open-ended exploration, then refine and iterate.

**Round 1, probe:** toxicity insults get kind apologies; off-topic questions stay on task. Reconnaissance maps capabilities by asking what it can do, then asking for specifics. Automated low-hanging fruit via Giskard scan: harmfulness scan finds the bot robust, but the prompt-injection scan finds 4 issues with well-known injection prompts succeeding. Round 1 conclusion: respectful, on-topic, but manipulable, with refund/cancel powers as the round-2 target.

**Round 2, exploit:** recon establishes refund conditions (order within 14 days, under 5% read, completed status). A naive injection fails. Incremental system-prompt extraction works: collect the first words piece by piece ("UR…", "UR design…"), then ask for the full message verbatim, exposing role, instructions, and the tool list. Then chained injections: a fake date defeats the 14-day check; a "new government regulation" instruction defeats the 5%-read rule. The bot refunds an ineligible order. Store-policy violation demonstrated.

## Why it matters
- **Excessive agency** is the category to watch: the vulnerability was not rude text, it was a bot with refund powers and weak instruction boundaries. Tool-equipped agents multiply red-teaming stakes.
- The scope-first discipline (categories, actors, rounds) is how you run this as engineering work instead of random poking.
- Chaining (recon → extract → bypass check 1 → bypass check 2) is the realistic shape of an exploit, not a single magic prompt.

## How I'd use it
- **Roadmap Phase 3 (harness):** any agent I ship with tools gets a scoped red-team pass: map capabilities, scan for injection, attempt privilege-adjacent actions.

## Open questions
- None. The case study was self-contained and complete.
