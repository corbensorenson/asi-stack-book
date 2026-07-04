# Readiness Lifecycle Probe

Last updated: 2026-07-02

The readiness lifecycle probe is a deterministic synthetic replay for the
finite lifecycle relation in `AsiStackProofs.ReadinessGates`. It complements
the older readiness/residual gate harness by checking the state-transition
surface directly: candidate, shadow, canary, default-ready, quarantined,
superseded, and retired.

## Command

```bash
python3 scripts/validate_readiness_lifecycle_probe.py
```

## Current Local Result

The result record is
`experiments/readiness_lifecycle_probe/results/2026-07-02-local.json`.

The probe covers six valid synthetic readiness lifecycle transitions:

- candidate to shadow with fresh gate evidence, residual escrow, fallback, and
  expiry records;
- shadow to canary while carrying residual escrow;
- qualified to default-ready with regression floor, authority scope, and
  ordinary-route permission preserved;
- canary to quarantined with ordinary routing blocked, diagnostic routing
  allowed, and a fallback path present;
- qualified to superseded with residual escrow and a supersession record;
- superseded to retired with residual escrow and a retirement receipt.

It also covers twelve expected-invalid controls: non-forward jump, missing fresh
gate evidence, missing residual escrow, default without regression floor,
default without authority scope, quarantine with ordinary routing, quarantine
without diagnostic fallback, supersession without a record, retirement without a
receipt, transition from retired state, missing non-claim boundary, and support
state promotion overclaim.

## Lean Bridge

The bridge proof tag is
`lean:readiness.gates.lifecycle_probe_bridge` in
`AsiStackProofs.ReadinessGates`. The Lean side checks the finite lifecycle
constraint family; the Python side replays a public-safe fixture summary with
the same boundary names. This is a bridge between modeled transition semantics
and executable fixture accountability, not a proof of deployed readiness
behavior.

## Boundary

This is no support-state transition. The accepted no-promotion decision
`evidence_transitions/v1_x_measured/readiness_lifecycle_probe_no_change.json`
records the fixture as a blocking decision, not as upward support movement. It
does not execute a deployed readiness engine, prove residual-ledger storage,
prove live quarantine routing, prove benchmark quality, prove MoECOT replay, or
promote the chapter support state.
