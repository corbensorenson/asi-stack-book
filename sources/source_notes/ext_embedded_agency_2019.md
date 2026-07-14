# Source Note: Embedded Agency

| Field | Value |
|---|---|
| Source ID | `ext_embedded_agency_2019` |
| Source title | Embedded Agency |
| Ingestion date | 2026-07-14 |
| Source version / URL | arXiv:1902.09469v1, https://arxiv.org/abs/1902.09469 |
| Citation label | Demski and Garrabrant (2019), Embedded Agency |
| Published / updated | 2019-02-25 / 2019-02-25 |
| DOI | 10.48550/arXiv.1902.09469 |
| Ingestion basis | Primary arXiv abstract and canonical authors' full-text sequence sections on decision theory, embedded world-models, robust delegation, and subsystem alignment reviewed; no formal result was imported. |

## Thesis

Classical agent models often place an agent outside a fully modeled
environment. Real systems are physical parts of their worlds, must reason with
models smaller than those worlds, must reason about themselves, and contain
modifiable parts that can work at cross purposes. The paper surveys these
obstacles rather than claiming to solve them.

## Mechanisms

- Reject a clean Cartesian agent/environment boundary.
- Treat internal world models as bounded objects inside the modeled world.
- Preserve uncertainty about the system's own reasoning and future changes.
- Treat delegation and subsystem objectives as alignment problems, not merely
  implementation details.

## Evidence

This is a primary informal foundations survey. It supplies a strong objection
and vocabulary for limits; it does not provide a complete formal theory,
benchmark, deployed system, or evidence that the ASI Stack solves the surveyed
problems.

## Failure Modes

- A finite ledger can be mistaken for a complete external view of the system.
- Self-models and verifiers can share blind spots with the system they assess.
- Delegates and descendants can change the effective objective or ontology.
- Subsystem alignment can fail even when the top-level record is coherent.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model`
- `constitutional-alignment-substrate`
- `recursive-self-improvement-boundaries`
- `evidence-states-and-claim-discipline`
- `integrated-reference-architecture`

## Claims To Add Or Update

- State explicitly that record-level correctness is not embedded-agent
  correctness.
- Require verifier trust roots, recursion stops, descendant identity, and
  outside-model residuals without claiming completeness.
- Keep CAIS, corrigibility, Goodhart pressure, and embedded agency as distinct
  foundation-level constraints.

## Open Questions

- Which stack boundary is authoritative when the governing system is part of
  the environment it governs?
- How should ontology change invalidate old claims and permissions?
- What evidence can distinguish subsystem agreement from coordinated failure?
