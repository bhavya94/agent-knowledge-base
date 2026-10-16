# Module 3 — GPA: Goal-Plan-Act Alignment and Runtime Improvement

**Course:** Building and Evaluating Data Agents (DeepLearning.AI, with Snowflake) **Date:** 2026-10-15 **Verdict:** the course's original contribution. GPA is the process-eval framework I did not have a name for.

## What problem?
Output evals (the RAG triad) tell you the answer was bad. They do not tell you whether the plan was wrong, the plan was ignored, the execution wasted steps, or the reasoning contradicted itself. For agents, the process is where the failures live.

## What idea?
**GPA: Goal-Plan-Act alignment.** A data agent is trustworthy when its goal, plan, and actions line up. Four failure modes, each with its own evaluator:
1. **Plan Quality:** the plan must be specific, feasible, and tied to the goal, with explicit filters, thresholds, prioritization logic, and a defined output schema. Failure: vague steps, missing thresholds, unclear outputs.
2. **Plan Adherence:** the trace must show the plan actually being followed. Failure: a missing date filter, a partially applied filter, an output that does not match the planned schema.
3. **Execution Efficiency:** flag redundancy and preventable waste. Failure: duplicate work, redundant retrieval, unrequested outputs (YAGNI as an eval criterion).
4. **Logical Consistency:** catch contradictions and ungrounded assumptions. Failure: a count that changes after a filter is applied, actions that mismatch recorded state.

The diagnostic payoff: GPA metrics tell you where in the goal → plan → act chain the agent broke, not just that it broke.

**Improvement loop:** measure, then make targeted changes and validate. The course makes two. First, **prompt surgery on the planner**: each plan step now carries explicit goals, pre-conditions, and post-conditions, which improves the executor's tool selection and routing. Second, **inline evaluations**: a decorator wraps the context-relevance feedback onto the research nodes, so at every retrieval step the agent scores whether the collected data is relevant and can adjust its plan at runtime. Evaluation moves from a post-hoc dashboard into the live control loop. The improved agent is registered as a new version and compared against the previous one on the same queries in the dashboard.

## Why it matters
- GPA is the missing half of agent evals. Triad judges grade outputs; GPA judges grade the process. A serious agent eval suite needs both.
- Inline evals are the runtime version of the same idea: an agent that can notice irrelevant retrieval mid-run and replan is categorically more robust than one graded after the fact.
- Plan steps with pre/post-conditions is a small prompt change with outsized effect, worth testing in any planner I write.

## How I'd use it
- **Roadmap Phase 2 (judge):** add GPA-style process judges to the eval design: plan quality and plan adherence judges over traces, alongside the triad's output judges.
- **Roadmap Phase 3 (harness):** inline eval hooks at retrieval steps, with the score wired into the replan decision. This is the sentinel pattern from my agent work, given a concrete implementation.

## Open questions
- GPA evaluators are themselves LLM judges here. Their agreement with human process audits is unmeasured in the course; same Kappa caveat as every judge in this distillation set.
