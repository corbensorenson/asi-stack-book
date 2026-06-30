# Source Note: Three States and a Plan: The A.I. of F.E.A.R.

| Field | Value |
|---|---|
| Source ID | `ext_three_states_plan_fear_2006` |
| Source title | Three States and a Plan: The A.I. of F.E.A.R. |
| Ingestion date | 2026-06-28 |
| Source version / URL | GDC Vault page, https://gdcvault.com/play/1013282/Three-States-and-a-Plan |
| Citation label | Orkin (2006), Three States and a Plan |
| Published / updated | 2006 /  |
| DOI |  |
| Ingestion basis | Primary GDC Vault page inspected for the planning/orchestration literature queue; talk media, slides, game code, and planner traces are not vendored into this repository. |

## Thesis

The F.E.A.R. planning talk belongs in the planning and runtime chapters as an external reference for Goal Oriented Action Planning under real-time action-game constraints. It gives the ASI Stack a concrete comparison point for practical planning systems that must operate under latency, CPU, agent-behavior, and higher-level coordination constraints.

## Mechanisms

- Use Goal Oriented Action Planning for autonomous characters in a real-time action-game setting.
- Make planning practical enough for action gameplay rather than offline deliberation alone.
- Let autonomous planning characters support higher-level squad behavior.
- Separate the planner's benefits from the engineering constraints needed to make it usable in a live system.

## Evidence

- The source is an external conference-talk reference for GOAP vocabulary and practical real-time planning constraints.
- This repository has not reproduced F.E.A.R.'s planner, imported action schemas, executed game traces, benchmarked latency, or evaluated squad behavior.
- Use it as external comparison vocabulary for PlanForge and runtime handoff boundaries, not as local planner evidence.

## Failure Modes

- GOAP-style planning can be overread as general agent intelligence when it may be a domain-specific action-selection architecture.
- Practical game constraints can force caching, heuristics, or simplifications that hide evidence and residuals unless the runtime records them.
- Squad-level behavior can look coordinated without proving authority discipline, rollback readiness, or user-intent preservation.

## Book Chapters Supported

- `planning-as-a-control-layer` (Planning as a Control Layer)
- `planforge-dags-and-intelligence-arbitrage` (PlanForge DAGs and Intelligence Arbitrage)
- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores; includes folded MoECOT Runtime Crosswalk)

## Claims To Add Or Update

- Use this note to ground GOAP as practical planning vocabulary for real-time agent control.
- Do not claim PlanForge or MoECOT implements GOAP, reproduces F.E.A.R., or inherits its behavior.
- Keep support state at `argument` until planner traces, latency records, action-schema fixtures, or accepted evidence transitions exist.

## Open Questions

- Which PlanForge fixture should encode GOAP-style goals, actions, preconditions, effects, and planner budget?
- What runtime receipt should record when a real-time planner falls back because latency, authority, or context constraints block a plan?
- How should squad or multi-agent planning distinguish coordination from authority laundering?
