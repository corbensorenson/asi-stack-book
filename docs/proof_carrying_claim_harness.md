# Proof-Carrying Claim Harness

Last updated: 2026-06-28

The twelfth Phase 5 harness checks synthetic proof-carrying-claim fixtures under
`experiments/proof_carrying_claims/`.

## What It Checks

- Passed verifier results must preserve verifier artifact references and a
  positive artifact-validity state.
- Formal tiers must be backed by formal proof artifacts, citation tiers by
  citation or tribunal dossiers, and procedure tiers by procedure logs or
  schema fixtures.
- A narrow pass can become eligible for bounded evidence review only when the
  scope, limitations, consumer requirements, and non-claim boundaries are
  explicit.
- Failed, timed-out, or mismatched verifier results must preserve failed-attempt
  refs and route to no-change, downgrade, block, or escalation rather than
  promotion.
- Formalization mismatches must remain non-promotional and route to proof
  adequacy, tribunal, or claim-ledger review.
- Fixtures must deny semantic-equivalence, verifier-quality, runtime, and
  support-state-promotion claims.

## Command

```bash
python3 scripts/validate_proof_carrying_claims.py
```

## Current Local Result

The 2026-06-28 local run passed:

```text
Proof-carrying claim harness passed: 3 valid fixture(s), 5 expected-invalid fixture(s).
```

The result record is
`experiments/proof_carrying_claims/results/2026-06-28-local.md`.

## Boundary

This is a synthetic proof-carrying record-discipline slice. It makes part of
the Spinoza Verification and Proof-Carrying Claims chapter executable at the
record level: verifier artifacts, requested tiers, interpretation mappings,
scope boundaries, mismatch routes, failed attempts, and non-promotional
outcomes have to line up.

It is not an open-domain verifier, proof generator, citation validator,
semantic-equivalence checker, source-interpretation review, theorem-validity
result, runtime trace, reader-release review, or proof of whole-system
epistemic correctness. It does not promote Appendix C, prove verifier quality,
prove citation accuracy, validate deployed AI behavior, or approve reader
artifacts.
