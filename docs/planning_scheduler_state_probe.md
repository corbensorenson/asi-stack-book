# Planning Scheduler-State Probe

The Planning Scheduler-State Probe is a deterministic synthetic scheduler
fixture for the chapter `planning-as-a-control-layer`.

It validates two valid synthetic scheduler traces and seven expected-invalid controls.
The valid traces cover a ready dispatchable node, a context-blocked
node that preserves residuals, a failed cheap route rejected by its adequacy
predicate, a branch merge blocked by conflicting assumptions, and a local
repair/replanning trace that touches only the affected subgraph. The controls
reject blocked-node dispatch, ready-without-context dispatch, failed-adequacy
route selection, conflicting merge acceptance, replanning authority erasure,
accepted dependency cycles, and cost-quality ledgers that erase repair,
human-review, failed-attempt, or residual costs.

Run:

```bash
python3 scripts/validate_planning_scheduler_state_probe.py
```

The local result record is:

```text
experiments/planning_scheduler_state/results/2026-07-02-local.json
```

This probe does not prove decomposition quality, context-demand prediction,
selected-tier adequacy, route quality, scheduler optimality, deployed
scheduler behavior, runtime replanning behavior, or chapter support-state
promotion. In short: no support-state transition.
