# Claim Ledger Completeness Audit

The Claim Ledger Completeness Audit checks the real Appendix C claim/evidence
matrix against `book_structure.json`.

It verifies 44 manifest chapter core claims and 44 core claim rows in Appendix
C. Each row must have the expected core claim ID, chapter ID, claim text, claim
label, current support state, assigned sources, current evidence text,
claim-source mapping text, open gap, and reviewer-facing promotion path. The
audit also runs seven expected-invalid mutation controls for missing rows,
duplicate rows, unknown rows, claim-label mismatch, support-state mismatch,
missing open gaps, and missing promotion paths.

Run:

```bash
python3 scripts/validate_claim_ledger_completeness_audit.py
```

The local result record is:

```text
experiments/claim_ledger_completeness/results/2026-07-02-local.json
```

This audit does not prove claim truth, prove source interpretation, prove
promotion readiness, create a support-state transition, promote chapter core
claims, or prove external review quality. In short: no support-state
transition.
