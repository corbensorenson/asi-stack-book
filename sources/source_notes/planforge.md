# Source Note: PlanForge

| Field | Value |
|---|---|
| Source ID | `planforge` |
| Source title | PlanForge |
| Ingestion date | 2026-06-24 |
| Source version / URL | Version 1.0, December 26 2025; https://docs.google.com/document/d/12mSs7u6JxrtVQ_GbNpBY7lXCA5uyE62Lx91gi_VRjgo |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/planforge.txt`; raw text is not published. |

## Thesis

PlanForge is a planning middleware layer that compiles natural-language goals into optimized, parallelized, tier-aware execution schedules. It decouples planning from execution so heterogeneous workers can be scheduled by dependency, cost, capability tier, and fallback requirements.

## Mechanisms

- Recursive hierarchical decomposition from goal to primitive action schema.
- Plan optimization and verification through deduplication, subtree merging, consistency checks, and pre/postcondition annotation.
- Minimum viable intelligence tier annotation for each primitive.
- Dependency inference and scheduling across available workers.
- Execution handoff with feedback loops for failure-driven replanning.

## Evidence

- The source is a whitepaper/conceptual design with implementation considerations.
- It references planning traditions such as HTN, TAMP, behavior trees, GOAP, LLM agent frameworks, and learned plan generators as related work.
- It does not provide book-repo benchmark results or a verified implementation in this project.

## Failure Modes

- Redundant subtasks, poor dependency modeling, sequential bottlenecks, overuse of expensive cognition, and brittle coupling to executors.
- Inadequate primitive schemas or hidden preconditions can make a formally tidy DAG operationally invalid.
- Tier classifiers can under-assign difficult subtasks unless escalation and residual handling are explicit.

## Book Chapters Supported

- Planning as a Control Layer
- PlanForge DAGs and Intelligence Arbitrage
- Intent-to-Execution Contracts
- Resource Economics and Token Budgets
- Integrated Reference Architecture

## Claims To Add Or Update

- Treat planning as a control layer that emits typed, dependency-aware work rather than prose.
- Use PlanForge for the MVI/tier-routing vocabulary, while keeping execution authority outside the planner.
- Formalize DAG acyclicity, dependency precedence, and failed-quality escalation as priority proof/test targets.

## Open Questions

- Which primitive schema should the book use for examples?
- Should PlanForge's scheduler be prototyped in `experiments/planforge/` before drafting implementation claims?
- How should human workers and tool workers be represented in the same schedule without authority confusion?
