# Source Note: The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS

| Field | Value |
|---|---|
| Source ID | `ext_black_box_simplex_2021` |
| Source title | The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2102.12981, https://arxiv.org/abs/2102.12981 |
| Citation label | Mehmood et al. (2021), Black-Box Simplex |
| Published / updated | 2021-02-24 / 2022-05-31 |
| DOI | 10.1007/978-3-031-06773-0_12 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the formal-methods/runtime-assurance queue; case studies, proofs, controller models, and runtime checks are not imported into this repository. |

## Thesis

Black-Box Simplex belongs in the runtime-adapter, readiness-gate, proof-envelope, and reference-architecture chapters as an external reference for runtime assurance. It gives the ASI Stack a concrete vocabulary for switching away from advanced but hard-to-verify behavior when runtime checks show safety risk.

## Mechanisms

- Use a runtime assurance framework where control authority can switch from an advanced controller to a backup baseline controller.
- Replace some static-verification requirements with runtime checks.
- Treat the advanced and baseline controllers as black boxes for the assurance architecture.
- Prove a safety architecture and evaluate case studies in autonomous cyber-physical systems.

## Evidence

- The source reports a Black-Box Simplex architecture, proof claims, and case studies in its own setting.
- This repository has not imported the proofs, models, case studies, controllers, or runtime checks.
- Use the source as external runtime-assurance vocabulary, not as proof that ASI Stack runtime adapters are safe.

## Failure Modes

- A fallback controller can be invoked too late if the runtime check lacks margin.
- A black-box controller may violate assumptions that the assurance wrapper cannot observe.
- Safety-switching language can be overapplied to software/tool workflows unless authority, state, and rollback records are explicit.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval` (Runtime Adapters, Tool Permissions, and Human Approval)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `integrated-reference-architecture` (Integrated Reference Architecture)

## Claims To Add Or Update

- Use this note to compare readiness gates and runtime adapters to runtime-assurance switching patterns.
- Do not claim that ASI Stack fallback, rollback, or quarantine gates have Simplex-level safety guarantees.
- Keep support state at `argument` until local monitor models, safety margins, runtime traces, or accepted evidence transitions exist.

## Open Questions

- What ASI Stack receipt should prove that a fallback route was selected before irreversible residuals grew too large?
- Which runtime-adapter states correspond to advanced controller, baseline controller, and switch decision?
- Can readiness-gate tests encode safety-margin obligations without overclaiming cyber-physical assurance?
