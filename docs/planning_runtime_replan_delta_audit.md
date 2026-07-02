# Planning Runtime-Replan Delta Audit

The Planning Runtime-Replan Delta Audit is a deterministic synthetic
runtime-replan fixture for the chapter `planning-as-a-control-layer`.

It validates two valid synthetic runtime-replan traces and nine expected-invalid controls.
The valid traces cover a local source-repair delta
that reruns only the affected subgraph and an authority-blocked replan that
records a residual without issuing a dispatch receipt. The controls reject
authority widening, stop-condition erasure, unaffected-node reruns without a
dependency impact record, missing residual ownership, missing context deltas,
missing verification deltas, blocked-authority dispatch receipts,
support-promotion overclaims, and missing non-claim boundaries.

Run:

```bash
python3 scripts/validate_planning_runtime_replan_delta.py
```

The local result record is:

```text
experiments/planning_runtime_replan_delta/results/2026-07-02-local.json
```

This audit does not execute a deployed planner, does not prove runtime
scheduler behavior, does not prove decomposition quality, does not prove route
quality or selected-tier adequacy, does not prove live feedback handling, and
does not promote the chapter support state. In short: no support-state transition.
