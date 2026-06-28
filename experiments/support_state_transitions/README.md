# Support-State Transition Harness

This experiment checks the book's support-state transition gate with synthetic
evidence-transition records.

It is intentionally not a test of any live-book chapter claim. The fixtures use
`claim://synthetic/...` identifiers, and their non-claims make clear that a
passing harness run does not promote Appendix C, prove source interpretation, or
validate AI behavior.

## Command

```bash
python3 scripts/validate_support_state_transitions.py
```

## Fixtures

- `fixtures/valid_argument_no_change.json` checks that a schema-valid no-change
  record can remain conservative while listing blockers.
- `fixtures/valid_scoped_source_promotion.json` checks the minimum synthetic
  shape of an accepted, scoped upward transition.
- `fixtures/invalid_unreviewed_promotion.json` checks that an upward movement is
  rejected without accepted review, passing verification, artifacts, evidence
  packets, and source mappings.
- `fixtures/invalid_failed_verification_promotion.json` checks that a failed
  verification result blocks upward movement even when review text is present.

## Environment

- Python 3.
- No network access.
- No external packages beyond the repository's dependency-free schema subset
  validator in `scripts/validate_protocol_examples.py`.

## Non-Claims

- This harness validates transition-gate semantics for synthetic records only.
- It does not promote any live chapter claim above `argument`.
- It does not prove semantic source adequacy, proof adequacy, runtime behavior,
  benchmark performance, or any AI safety property.
