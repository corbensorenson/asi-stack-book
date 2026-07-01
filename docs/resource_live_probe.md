# Resource Live Probe

Date: 2026-07-01

This record documents a local replay probe for the Resource Economics lane. It
runs five local Resource Economics validators, records command exit codes,
elapsed milliseconds, output digests, and tracked artifact hashes, then checks
that the result remains a repository replay artifact rather than a claim
promotion.

This is not a deployed scheduler result, live TokenMana or PlanForge result,
model-quality measurement, production cost-quality result, physical-feasibility
review, simulator-adequacy result, human-repair burden measurement, or external
review. It is a reproducibility and accounting increment for the flagship
evidence lane.

## Command

```bash
python3 scripts/run_resource_live_probe.py --write-result
python3 scripts/validate_resource_live_probe.py
```

The first command writes the local measured result record. The second command
replays the same validator set, checks command-output digests, verifies tracked
artifact hashes, and enforces the non-claim boundary.

## Result Record

Result record:
`experiments/resource_live_probe/results/2026-07-01-local.json`

| Field | Value |
|---|---|
| Probe ID | `resource-live-probe-2026-07-01-local` |
| Replay commands | 5 |
| Tracked artifacts | 15 |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |

## Replay Surface

The probe runs and records these local commands:

| Command | Evidence surface |
|---|---|
| `python3 scripts/validate_costed_route_resource_slice.py` | Non-core synthetic-test-backed costed-route/resource-budget slice. |
| `python3 scripts/validate_resource_workflow_trace.py` | Deterministic multi-step Resource Economics workflow trace. |
| `python3 scripts/validate_resource_budget_ledgers.py` | Resource Budget Record fixture decisions. |
| `python3 scripts/validate_capacity_smoothing.py` | Bounded-capacity toy trace fixtures. |
| `python3 scripts/validate_simulation_transfer_boundaries.py` | Simulation-transfer boundary fixtures folded into Resource Economics. |

## Boundary

The probe proves only that the current repository can replay the named local
validators and that the tracked Resource Economics evidence artifacts match the
recorded hashes at the time of validation. It does not replace the larger
blockers for this lane: live or externally reviewable workload quality review,
production scheduler logs, measured displaced-cost accounting, physical-
feasibility review, and measured simulation outputs.

## Non-Claims

- This local replay probe does not promote any chapter core claim above
  `argument`.
- This local replay probe does not create a support-state transition.
- This local replay probe does not prove deployed scheduler behavior, runtime
  budget enforcement, TokenMana behavior, PlanForge behavior, model quality,
  economic outcomes, physical feasibility, simulator adequacy, or open-world
  transfer.
- This local replay probe records repository command execution only; it is not
  a live workload quality review, production scheduler log, human-repair
  measurement, or external physical-feasibility review.
