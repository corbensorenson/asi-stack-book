# Context Admission/Adequacy Harness

Last updated: 2026-06-28

The fourth Phase 5 harness checks synthetic cross-record consistency for context
ABI records, context packets, semantic page certificates, context transactions,
and context adequacy records under `experiments/context_admission_adequacy/`.

## What It Checks

- All nested context records validate against their existing public schemas.
- Context packets must match the ABI task and materialization reference.
- Adequacy semantic units must have matching semantic page certificates and
  packet handles.
- Certificates must preserve ABI source refs, stay within the ABI authority
  ceiling, name transaction refs, and expose summary/loss omissions.
- Transactions must reference the ABI request, share the ABI snapshot, and
  block materialization when deletion closure remains open.
- Admitted context can still be inadequate for a target claim and must preserve
  escalation and promotion blockers for high-risk claims.
- Conflicts, stale/revoked certificates, propagated taint, open deletion
  obligations, and weak verification modes cannot become evidence-ready support.

## Command

```bash
python3 scripts/validate_context_admission_adequacy.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Context admission/adequacy harness passed: 3 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/context_admission_adequacy/results/2026-06-28-local.md`.

## Boundary

This is synthetic cross-record gate validation. It improves executable evidence
discipline because it catches admission/adequacy collapse, conflict promotion,
stale certificate reuse, mode confusion, and open deletion materialization
across existing context schemas.

It is not a VCM resolver, context compiler, transactional memory-store test,
summary-fidelity result, contradiction-rate benchmark, distractor-resistance
result, model-facing context run, or proof of AI behavior. It does not promote
Appendix C, prove source interpretation, prove proof adequacy, reproduce a
benchmark, or validate runtime behavior.
