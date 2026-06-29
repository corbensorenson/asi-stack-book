# Capability Replacement Harness

Last updated: 2026-06-28

The twentieth Phase 5 harness checks synthetic replacement-transaction
fixtures under `experiments/capability_replacement/`.

## What It Checks

- Replacement transactions must use `replacement://`, `field://`, and
  `impl://` identifiers for the transaction, field, prior implementation, and
  candidate implementation.
- Identity preservation must state that field identity remains the same or
  unchanged.
- Precheck results, qualification evidence, regression results, residual
  escrow, source refs, and non-claims must be non-empty.
- Authority checks must preserve a non-widening boundary and must not authorize
  ambient or unrestricted authority.
- Evaluator independence must name a separate review boundary rather than
  candidate self-attestation.
- Rollback plans must name restore, rollback, revert, or fallback behavior.
- Rollback receipts must point back to the prior implementation and include
  trigger conditions for canary or commit decisions.
- Commit decisions require a passing rollback dry run, a concrete
  `approval://` record, passing monitor status, and no unresolved promotion
  blockers.
- Failed regression evidence blocks canary, commit, and retire decisions.
- Non-claims must preserve runtime and support-state boundaries.

## Command

```bash
python3 scripts/validate_capability_replacement.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Capability replacement harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is
`experiments/capability_replacement/results/2026-06-28-local.md`.

## Boundary

This is a synthetic capability-replacement record-discipline slice. It makes
part of the Capability Replacement and Rollback chapter executable at the
transaction-record level: field identity, prior and candidate implementations,
qualification evidence, regression results, authority checks, evaluator
separation, residual escrow, rollback receipts, approvals, monitor state,
promotion blockers, and explicit non-claims have to line up.

It is not a deployed replacement-behavior result, runtime route-quality result,
evaluator-integrity proof, authority-enforcement result, rollback-execution
trace, regression-quality result, source-interpretation review,
reader-release review, or model-behavior result. It does not promote Appendix
C, validate deployed AI behavior, or approve reader artifacts.
