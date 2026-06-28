# Capacity Smoothing Toy Harness

Last updated: 2026-06-28

The tenth Phase 5 harness checks deterministic toy capacity traces under
`experiments/capacity_smoothing/`.

## What It Checks

- Capacity arithmetic is internally consistent across a trace.
- Admitted work cannot exceed regenerated bounded capacity.
- Low-risk work cannot consume capacity while high-risk work is blocked.
- Deferral and scope reduction remain explicit decisions.
- Fixture records preserve support-state non-promotion and deny load,
  scheduler, TokenMana, runtime, and economic-result claims.

## Command

```bash
python3 scripts/validate_capacity_smoothing.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Capacity smoothing toy harness passed: 2 valid fixture(s), 3 expected-invalid fixture(s).
```

The result record is `experiments/capacity_smoothing/results/2026-06-28-local.md`.

## Boundary

This is a deterministic toy-trace check for Resource Economics. It gives the
book an executable sanity check for bounded regeneration, priority deferral,
scope reduction, and non-claim discipline.

It is not TokenMana, a budget scheduler, a review-queue optimizer, a load test,
a serving benchmark, a welfare study, a human productivity result, an economic
outcome, a runtime enforcement result, or a deployed AI behavior result. It
does not promote Appendix C, prove source interpretation, prove proof adequacy,
or validate production capacity behavior.
