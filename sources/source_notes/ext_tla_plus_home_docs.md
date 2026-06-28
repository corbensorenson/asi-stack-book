# Source Note: My TLA+ Home Page

| Field | Value |
|---|---|
| Source ID | `ext_tla_plus_home_docs` |
| Source title | My TLA+ Home Page |
| Ingestion date | 2026-06-28 |
| Source version / URL | Leslie Lamport TLA+ home page, https://lamport.azurewebsites.net/tla/tla.html |
| Citation label | Lamport, My TLA+ Home Page |
| Published / updated | not recorded / 2025-05-14 page modification noted |
| DOI | none recorded |
| Ingestion basis | Primary TLA+ home page inspected for the formal-methods literature queue; no TLA+ spec or model-checking run imported. |

## Thesis

This source belongs in the proof-envelope and planning chapters as an external reference for formal specification of systems, especially concurrent and distributed systems. It reinforces the book's distinction between precise design models, implementation, and runtime evidence.

## Mechanisms

- Use a high-level mathematical language to model system behavior.
- Apply tools to find design errors before code becomes the evidence surface.
- Separate specification, model checking, proofs, implementation, and deployment.
- Treat formal specifications as design artifacts with scoped authority.

## Evidence

- The source contributes official TLA+ documentation context.
- This repository has not written, checked, or imported a TLA+ spec.
- Use it as formal-methods comparison material, not as proof that the ASI Stack has complete specifications.

## Failure Modes

- A model can omit the behavior that matters.
- Passing a model checker is not proof of implementation correctness.
- Formal-methods branding can create proof theater if the consumer boundary is unclear.

## Book Chapters Supported

- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `planning-as-a-control-layer` (Planning as a Control Layer)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Use this note to compare Lean-oriented proof-envelope design with TLA+ style system specification.
- Do not claim a TLA+ model exists in this repository.
- Keep support state at `argument` until formal artifacts and validation commands are recorded.

## Open Questions

- Which ASI Stack lifecycle state machine is best suited to a future TLA+ spec?
- How should TLA+ model-checking results differ from Lean proof results in Appendix E?
- What release record should capture formal-model scope and limitations?
