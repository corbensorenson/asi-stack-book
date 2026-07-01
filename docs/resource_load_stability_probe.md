# Resource Load-Stability Probe

Date: 2026-07-01

This record documents a local synthetic Resource Economics load-stability
probe. The scoped workload is `resource-burst-review-workload-v1`: a finite
burst of repository-review tasks with capacity cost, review minutes, risk
class, arrival tick, and value points. The probe compares an admit-arrivals
baseline, a protected capacity-smoothing route, and a cheaper invalid
review-erasure route.

## Command

```bash
python3 scripts/run_resource_load_stability_probe.py --write-result
python3 scripts/validate_resource_load_stability_probe.py
```

The first command writes the deterministic local result. The second command
recomputes the runner output, checks tracked artifact hashes, verifies the
finite Lean fixture bridge in `AsiStackProofs.ResourceEconomics`, checks route
selection fields, and enforces the non-claim boundary.

## Result Record

Result record:
`experiments/resource_load_stability_probe/results/2026-07-01-local.json`

| Field | Value |
|---|---|
| Probe ID | `resource-load-stability-probe-2026-07-01-local` |
| Workload ID | `resource-burst-review-workload-v1` |
| Task count | 10 |
| Horizon | 6 ticks |
| Capacity limit | 7 units per tick |
| Review capacity limit | 5 minutes per tick |
| Selected route | `route://selected-protected-capacity-smoothing` |
| Baseline route | `route://baseline-admit-arrivals` |
| Negative control | `route://negative-latency-only-review-erasure` |
| Selected-vs-baseline instability reduction | 100.0 percent |
| Negative control rejected | `true` |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |

## Route Records

| Route | Strategy | Load-instability units | Deferred task-ticks | Review minutes | Quality result | Selection result |
|---|---|---:|---:|---:|---|---|
| `route://baseline-admit-arrivals` | admit every arriving task immediately | 5 | 0 | 16 | pass | Eligible baseline; it preserves protected review but exposes burst overload. |
| `route://selected-protected-capacity-smoothing` | admit high-risk work first within capacity and residualize lower-risk deferrals | 0 | 7 | 16 | pass | Selected because it removes capacity/review overrun while keeping protected review and residualizing every deferral. |
| `route://negative-latency-only-review-erasure` | keep capacity low by erasing review and hiding deferrals | 0 | 0 visible; 7 hidden | 0 | fail | Rejected even though it uses less review, because it erases protected review on three high-risk tasks and hides deferrals. |

## Lean Fixture Bridge

`AsiStackProofs.ResourceEconomics` contains a finite
`LoadSmoothingWorkloadSummary` fixture for this result. The validator checks
that the result record names the bridge and that these theorem references are
present:

- `resource_load_smoothing_workload_fixture_valid`
- `resource_load_smoothing_workload_reduces_overrun`
- `resource_load_smoothing_workload_rejects_review_erasure`
- `resource_load_smoothing_workload_residualizes_deferrals`
- `resource_load_smoothing_workload_has_no_support_promotion`

The bridge is deliberately narrow. It links the public JSON result to finite
workload facts: 10 tasks, 3 routes, baseline total overrun of 5 units, selected
overrun of 0 units, 7 selected deferred task-ticks, 7 residualized selected
deferrals, and 3 negative-control protected-review violations.

## What It Adds

This probe is stronger than the earlier toy capacity-smoothing fixture because
it records a concrete finite workload, route outputs, selected-vs-baseline
metrics, a review-erasure negative control, and a Lean/Python fixture bridge.
It does not turn the result into a production scheduler claim. The selected
route wins only inside the local synthetic workload because it removes overload
without making lower-risk deferrals disappear.

The negative control preserves the hidden-cost boundary. A route that appears
cheaper because it reports zero review minutes is rejected when that saving
comes from erasing protected review or hiding deferred work.

## Residuals

- The workload is a deterministic local synthetic burst of repository-review
  tasks, not a production queue trace.
- The selected route reduces overload in the finite workload by deferring
  lower-risk work, but those deferrals are residual costs rather than free
  savings.
- The negative control shows that lower review minutes are invalid when
  protected high-risk review is erased or deferred work is hidden.

## Boundary

This is a local synthetic load-stability probe. It deepens the Resource
Economics lane by connecting finite workload records, route choice, overload
metrics, protected review, residualized deferrals, a negative control, a
finite Lean fixture bridge, and explicit non-claims. It does not replace
production scheduler logs, live workload-quality review, human-repair
measurement, physical-feasibility review, simulation benchmark, external
review, or the full book gate.

## Non-Claims

- This load-stability probe does not promote any chapter core claim above
  `argument`.
- This load-stability probe does not create a support-state transition.
- This load-stability probe does not prove TokenMana behavior, PlanForge
  behavior, deployed scheduler behavior, production queue behavior, real load
  stability, human productivity, model quality, economic outcomes, physical
  feasibility, simulator adequacy, or workload-quality improvement outside
  this local synthetic repository workload.
- The selected route is scoped to this finite burst-review workload only and
  does not replace production scheduler logs, live workload-quality review,
  human-repair measurement, external review, or the full book gate.
