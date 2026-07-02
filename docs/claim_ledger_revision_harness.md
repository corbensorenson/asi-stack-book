# Claim Ledger Revision Harness

Last updated: 2026-07-02

The eleventh Phase 5 harness checks synthetic claim-ledger and belief-revision
fixtures under `experiments/claim_ledger_revision/`.

## What It Checks

- A claim revision record preserves claim identity, prior evidence, evidence
  refs, revision history, affected surfaces, review routes, residuals, and
  non-claim boundaries.
- Upward support-state movement is rejected unless an accepted evidence
  transition is explicitly referenced.
- Contradicted claims cannot be promoted in the same revision.
- Contradictions must trigger quarantine, downgrade, split, residualization,
  escalation, or deprecation rather than silent no-change treatment.
- State-changing revisions must name affected book or release surfaces so
  dependent prose, appendices, reader artifacts, or release records can be
  reconciled.
- Semantic variants can merge only when their surface refs are synchronized,
  their scope remains unchanged, and their support-state effect is `none`.
- Contested or unsupported assumption contexts must split, downgrade,
  residualize, escalate, or quarantine instead of being treated as ordinary
  no-change revisions.
- Fixtures must preserve explicit support-state non-promotion and deny source
  interpretation, runtime, verifier-quality, semantic-equivalence, and
  assumption-context completeness claims.

## Command

```bash
python3 scripts/validate_claim_ledger_revision.py
```

## Current Local Result

The 2026-07-02 local run passed:

```text
Claim ledger revision harness passed: 5 valid fixture(s), 7 expected-invalid fixture(s).
```

The result record is
`experiments/claim_ledger_revision/results/2026-07-02-local.md`.

## Boundary

This is a synthetic claim-ledger record-discipline slice. It turns part of the
Claim Ledgers and Belief Revision chapter into executable checks for
contradiction routing, semantic-variant merge boundaries, assumption-context
dependency preservation, revision-history preservation, support-state promotion
blocking, surface propagation, residuals, and non-claim language.

It is not a claim extractor, verifier, belief engine, source-interpretation
review, semantic-equivalence checker, assumption-context completeness checker,
runtime trace, reader-release review, or proof of whole-system epistemic
correctness. It does not promote Appendix C, prove source interpretation, prove
proof adequacy, validate deployed AI behavior, or approve reader artifacts.
