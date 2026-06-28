# Source Note: Theorem Proving in Lean 4

| Field | Value |
|---|---|
| Source ID | `ext_lean4_theorem_proving` |
| Source title | Theorem Proving in Lean 4 |
| Ingestion date | 2026-06-28 |
| Source version / URL | Official Lean text, https://lean-lang.org/theorem_proving_in_lean4/ |
| Citation label | Avigad et al., Theorem Proving in Lean 4 |
| Published / updated | not recorded / Lean 4.26.0 version noted |
| DOI | not recorded |
| Ingestion basis | Official Lean theorem-proving text inspected for proof-assistant and proof-envelope vocabulary; source not vendored into this repository and no external theorem imported. |

## Thesis

Theorem Proving in Lean 4 belongs in the proof-envelope, Circle, Spinoza, and research-agenda chapters as the external proof-assistant reference for dependent type theory, propositions-as-types, tactics, inductive definitions, structures, and proof terms. It grounds the book's Lean vocabulary without implying that the current ASI Stack Lean files prove more than their finite-record predicates state.

## Mechanisms

- Use dependent type theory to represent propositions, proofs, functions, records, inductive types, and computation.
- Support interactive proof development through tactic-mode and term-style proof construction.
- Separate theorem statements, definitions, structures, and axioms from the broader semantic adequacy of a model.
- Expose records and inductive types as natural carriers for finite protocol predicates.

## Evidence

- The source is an official Lean learning and reference text for theorem proving in Lean 4.
- This repository has not imported external Lean examples from the text or mechanically connected chapter claims to full semantic models.
- Use this source as proof-assistant vocabulary and method context, not as evidence that ASI Stack proofs are semantically adequate.

## Failure Modes

- A successful Lean build can verify a narrow formal statement while missing the intended safety property.
- Records and predicates can encode only the fields the author chose to model.
- Tactic success can be mistaken for system correctness when runtime behavior, source interpretation, and empirical premises are outside the theorem.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `circle-calculus-and-proof-carrying-ai-contracts` (Circle Calculus and Proof-Carrying AI Contracts)
- `spinoza-verification-and-proof-carrying-claims` (Spinoza Verification and Proof-Carrying Claims)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to ground Lean proof-assistant terminology and finite-record proof patterns.
- Do not claim that the book's Lean modules prove broad ASI safety, runtime behavior, or semantic adequacy.
- Keep support state at `argument` unless a specific theorem is tied to an accepted evidence transition with scoped semantics.

## Open Questions

- Which ASI Stack proof targets should graduate from finite-record predicates to richer inductive state machines?
- What theorem statements would be precise enough to affect a chapter support boundary?
- How should the book explain the difference between proof assistant success and evidence-state promotion?
