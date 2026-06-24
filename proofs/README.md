# Proofs

This folder tracks proof plans and links to executable formalizations.

Proof target source of truth:

- `docs/book_outline.md` - human-readable chapter outline with stable `lean:*` proof tags.
- `proofs/proof_manifest.json` - generated machine-readable manifest. Regenerate with `python3 scripts/sync_proof_manifest.py`.

Current executable proof workspace:

- `lean/` - Lean 4 project for small architecture invariants.

Initial proof targets:

- See `proofs/proof_manifest.json` for the current chapter-by-chapter target set.

Do not claim an architecture theorem is proven unless the corresponding proof checker command passes.
