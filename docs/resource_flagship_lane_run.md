# Resource Flagship Lane Run

This record documents the current one-command Resource Economics flagship lane
replay. It composes existing public-safe evidence artifacts rather than
creating a new chapter-core support transition.

Command:

```bash
python3 scripts/run_resource_flagship_lane.py --write-result
```

Tracked result:

`experiments/resource_flagship_lane/results/2026-07-01-local.json`

Validation command:

```bash
python3 scripts/validate_resource_flagship_lane.py
```

## Scope

- Lane: `resource-economics-and-token-budgets`
- Support-state effect: `none`
- Chapter-core support effect: `none`
- Evidence transition created by this run: `false`
- Commands replayed: 10
- Tracked artifact digests: 24

The run ties together the bounded costed-route slice, load-stability selector
transition, workflow trace,
budget-ledger fixtures, capacity-smoothing trace, local live replay probe,
workload-quality probe, load-stability probe, CI cost profile,
simulation-transfer boundary fixtures, and evidence-transition validation.

## Accepted Narrow Transitions

The accepted upward transitions remain scoped to non-core Resource claims, not
the Resource Economics chapter core claim.

| Field | Value |
|---|---|
| Costed-route claim | `resource-economics.costed_route_budget_slice` |
| Selected route | `route://bounded-transform-plus-verifier` |
| Baseline route | `route://frontier-manual-review` |
| Negative controls | `route://cheap-unverified-transform`; `route://hidden-residual-auto-merge` |
| Cost reduction vs baseline | 66.98 percent |
| New support state | `synthetic-test-backed` |
| Transition state | `review_accepted` |

| Field | Value |
|---|---|
| Load-stability claim | `resource-economics.finite_burst_load_smoothing_selector` |
| Selected route | `route://selected-protected-capacity-smoothing` |
| Baseline route | `route://baseline-admit-arrivals` |
| Negative control | `route://negative-latency-only-review-erasure` |
| Instability reduction vs baseline | 100.0 percent |
| New support state | `synthetic-test-backed` |
| Transition state | `review_accepted` |

## Chapter-Core Decision

The Resource Economics chapter core remains governed by
`evidence_transitions/v1_0_pilot/resource_economics_no_change.json`.

| Claim | Transition effect | Support-state effect |
|---|---|---|
| `resource-economics-and-token-budgets.core` | `no_change` | `argument_only` |

## Sublane No-Promotion Decisions

Each measured or replayed Resource sublane now has an explicit accepted
no-change decision. These records make the no-promotion boundary reviewable
without creating new upward transitions.

| Sublane | Claim ID | Decision record | Support-state effect |
|---|---|---|---|
| Workflow trace | `resource-economics.workflow_trace_dispatch_accounting` | `evidence_transitions/v1_x_measured/resource_workflow_trace_no_change.json` | `blocks_promotion` |
| Local replay probe | `resource-economics.local_replay_probe` | `evidence_transitions/v1_x_measured/resource_live_probe_no_change.json` | `blocks_promotion` |
| Workload-quality probe | `resource-economics.local_workload_quality_route_selection` | `evidence_transitions/v1_x_measured/resource_workload_quality_probe_no_change.json` | `blocks_promotion` |
| Broader load-stability probe | `resource-economics.synthetic_load_stability_route_selection` | `evidence_transitions/v1_x_measured/resource_load_stability_probe_no_change.json` | `blocks_promotion` |
| CI cost profile | `resource-economics.publication_pipeline_cost_profile` | `evidence_transitions/v1_x_measured/resource_ci_cost_profile_no_change.json` | `blocks_promotion` |

## Measured Workload-Quality Slice

The local workload-quality probe selected a scoped validator over a broader
baseline while rejecting a cheaper no-op route.

| Role | Route | Median elapsed | Decision |
|---|---|---:|---|
| Baseline | `route://baseline-full-resource-lane-replay` | 159.146 ms | quality pass |
| Selected | `route://selected-scoped-workflow-trace-validator` | 26.523 ms | quality pass |
| Negative control | `route://negative-no-op-success-text` | 20.311 ms | rejected |

Observed selected-vs-baseline elapsed reduction: 83.334 percent.

## Load-Stability Slice

The local synthetic load-stability probe selected protected capacity smoothing
over admitting arrivals while rejecting a review-erasure shortcut.

| Role | Route | Instability units | Residual / rejection |
|---|---|---:|---|
| Baseline | `route://baseline-admit-arrivals` | 5 | burst overload exposed |
| Selected | `route://selected-protected-capacity-smoothing` | 0 | 7 deferred task-ticks residualized |
| Negative control | `route://negative-latency-only-review-erasure` | 0 | rejected for 3 protected-review violations and 7 hidden deferred task-ticks |

Observed selected-vs-baseline instability reduction: 100.0 percent.

## Residuals

- The accepted upward transitions remain scoped to `resource-economics.costed_route_budget_slice` and `resource-economics.finite_burst_load_smoothing_selector`, not the chapter core claim.
- Workload-quality timing is a local repository-task measurement and remains machine-load sensitive.
- Load-stability evidence is a finite synthetic burst-review workload with residualized deferrals, not a production queue trace.
- CI cost evidence is publication-pipeline metadata, not a scheduler or economic-result measurement.
- Simulation-transfer evidence is record discipline over declared contracts, not simulator adequacy or physical-feasibility validation.

## Non-Claims

- This run does not promote the Resource Economics chapter core claim above `argument`.
- This run does not create a new support-state transition.
- This run does not prove deployed scheduler behavior, production queue behavior, TokenMana behavior, PlanForge behavior, KV-cache behavior, simulator adequacy, model quality, benchmark performance, safety outcomes, human productivity, or economic outcomes.
- This run is a local repository replay over tracked public-safe artifacts, not external review, live workload review, production scheduler logs, or artifact approval.
