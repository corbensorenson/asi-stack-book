# Stable Capability Fields Harness

Last updated: 2026-06-28

The nineteenth Phase 5 harness checks synthetic stable-capability-field
fixtures under `experiments/stable_capability_fields/`.

## What It Checks

- Stable field records must use `field://` identifiers.
- Authority ceilings must not grant ambient or unbounded authority.
- Evidence-mapped and qualified fields must preserve qualification predicates,
  evidence refs, and regression suites.
- Routed lifecycle states must carry readiness-gate refs and valid or residual
  route-validity state.
- Canary, shadow, and qualified routes must preserve default-route blockers.
- Default routes require valid route state and an active non-fixture lease.
- Evaluator policy and evaluator independence must preserve separate review
  rather than self-attestation by the candidate.
- Rollback plans and obligations must preserve rollback, fallback, retain, or
  restore duties.
- Non-claims must explicitly preserve runtime and support-state boundaries.

## Command

```bash
python3 scripts/validate_stable_capability_fields.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Stable capability fields harness passed: 3 valid fixture(s), 6 expected-invalid fixture(s).
```

The result record is
`experiments/stable_capability_fields/results/2026-06-28-local.md`.

## Boundary

This is a synthetic stable-capability-field record-discipline slice. It makes
part of the Stable Capability Fields chapter executable at the record level:
qualification predicates, evidence refs, readiness refs, authority ceilings,
route scopes, route permission effects, evaluator independence, review
triggers, rollback obligations, default-route blockers, and explicit
non-claim boundaries have to line up.

It is not a deployed route-validity result, runtime capability-identity result,
evaluator-integrity proof, authority-enforcement result, replacement-safety
result, rollback-execution trace, source-interpretation review,
reader-release review, or model-behavior result. It does not promote Appendix
C, validate deployed AI behavior, or approve reader artifacts.
