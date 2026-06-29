# Constitutional Alignment Harness

Last updated: 2026-06-28

The seventeenth Phase 5 harness checks synthetic constitutional-predicate
fixtures under `experiments/constitutional_alignment/`.

## What It Checks

- Protected constitutional predicate scope must be explicit.
- Operational or partial predicates must include executable-style tests and a
  usable review route.
- Speculative-lineage predicates must preserve uncertainty and state that they
  do not authorize action.
- Predicate conflicts must route, narrow, defer, block, deny, preserve
  residuals, or use review rather than defaulting to hidden optimizer choice.
- Self-modification rules must block, reject, deny, or route predicate
  weakening to governance review.
- Protected predicate migrations must preserve migration diff, record, review,
  or rollback semantics.
- Least-sufficient-power predicates cannot select maximum or unbounded power by
  default.
- Fixtures must preserve runtime, source-interpretation, and support-state
  non-claim boundaries.

## Command

```bash
python3 scripts/validate_constitutional_alignment.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Constitutional alignment harness passed: 3 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/constitutional_alignment/results/2026-06-28-local.md`.

## Boundary

This is a synthetic constitutional-predicate record-discipline slice. It makes
part of the Constitutional Alignment Substrate chapter executable at the record
level: predicate scope, operational tests, conflict routing, review routes,
self-modification rules, migration policies, least-sufficient-power behavior,
uncertainty, and non-claim boundaries have to line up.

It is not a deployed constitutional-alignment result, moral-correctness result,
runtime-policy trace, source-interpretation review, self-modification safety
result, predicate-translation adequacy review, review-quality audit,
reader-release review, or proof of whole-system alignment. It does not promote
Appendix C, validate deployed AI behavior, or approve reader artifacts.
