# Authority Transition Harness

This experiment checks synthetic authority-transition records for non-escalation,
permission separation, denial receipts, and review escalation.

It is intentionally not a test of deployed authorization middleware. The
fixtures use synthetic principals, local authority labels, and non-claims that
prevent the result from being treated as production security evidence.

## Command

```bash
python3 scripts/validate_authority_transitions.py
```

## Fixtures

- `fixtures/valid_allow_scoped_write.json` checks that an allowed write remains
  within the caller ceiling and carries an effect receipt.
- `fixtures/valid_deny_over_ceiling.json` checks that an over-ceiling execution
  request is denied without an effect receipt.
- `fixtures/valid_escalate_approval_required.json` checks that approval-class
  authority routes to review instead of executing.
- `fixtures/invalid_allow_over_ceiling.json` checks that a low-authority caller
  cannot borrow a higher-authority tool capability.
- `fixtures/invalid_missing_effect_receipt.json` checks that an allowed effect
  without an effect receipt is invalid.
- `fixtures/invalid_permission_class_collapse.json` checks that a disclosure
  action cannot be represented as a read-level target.

## Environment

- Python 3.
- No network access.
- No external packages beyond the repository's dependency-free schema subset
  validator in `scripts/validate_protocol_examples.py`.

## Non-Claims

- This harness validates synthetic authority-transition gate semantics only.
- It does not prove deployed permission enforcement, confused-deputy resistance,
  tool-wrapper security, secret handling, revocation propagation, runtime
  behavior, or any AI safety property.
- It does not promote any live chapter claim above `argument`.
