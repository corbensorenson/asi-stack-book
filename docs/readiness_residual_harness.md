# Readiness/Residual Gate Harness

Last updated: 2026-06-28

The fifth Phase 5 harness checks synthetic cross-record consistency for costed
routes, readiness gates, and replacement transactions under
`experiments/readiness_residual_gates/`.

## What It Checks

- All nested route, gate, and replacement records validate against their
  existing public schemas.
- A field-implementation readiness target must match the replacement candidate
  and field identity.
- A selected route must be declared as a candidate route, stay inside the gate's
  authority scope, avoid blocked routes during promotion, and preserve fallback.
- Canary, qualify, and default decisions need ready evidence state, passing
  route verification, adequate route outcome, non-failing floor/regression
  evidence, and non-stale freshness.
- Route residual obligations and inherited residuals must remain covered by
  gate or replacement escrow before promotion.
- Quarantine must block the failed selected route, keep a fallback route
  allowed, and record a quarantined replacement decision.
- Default commit requires a committed replacement state, passing rollback
  dry-run receipt, passing monitor status, meaningful approval, and
  default-review support-state effect.
- Expired evidence must rerun or reject rather than entering canary, qualify, or
  default state.

## Command

```bash
python3 scripts/validate_readiness_residual_gates.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Readiness/residual gate harness passed: 4 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/readiness_residual_gates/results/2026-06-28-local.md`.

## Boundary

This is synthetic cross-record gate validation. It improves executable evidence
discipline because it catches promotion without regression evidence, lost
residual escrow, failed-route promotion, authority widening, stale-evidence
promotion, and commit without rollback readiness across existing protocol
schemas.

It is not a router, readiness engine, residual database, rollback executor,
runtime monitor, MoECOT replay path, routing benchmark, deployment result, or
proof of AI behavior. It does not promote Appendix C, prove source
interpretation, prove proof adequacy, reproduce a benchmark, or validate runtime
behavior.
