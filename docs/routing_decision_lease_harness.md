# Routing Decision Lease Harness

Last updated: 2026-07-01

Command:

```bash
python3 scripts/validate_routing_decision_lease.py
```

Result record: `experiments/routing_decision_lease/results/2026-07-01-local.md`

Result summary: Routing decision lease harness passed: 3 valid fixture(s), 7 expected-invalid fixture(s).

## What It Checks

The harness validates synthetic routing-head lease packets around the existing
specialist registry, routing decision, and MoECOT orchestration schemas. Each
scenario includes candidate specialists, an authority-rank context, a routing
decision, a MoECOT runtime-crosswalk packet, expected rejected candidates, and
non-claims.

The validator checks that selected routes use a registered candidate, cover the
required capability, satisfy readiness, stay under the authority ceiling, keep
the granted authority subset inside the selected specialist's registry
envelope, and choose a least-authority eligible specialist. It requires
overprivileged specialists to be rejected with non-selection evidence,
missing-readiness or blocked routes to preserve fallback/residual paths,
expired leases to stop selected routing, and source-only MoECOT packets to keep
replay gaps and promotion blockers visible.

## Boundary

This is synthetic record-gate evidence. Passing it proves only that the
fixtures obey the route-lease rules checked by the script. It does not prove
routing accuracy, learned-router quality, deployed authority enforcement,
least-cost optimality, specialist quality, MoECOT replay, benchmark
performance, runtime behavior, model quality, safety, or ASI capability. It
does not promote any Appendix C or chapter core support state.
