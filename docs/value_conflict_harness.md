# Value Conflict Harness

Last updated: 2026-06-28

The fourteenth Phase 5 harness checks synthetic value-conflict fixtures under
`experiments/value_conflicts/`.

## What It Checks

- Value-conflict records must name at least two value axes, stakeholders, and
  evidence requirements.
- High-stakes or irreversible conflicts must route through review, tribunal,
  human review, or appeal paths rather than silent auto-approval.
- Unresolved, bounded, escalated, deferred, or denied decisions must preserve
  residual uncertainty.
- Bounded, deferred, denied, or escalated decisions must narrow, block, deny,
  defer, limit, or escalate authority.
- Bounded decisions must preserve dissent payloads and real expiry or revisit
  conditions.
- Deprecated premises must block or mark authority as deprecated.

## Command

```bash
python3 scripts/validate_value_conflicts.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Value conflict harness passed: 3 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is `experiments/value_conflicts/results/2026-06-28-local.md`.

## Boundary

This is a synthetic value-conflict record-discipline slice. It makes part of
the Moral Uncertainty and Value Conflict chapter executable at the record
level: classification, stakeholder and evidence fields, review routing,
residual uncertainty, authority effects, dissent, and revisit conditions have
to line up.

It is not a moral-correctness result, value-classification quality result,
reviewer-independence audit, human-review quality result, tribunal-quality
result, runtime policy trace, source-interpretation review, reader-release
review, or proof of whole-system moral adequacy. It does not promote Appendix C,
validate deployed AI behavior, or approve reader artifacts.
