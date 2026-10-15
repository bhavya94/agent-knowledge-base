# Red Teaming LLM Applications

**Source:** DeepLearning.AI short course, built with Giskard, hosted by Andrew Ng with Matteo Dora and Luca Martial. **Date distilled:** 2026-10-15. **Status:** enrolled, read-only extraction. No account changes made.

**Course page:** https://learn.deeplearning.ai/courses/red-teaming-llm-applications

## Verdict
The safety counterpart to the crewAI course. Where crewAI taught how to build agent systems, this teaches how to break them, and the breaking discipline transfers directly to eval design. Modules 1 and 3 are the re-reads.

## Modules
1. [The Vulnerability Landscape](module-1-vulnerability-landscape.md) — why benchmarks are not safety tests; bias, info disclosure, service disruption, hallucinations; OWASP/AVID resources.
2. [Attack Techniques](module-2-attack-techniques.md) — text-completion exploits, bias-loaded hallucination questions, instruction injection, prompt-format reconnaissance.
3. [Automated Red Teaming](module-3-automated-red-teaming.md) — the automation ladder (hand-written + rules, prompt library, Giskard scan); LLM-generated adversarial inputs with LLM judges.
4. [Full Red Teaming Assessment](module-4-full-assessment.md) — ByteChapters case study: scoping, probing, incremental prompt extraction, chained refund exploit.

## Key takeaways
- Red teaming is eval with an adversarial generator: generate, execute, judge.
- The prompt is IP and a leak vector. Treat system prompts like secrets.
- Excessive agency (tool-equipped agents with weak instruction boundaries) is the highest-stakes category.
- Rule-based detection first, LLM judges second. Cheap layers catch cheap failures.
- Scope before you poke: categories, threat actors, rounds.

## Builds to steal
- **Adversarial input generator:** temperature-high LLM cast as red teamer, emitting JSON lists of requirement-targeted probes. Permanent fixture for my eval suite.
- **LLM safety judge:** evaluator prompt returning safe/unsafe per Q&A pair against an explicit requirement. Validate against human labels (Kappa) before trusting.
- **Scoped assessment template:** the ByteChapters round structure (probe → scan → recon → chain) as the checklist for any tool-equipped agent I ship.

## Notebooks
None. The course's hands-on notebooks were retired (models and libraries deprecated), so it is video-only. The code patterns from the videos (ZephyrApp probes, prompt_attempts loops, Giskard scan setup, ByteChapters assessment) are captured in the module notes above.
