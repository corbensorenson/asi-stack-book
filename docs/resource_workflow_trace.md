# Resource Workflow Trace

Date: 2026-07-01

This record documents a deterministic public-safe Resource Economics workflow
trace. It deepens the flagship evidence lane by checking a multi-step workload
with explicit route costs, scheduler order, protected high-risk review,
quality predicates, displaced-cost residuals, and bounded simulation-transfer
language.

It is intentionally narrower than a benchmark. It does not run a deployed
scheduler, does not measure model quality, does not reproduce TokenMana or
PlanForge, does not prove physical feasibility, and does not promote any
chapter core claim.

## Command

```bash
python3 scripts/validate_resource_workflow_trace.py
```

The command recomputes the selected-route totals from tracked fixture fields,
checks 1 valid fixture and 4 expected-invalid controls, and verifies this
summary plus the tracked result record.

## Public Trace

Trace ID: `resource-workflow-trace-2026-07-01`

Input fixture:
`experiments/resource_workflow_trace/fixtures/valid_multi_step_public_trace.json`

Result record:
`experiments/resource_workflow_trace/results/2026-07-01-local.json`

Observed deterministic fixture summary:

| Field | Value |
|---|---:|
| Steps | 3 |
| Selected-route tokens | 12,200 |
| Selected-route review minutes | 26 |
| Selected-route verification minutes | 21 |
| Selected-route cost | 119.7 cost units |
| Transfer decision | `scenario_only` |
| Support-state effect | `none` |

## Selected Routes

| Step | Selected route | Reason |
|---|---|---|
| `step://high-risk-release-gate` | `route://human-verifier-release-gate` | The lower-cost automatic route omits protected human review, audit, and rollback overhead. |
| `step://source-crosswalk-refresh` | `route://bounded-crosswalk-refresh` | The latency-only route fails quality and leaves displaced reader repair unowned; the manual baseline is eligible but more costly. |
| `step://low-risk-index-cleanup` | `route://local-index-cleanup` | The local route passes the fixture quality predicate without consuming scarce human review capacity. |

## Lean Fixture Bridge

The validator also checks that the finite workflow summary fixture in
`AsiStackProofs.ResourceEconomics` matches the public result record for step
count, selected-route count, total cost tenths, expected-invalid control count,
high-risk-first ordering, displaced-cost residualization,
physical-feasibility-overclaim rejection, latency-only selection rejection,
support-state non-promotion, and non-claim boundaries.

This bridge proves fixture alignment only. It does not prove deployed scheduler
behavior, route-search completeness, physical feasibility, model quality,
economic outcomes, simulator adequacy, or a chapter-core support-state
transition.

## Negative Controls

- `invalid_latency_only_selector.json` rejects a selected route whose low
  latency hides failed quality and partial verification.
- `invalid_displaced_cost_erased.json` rejects a dispatch that records future
  debugging and reviewer burden but erases residual ownership.
- `invalid_physical_feasibility_overclaim.json` rejects a toy accounting trace
  that tries to become physical-feasibility or support-state evidence.
- `invalid_scheduler_starves_high_risk.json` rejects low-risk work scheduled
  ahead of protected high-risk review when the trace requires high-risk-first
  ordering.

## Non-Claims

- This record does not promote any chapter core claim above `argument`.
- This record does not prove deployed scheduler behavior, runtime behavior,
  load stability, KV-cache behavior, economic outcomes, physical feasibility,
  simulator adequacy, model quality, or TokenMana/PlanForge behavior.
- This record does not create a support-state transition.
- This record does not replace a larger public trace with live workload
  quality review, displaced-cost accounting, scheduler logs, physical review,
  external review, or production measurements.
