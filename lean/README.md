# Lean Proof Workspace

Minimal Lean 4 project for formalizing small ASI Stack invariants.

Proof targets come from `docs/book_outline.md` and are mirrored into `proofs/proof_manifest.json`.

Run:

```bash
cd lean
lake build
```

The initial module is a toolchain smoke test for support-state ordering. It is not a proof of the book's architecture. Use the proof manifest to decide which modules and theorems to implement next.
