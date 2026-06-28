# Authority Transition Harness

Last updated: 2026-06-28

The second Phase 5 harness checks synthetic authority-transition records under
`experiments/authority_transitions/`.

## What It Checks

- Allowed effects must remain within the caller ceiling and active authority
  ceiling.
- Allowed effects must carry a `receipt://` effect receipt and audit refs.
- Denied over-ceiling requests must not carry an effect receipt.
- Approval-class requests can escalate to review without executing.
- Permission classes must not collapse, so disclosure cannot be represented as
  read-level authority.
- A low-authority caller cannot borrow a higher-authority tool's raw capability
  as a confused-deputy shortcut.

## Command

```bash
python3 scripts/validate_authority_transitions.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Authority transition harness passed: 3 valid fixture(s), 3 expected-invalid fixture(s).
```

The result record is
`experiments/authority_transitions/results/2026-06-28-local.md`.

## Boundary

This is fixture-level gate validation for synthetic records. It improves the
book's executable evidence discipline because it catches basic authority
inflation paths, but it is not deployed authorization middleware and not a
runtime adapter test. It does not prove permission enforcement in a live agent,
tool wrapper, approval service, secret-handling system, or production runtime.
It does not promote Appendix C, prove source interpretation, prove proof
adequacy, reproduce a benchmark, or validate AI behavior.
