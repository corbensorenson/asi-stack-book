# Source Note: LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics

| Field | Value |
|---|---|
| Source ID | `ext_lejepa_2025` |
| Ingestion date | 2026-11-02 |
| Primary version | [arXiv:2511.08544v3](https://arxiv.org/html/2511.08544v3) |
| Citation | Balestriero and LeCun (2025), LeJEPA |
| Published / updated | 2025-11-11 / 2025-11-14 |
| Review scope | Abstract; Sections 1, 4.1–4.3 and 5.1–5.2; Section 6 evaluation framing. Selected primary HTML passages; no independent theorem verification or experiments. |
| Custody | Public-safe authored note only; raw primary HTML remains in ignored local research cache. |

## Thesis
LeJEPA combines predictive agreement with SIGReg, which pushes embedding distributions toward an isotropic Gaussian through one-dimensional projections.

## Mechanisms
Sections 4–5 connect distribution matching, characteristic-function tests and a predictive objective. The implemented recipe avoids the stop-gradient and teacher–student machinery used by several other JEPAs. This does not make those components absent from the whole JEPA family.

## Evidence
The authors report evaluations across architectures and domains. No reported model, metric, complexity implementation or training-stability result was reproduced here.

## Failure Modes
Distributional regularization is not a guarantee of useful semantics or downstream control. The 2026 Platonic-representation paper explicitly leaves uniqueness under LeJEPA's full-distribution constraint as an assumption; it proves the spectral uniqueness result for a different second-order setting.

## Claims To Add Or Update
Record the objective, view construction and collapse-prevention recipe separately from the encoder architecture. Do not transfer a conditional theorem between different objectives by the JEPA name.

## Open Questions
Does an alignment gain preserve the information the intended downstream task needs?

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`
- `learning-theory-generalization-and-scaling-science`

## Chapter Decision

Update existing owners through `new_paper_triage_scenarios/jepa_platonic_and_hnet_2026_11_02.json`. No new chapter, no claim-core promotion, no local model result.
