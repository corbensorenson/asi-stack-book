# Source Note: Capability-Based Computer Systems

| Field | Value |
|---|---|
| Source ID | `ext_capability_based_computer_systems_1984` |
| Source title | Capability-Based Computer Systems |
| Ingestion date | 2026-06-29 |
| Source version / URL | University of Washington online book page, https://homes.cs.washington.edu/~levy/capabook/ |
| Citation label | Levy (1984), Capability-Based Computer Systems |
| Published / updated | 1984 / 1984 |
| Ingestion basis | Public university-hosted book page inspected for the SCF external-positioning queue; book not vendored into this repository and no capability system implemented. |

## Thesis

Capability-based computer systems are a direct external comparator for authority-bearing references and protection boundaries. They help position Stable Capability Fields beside established systems work on capabilities while preserving the ASI Stack distinction between a capability name, its authority ceiling, and the implementation that may satisfy it.

## Mechanisms

- Treat capabilities as authority-bearing references.
- Bind access rights to possession or mediation of capabilities.
- Separate protection domains, objects, and rights.
- Use capability discipline to reason about confinement, delegation, and authority boundaries.

## Evidence

- The source is a classic systems text; this repository has not implemented or evaluated a capability system from it.
- Use it to source-note the authority-boundary comparator for SCF, not to claim ASI Stack route enforcement or security.

## Failure Modes

- Capability terminology can be imported while actual authority enforcement is absent.
- A capability boundary can be confused with semantic capability identity.
- Delegation and revocation need implementation-specific behavior that this repo has not built.
- Authority references do not by themselves prove qualification evidence, evaluator independence, or rollback readiness.

## Book Chapters Supported

- `stable-capability-fields` (Stable Capability Fields)

## Claims To Add Or Update

- Use this source to position SCF authority ceilings beside capability-system authority boundaries.
- Keep SCF as a broader governed capability-identity record, not a claim of implemented object-capability security.
- Do not promote deployed route validation, least-authority enforcement, confinement, or revocation behavior without local evidence.

## Open Questions

- Which SCF fields should be treated as authority-bearing capability grants versus semantic identity metadata?
- Should capability revocation become a first-class rollback or lease-expiry test?
- What negative control would show a replacement widening authority without an explicit governance grant?
