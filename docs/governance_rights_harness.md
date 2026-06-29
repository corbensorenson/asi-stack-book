# Governance Rights Harness

Last updated: 2026-06-28

The fifteenth Phase 5 harness checks synthetic governance-right fixtures under
`experiments/governance_rights/`.

## What It Checks

- Granted or preserved audit rights must preserve available material and receipt
  refs.
- Denied, redacted, or partially granted rights must preserve a reason and a
  usable appeal or review path.
- Exit and fork rights must expose materially usable access paths such as
  exports, repositories, snapshots, portable bundles, or source snapshots.
- Exit and fork rights must preserve rule and obligation text plus a real
  expiry or revisit condition.
- Fork rights must retain safety constraints and available material.
- Challenged-party independence must name an independent or durable record path
  rather than relying on self-attestation by the challenged party.
- Fixtures must deny institutional, runtime, legal, and support-state claims.

## Command

```bash
python3 scripts/validate_governance_rights.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Governance rights harness passed: 3 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is `experiments/governance_rights/results/2026-06-28-local.md`.

## Boundary

This is a synthetic governance-right record-discipline slice. It makes part of
the Governance Rights: Fork, Exit, and Audit chapter executable at the record
level: audit receipts, material availability, redaction reasons, appeal paths,
usable exit/fork access, safety constraints, preservation obligations, and
durable record paths have to line up.

It is not an institutional-governance result, legal-rights result, runtime
right-enforcement trace, deployed exit/fork usability result, reviewer-
independence audit, source-interpretation review, reader-release review, or
proof of whole-system contestability. It does not promote Appendix C, validate
deployed AI behavior, or approve reader artifacts.
