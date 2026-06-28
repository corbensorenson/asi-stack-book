# Source Note: Integrated Task and Motion Planning

| Field | Value |
|---|---|
| Source ID | `ext_integrated_tamp_2020` |
| Source title | Integrated Task and Motion Planning |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2010.01083, https://arxiv.org/abs/2010.01083 |
| Citation label | Garrett et al. (2020), Integrated Task and Motion Planning |
| Published / updated | 2020-10-02 / 2020-10-02 |
| DOI | 10.48550/arXiv.2010.01083 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the planning/control literature queue; paper not vendored into this repository and no task-and-motion planning algorithm reproduced. |

## Thesis

Integrated task and motion planning belongs in the planning, runtime-adapter, and integrated-architecture chapters as an external reference for interfaces between discrete task planning and continuous motion or feasibility subproblems. It helps the ASI Stack talk about planner/runtime boundaries without pretending that a text plan is physically executable.

## Mechanisms

- Treat TAMP as an integration problem spanning discrete task planning, continuous motion planning, and mathematical programming subproblems.
- Characterize solution methods by how they solve continuous-space subproblems and integrate discrete and continuous search.
- Preserve the difference between high-level task order and low-level feasibility.
- Expose black-box subproblem interfaces as a design issue rather than hiding them inside one planner.

## Evidence

- The source surveys TAMP problem structure and algorithm families.
- This repository has not run any TAMP benchmark, motion planner, robot simulator, or physical execution trace.
- Use this source as external boundary vocabulary for planning/runtime integration, not as evidence that the ASI Stack can plan in physical environments.

## Failure Modes

- Discrete plans can ignore geometric, physical, timing, or sensing feasibility.
- Black-box feasibility checks can hide why a task failed or why a route was selected.
- A successful simulation or motion-planning result in another setting cannot become local runtime evidence without reproduction and scoped artifacts.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer)
- `planforge-dags-and-intelligence-arbitrage` (PlanForge DAGs and Intelligence Arbitrage)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Use this note to ground external discrete/continuous planning-boundary vocabulary.
- Do not claim that the ASI Stack implements TAMP, runs motion planning, or proves physical feasibility.
- Keep support state at `argument` until simulator traces, adapter fixtures, physical constraints, or accepted evidence transitions exist.

## Open Questions

- What runtime-adapter receipt should record a continuous feasibility check for a discrete plan node?
- How should simulation-fidelity records constrain planner claims about physical tasks?
- Which integration-trace fields would distinguish task decomposition failure from motion-feasibility failure?
