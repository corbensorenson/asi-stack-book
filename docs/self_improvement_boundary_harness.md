# Self-Improvement Boundary Harness

Last updated: 2026-06-28

The twenty-first Phase 5 harness checks synthetic self-improvement transition
fixtures under `experiments/self_improvement_boundaries/`.

## What It Checks

- Transition, field, and replacement references must use
  `self-improvement://`, `field://`, and `replacement://` identifiers.
- Records must name cheaper interventions tried before replacement.
- Protected invariants must be present and non-empty.
- Evaluator independence must name a separate, independent, external, or
  review boundary and cannot rely on candidate self-evaluation.
- Advancing transitions must not widen authority, grant ambient/root access,
  weaken protected invariants, or claim broad safety proof or support-state
  promotion.
- Proposals that weaken protected invariants must be rejected, quarantined, or
  rolled back.
- Rollback paths must name fallback, restore, rollback, return, or revert
  behavior.
- Canary and promoted outcomes must route through review or concrete approval
  and carry an observation, canary, monitor, watch, or regression window.
- Promoted outcomes require a concrete `approval://` record and a clean or
  passing monitor result.
- Rolled-back outcomes must name the monitor failure, breach, violation, or
  regression that caused rollback.

## Command

```bash
python3 scripts/validate_self_improvement_boundaries.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Self-improvement boundary harness passed: 3 valid fixture(s), 7 expected-invalid fixture(s).
```

The result record is
`experiments/self_improvement_boundaries/results/2026-06-28-local.md`.

## Boundary

This is a synthetic recursive self-improvement transition-record discipline
slice. It makes part of the Recursive Self-Improvement Boundaries chapter
executable at the record level: protected invariants, evaluator separation,
cheaper-intervention ordering, authority non-widening, governance review,
monitor windows, rollback paths, and no-promotion language have to line up.

It is not a deployed self-improvement result, runtime optimization result,
evaluator-integrity proof, authority-enforcement result, rollback-execution
trace, regression-quality result, source-interpretation review, reader-release
review, or model-behavior result. It does not promote Appendix C, validate
deployed AI behavior, prove recursive self-improvement safety, or approve
reader artifacts.
