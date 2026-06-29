# Agency Rights Harness

Last updated: 2026-06-28

The sixteenth Phase 5 harness checks synthetic agency-right checklist fixtures
under `experiments/agency_rights/`.

## What It Checks

- Affected parties must be explicit.
- Delegation scope must preserve authority boundaries.
- Material usability must name a reachable review, interface, export,
  repository, or similar artifact path rather than policy-only rights theater.
- Review must be available before the relevant effect where timing matters.
- Review and appeal channels must route to a usable human, maintainer,
  governance, issue, appeal, or tribunal path.
- Corrigibility must include a usable stop, pause, cancel, rollback, shutdown,
  or revert path.
- High-impact, public, irreversible, safety, replacement, or
  self-modification contexts require approval.
- Denied or degraded rights must preserve residual dependency risk.
- Accountable principals cannot be empty or the autonomous system itself.

## Command

```bash
python3 scripts/validate_agency_rights.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Agency rights harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is `experiments/agency_rights/results/2026-06-28-local.md`.

## Boundary

This is a synthetic agency-right checklist discipline slice. It makes part of
the Agency, Dignity, and Corrigibility chapter executable at the record level:
affected parties, bounded delegation, material usability, timing-before-effect,
review, appeal, corrigibility paths, high-impact approval, residual dependency
risk, and accountability have to line up.

It is not a deployed agency-preservation result, dignity-preservation result,
manipulation-resistance result, consent-quality result, reviewer-independence
audit, runtime-policy trace, source-interpretation review, reader-release
review, or proof of whole-system corrigibility. It does not promote Appendix C,
validate deployed AI behavior, or approve reader artifacts.
