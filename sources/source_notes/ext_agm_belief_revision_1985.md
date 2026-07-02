# Source Note: On the Logic of Theory Change: Partial Meet Contraction and Revision Functions

| Field | Value |
|---|---|
| Source ID | `ext_agm_belief_revision_1985` |
| Source title | On the Logic of Theory Change: Partial Meet Contraction and Revision Functions |
| Ingestion date | 2026-07-01 |
| Source version / URL | PhilPapers metadata, https://philpapers.org/rec/ALCOTL-2 |
| Citation label | Alchourron, Gardenfors, and Makinson (1985), AGM belief revision |
| Published / updated | 1985 / 1985 |
| DOI | 10.2307/2274239 |
| Ingestion basis | PhilPapers bibliographic metadata and abstract inspected for the belief-revision literature queue; proofs, formal definitions, representation theorems, and full text are not imported into this repository. |

## Thesis

This source belongs in `claim-ledgers-and-belief-revision` as the canonical formal-epistemology comparator for rational theory change. It grounds the chapter's belief-revision language in a lineage that distinguishes contraction and revision instead of treating all evidence updates as generic confidence changes.

## Mechanisms

- Treat belief change as a formal operation over a theory rather than as a prose rewrite.
- Distinguish contraction, which removes support for a proposition, from revision, which incorporates a proposition.
- Analyze partial-meet contraction as a way of selecting among maximal subsets that avoid the proposition being removed.
- Connect belief-change operations to rationality postulates and representation results.

## Evidence

- The source is a journal article in the Journal of Symbolic Logic, 50(2):510-530, with DOI `10.2307/2274239`.
- This repository has not mechanized AGM postulates, imported the full proof text, or implemented partial-meet contraction.
- Use the source as external lineage for rational belief change, not as evidence that the ASI Stack implements AGM belief revision.

## Failure Modes

- Treating AGM lineage as if it solves natural-language claim extraction, contradiction detection, or semantic equivalence for generated prose.
- Collapsing formal theory change into informal confidence scoring.
- Importing rationality-postulate language without recording where the ASI claim ledger deliberately differs from AGM theory.

## Book Chapters Supported

- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)

## Claims To Add Or Update

- Use this note to position claim-ledger revision against formal contraction/revision theory.
- State that the claim ledger borrows the discipline of explicit belief-change operations while targeting publication support states, surface synchronization, and evidence histories for AI-generated artifacts.
- Keep the chapter support state at `argument` until local extraction, contradiction, semantic-equivalence, and revision-engine evidence exists.

## Open Questions

- Which ledger transitions correspond cleanly to contraction, revision, downgrade, split, merge, residualization, or retirement?
- Should any AGM postulate become a future Lean target, or would that over-formalize the current ledger before extraction and contradiction machinery exists?
- How should the book distinguish rationality postulates over formal theories from engineering gates over source-backed claims?
