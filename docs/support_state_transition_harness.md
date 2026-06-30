# Support-State Transition Harness

Last updated: 2026-06-30

The first Phase 5 harness checks the evidence-transition gate with synthetic
records under `experiments/support_state_transitions/`.

## What It Checks

- No-change records can stay conservative while listing blockers.
- Upward movement must match the declared support-state change.
- Upward movement requires accepted review, `review_accepted` validity, passing
  verification, no acceptance blockers, artifact refs, evidence packet refs,
  source mapping refs, reviewer refs, and `eligible_for_bounded_evidence_review`.
- Downward movement requires accepted review, negative evidence refs, downgrade
  triggers, reviewer refs, and `blocks_promotion`.
- Terminal `deprecated` and `refuted` movement requires accepted review,
  negative evidence refs, reviewer refs, and `blocks_promotion`.
- Failed verification blocks upward movement.
- Unreviewed or incomplete promotion attempts remain invalid even when the JSON
  shape matches the schema.
- Reasonless demotion and unsupported refutation attempts remain invalid even
  when the JSON shape matches the schema.

## Command

```bash
python3 scripts/validate_support_state_transitions.py
```

## Current Local Result

The 2026-06-30 local run passed:

```text
Support-state transition harness passed: 4 valid fixture(s), 4 expected-invalid fixture(s).
```

The result record is
`experiments/support_state_transitions/results/2026-06-30-local.md`.

## Boundary

This is fixture-level gate validation. It is useful because it prevents obvious
support-state inflation paths, but it is not a claim-specific evidence review.
It does not promote Appendix C, prove source interpretation, prove proof
adequacy, reproduce a benchmark, or validate runtime behavior.
