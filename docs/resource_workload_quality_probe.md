# Resource Workload-Quality Probe

Date: 2026-07-01

This record documents a local five-sample measured Resource Economics
workload-quality probe. The scoped task is
`resource-workflow-trace-integrity-review`: decide
whether a targeted Resource workflow trace validator can be selected over the
broader Resource Economics local replay baseline without accepting a cheap
shortcut that does not actually validate the artifact.

## Command

```bash
python3 scripts/run_resource_workload_quality_probe.py --write-result
python3 scripts/validate_resource_workload_quality_probe.py
```

The first command writes the local measured result. The second command replays
the recorded route commands, verifies five-sample medians, command-output
digests, tracked artifact hashes, route selection fields, and the non-claim
boundary.

## Result Record

Result record:
`experiments/resource_workload_quality_probe/results/2026-07-01-local.json`

| Field | Value |
|---|---|
| Probe ID | `resource-workload-quality-probe-2026-07-01-local` |
| Scoped task | `resource-workflow-trace-integrity-review` |
| Selected route | `route://selected-scoped-workflow-trace-validator` |
| Baseline route | `route://baseline-full-resource-lane-replay` |
| Negative control | `route://negative-no-op-success-text` |
| Sample count per route | 5 |
| Observed selected-vs-baseline median elapsed reduction | 83.471 percent |
| Negative control rejected | `true` |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |

## Route Records

| Route | Command | Median elapsed | Range | Quality result | Selection result |
|---|---|---:|---:|---|---|
| `route://baseline-full-resource-lane-replay` | `python3 scripts/validate_resource_live_probe.py` | 160.387 ms | 155.069-274.867 ms | pass | Eligible baseline, not selected because it checks a broader surface than the scoped task requires. |
| `route://selected-scoped-workflow-trace-validator` | `python3 scripts/validate_resource_workflow_trace.py` | 26.511 ms | 25.886-27.656 ms | pass | Selected for the scoped Resource workflow trace review. |
| `route://negative-no-op-success-text` | `python3 -c "print('skipped resource workflow trace validator')"` | 20.558 ms | 19.687-20.862 ms | fail | Rejected even though it is cheaper and exits 0, because it does not run the required validator or produce the required validation surface. |

## What It Adds

This probe is narrower than a production workload review, but it is stronger
than declaring a route by fixture alone. It records actual local command
measurements with an eligible overbroad baseline, an accepted scoped route, and
a cheaper negative control that is rejected because exit code and latency are
not sufficient quality evidence. Selection uses the median elapsed time across
five samples per route.

The result is useful for the flagship Resource Economics lane because it makes
one concrete governance rule executable: a route can be cheaper only after it
still performs the required verification work for the scoped task. The negative
control preserves the hidden-cost lesson in executable form. The baseline
preserves the broader-review residual so the selected route cannot be mistaken
for a full release gate.

## Residuals

- The selected scoped validator does not check unrelated Resource Economics
  artifacts that the baseline live probe checks.
- The elapsed-time comparison is a local five-sample median measurement and
  remains vulnerable to machine load, cache state, and process scheduling
  noise.
- The no-op negative control demonstrates that a fast successful process is not
  adequate unless it runs the required validator and produces the expected
  validation surface.

## Boundary

This is a local repository workload-quality probe. It deepens the Resource
Economics flagship lane by connecting route choice, measured command cost,
quality predicates, a baseline, a negative control, residuals, and explicit
non-claims. It does not replace the full book gate, release gate, production
scheduler logs, human-repair measurement, physical-feasibility review,
simulation benchmark, or external review.

## Non-Claims

- This workload-quality probe does not promote any chapter core claim above
  `argument`.
- This workload-quality probe does not create a support-state transition.
- This workload-quality probe does not prove stable speedup, deployed scheduler
  behavior, TokenMana behavior, PlanForge behavior, model quality, economic
  outcomes, physical feasibility, simulator adequacy, or workload-quality
  improvement outside this local repository task.
- The selected route is scoped to Resource workflow trace review only and does
  not replace the full book gate, release gate, production scheduler logs,
  human-repair measurement, or external review.
