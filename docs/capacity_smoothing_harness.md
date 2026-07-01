# Capacity Smoothing Toy Harness

Last updated: 2026-07-01

The tenth Phase 5 harness checks deterministic toy capacity traces under
`experiments/capacity_smoothing/`.

## What It Checks

- Capacity arithmetic is internally consistent across a trace.
- Admitted work cannot exceed regenerated bounded capacity.
- Low-risk work cannot consume capacity while high-risk work is blocked.
- Deferral and scope reduction remain explicit decisions.
- Reviewer-capacity traces preserve review-capacity arithmetic, protected
  review overhead, displaced-review-cost residualization, and low-risk review
  deferral while protected review is blocked.
- The Resource Economics Lean bridge names finite capacity-smoothing fixture
  and reviewer-capacity negative-case theorems.
- Fixture records preserve support-state non-promotion and deny load,
  scheduler, TokenMana, runtime, and economic-result claims.

## Command

```bash
python3 scripts/validate_capacity_smoothing.py
```

## Current Local Result

The 2026-07-01 local run passed:

```text
Capacity smoothing toy harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is `experiments/capacity_smoothing/results/2026-07-01-local.md`.

## Boundary

This is a deterministic toy-trace check for Resource Economics. It gives the
book an executable sanity check for bounded regeneration, priority deferral,
scope reduction, reviewer-capacity accounting, protected-overhead preservation,
displaced-review residualization, and non-claim discipline.

It is not TokenMana, a budget scheduler, a review-queue optimizer, a load test,
a serving benchmark, a welfare study, a human productivity result, an economic
outcome, a runtime enforcement result, a reviewer-capacity optimization result,
a protected-overhead adequacy result, a displaced-cost measurement, or a
deployed AI behavior result. It does not promote Appendix C, prove source
interpretation, prove proof adequacy, or validate production capacity behavior.
