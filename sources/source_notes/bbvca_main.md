# Source Note: Big Bang Volumetric Compression Architecture

| Field | Value |
|---|---|
| Source ID | `bbvca_main` |
| Source title | Big Bang Volumetric Compression Architecture |
| Ingestion date | 2026-06-24 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1tlgJismt6JaYv_jaf2XbwCX7WEqj9FJ0WvEtbHYS_-E |
| Ingestion basis | Local raw cache inspected at `sources/raw/google_docs/bbvca_main.txt`; raw text is not published. |

## Thesis

BBVCA main introduces compression as hierarchical causal reconstruction from compact generator states, deterministic laws, and bounded side information. It is an earlier research architecture that motivates BBVCA v9's more disciplined generate-verify-repair formulation.

## Mechanisms

- Map source artifacts into a bottom volumetric field.
- Search for compact upper generator voxels and deterministic expansion rules.
- Decode by replaying generator states and repair information.
- Use multiscale verification to prevent uncontrolled drift.
- Support lossless and near-lossless modes under explicit contracts.
- Identify risks such as side-information explosion, solver cost, mapping sensitivity, rule fragility, verification overhead, and domain mismatch.

## Evidence

- The source is a concept whitepaper and research architecture draft.
- It is useful for historical development and the volumetric intuition behind BBVCA.
- BBVCA v9 should be preferred for final claims about rate discipline, proxy accounting, and exact repair.
- No local codec implementation or benchmark exists in this repository.

## Failure Modes

- Assuming a compact apex seed can reconstruct arbitrary data without side information.
- Letting side information erase compression gains.
- Using a 3D mapping where the data domain does not justify it.
- Underpaying verification and repair costs.
- Treating philosophical analogy as compression proof.

## Book Chapters Supported

- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)

## Claims To Add Or Update

- Use BBVCA main as lineage for the compression chapter, but use BBVCA v9 for the strongest bounded claims.
- Mention earlier risks to show why v9's reconstruction contract and rate discipline matter.

## Open Questions

- Should the book compare BBVCA main and v9 to show maturation of the idea?
- Which risks can become validation checks for a toy codec?
