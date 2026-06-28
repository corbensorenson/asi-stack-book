# Source Note: Behavior Trees in Robotics and AI: An Introduction

| Field | Value |
|---|---|
| Source ID | `ext_behavior_trees_robotics_ai_2017` |
| Source title | Behavior Trees in Robotics and AI: An Introduction |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1709.00084, https://arxiv.org/abs/1709.00084 |
| Citation label | Colledanchise and Ogren (2018), Behavior Trees in Robotics and AI |
| Published / updated | 2017-08-31 / 2022-10-25 |
| DOI | 10.1201/9780429489105 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the planning/orchestration literature queue; book text not vendored into this repository and no behavior-tree controller reproduced. |

## Thesis

Behavior trees belong in the planning and runtime chapters as an external reference for modular, reactive task-switching structures. They help the ASI Stack compare PlanForge-style DAG planning with a different control idiom: trees that make local success, failure, running, fallback, sequence, and reactive switching boundaries explicit.

## Mechanisms

- Structure switching between tasks for autonomous agents such as robots or virtual entities.
- Use modular and reactive control nodes to compose larger behavior from smaller behaviors.
- Relate behavior trees to earlier switching structures and planning methods.
- Analyze properties such as safety, robustness, and efficiency through state-space descriptions.
- Extend behavior trees with stochastic outcomes to reason about success probability and time to completion.

## Evidence

- The source is an external book/arXiv reference for behavior-tree vocabulary, formal analysis hooks, and planning integration.
- This repository has not implemented a behavior-tree interpreter, imported behavior-tree examples, run a robotics controller, or reproduced stochastic behavior-tree calculations.
- Use the source as comparison vocabulary for planning control and runtime gating, not as evidence that ASI Stack planning works.

## Failure Modes

- A reactive tree can hide global plan quality if local nodes succeed while the broader objective drifts.
- Tree execution can look explainable while omitting authority, evidence, context, rollback, or residual fields.
- Imported robustness language can become misleading if no local controller, simulator, or proof obligation is reproduced.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer)
- `planforge-dags-and-intelligence-arbitrage` (PlanForge DAGs and Intelligence Arbitrage)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Use this note to compare PlanForge DAGs against modular reactive control structures.
- Do not claim behavior-tree safety, robustness, or efficiency for the ASI Stack without local formalization or execution traces.
- Keep support state at `argument` until behavior-tree adapters, fixtures, proofs, or accepted evidence transitions exist.

## Open Questions

- What PlanForge-to-behavior-tree adapter would preserve authority, residual, verification, and rollback fields?
- Which behavior-tree node statuses correspond to ASI Stack blocked, quarantined, escalated, or replanned states?
- Can stochastic behavior-tree accounting inform residual escrow or readiness gates without becoming a benchmark shortcut?
