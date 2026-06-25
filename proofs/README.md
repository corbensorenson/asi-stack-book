# Proofs

This folder tracks proof plans and links to executable formalizations.

Proof target source of truth:

- `docs/book_outline.md` - human-readable chapter outline with stable `lean:*` proof tags.
- `proofs/proof_manifest.json` - generated machine-readable manifest. Regenerate with `python3 scripts/sync_proof_manifest.py`.
- `proofs/proof_triage.json` - generated/readiness-oriented classification of proof targets.
- `docs/proof_artifact_audit.md` - generated proof artifact traceability audit. Refresh with `python3 scripts/validate_proof_artifact_audit.py --write` and check with `python3 scripts/validate_proof_artifact_audit.py`.

Current executable proof workspace:

- `lean/` - Lean 4 project for small architecture invariants.

Initial proof targets:

- See `proofs/proof_manifest.json` for the current chapter-by-chapter target set.

Do not claim an architecture theorem is proven unless the corresponding proof checker command passes.

The artifact audit checks wiring, coverage, and limitation/non-claim surfacing. It does not prove that a finite-record predicate is semantically adequate for the chapter claim, and it does not prove broad ASI Stack behavior.
