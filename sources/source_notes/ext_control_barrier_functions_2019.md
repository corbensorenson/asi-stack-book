# Source Note: Control Barrier Functions

| Field | Value |
|---|---|
| Source ID | `ext_control_barrier_functions_2019` |
| Source title | Control Barrier Functions: Theory and Applications |
| Ingestion date | 2026-07-24 |
| Source version / URL | ECC 2019 / arXiv:1903.11199, https://arxiv.org/abs/1903.11199 |
| Citation label | Ames et al. (2019), Control Barrier Functions |
| Published / updated | 2019-04-10 / 2019-04-10 |
| DOI | 10.23919/ECC.2019.8796030 |
| Ingestion basis | Primary abstract and bibliographic record inspected; no theorem, controller, plant, or application reproduced. |

## Thesis

Control barrier functions provide one principled way to express and enforce
forward-invariance-style safety constraints in optimization-based control. The
guarantee remains conditional on the modeled dynamics, state estimate, safe
set, feasibility, timing, and implementation.

## Mechanisms

- Encode safety through a barrier function and admissible control constraint.
- Combine a nominal controller with a safety-filter optimization.
- Apply the framework to robotic and other safety-critical systems.

## Evidence

The source surveys theory and applications. This repository has not
implemented a barrier controller or verified its assumptions.

## Failure Modes

- Wrong dynamics or state estimate.
- Infeasible safety constraints.
- Sampling and actuation delay.
- A mathematically valid safe set that omits the real hazard.

## Book Chapters Supported

- `embodied-agency-real-time-control-and-physical-safety`

## Claims To Add Or Update

- A physical safety envelope must bind model and timing assumptions.
- Formal controller evidence cannot authorize a plant outside its certified
  domain.

## Open Questions

- Which low-energy plant can provide an independently measured positive control?
- How should barrier infeasibility route to fallback and effect residuals?
