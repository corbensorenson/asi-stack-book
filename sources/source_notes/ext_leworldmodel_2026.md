# Source Note: LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels

| Field | Value |
|---|---|
| Source ID | `ext_leworldmodel_2026` |
| Review date | 2026-11-02 |
| Primary version | [2603.19312v3](https://arxiv.org/html/2603.19312v3) |
| Citation | Maes et al. (2026), LeWorldModel |
| Published / updated | 2026-03-13 / 2026-06-03 |
| Review scope | Sections 3.1–3.2 and Limitations & Future Work; June 3 revision. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Supplies an action-conditioned latent-dynamics example alongside our representation-only JEPA discussion: pixel encoder, next-embedding predictor, Gaussian regularization and latent-space planning.

## Mechanisms

Train a pixel encoder and action-conditioned next-latent predictor using predictive loss and Gaussian regularization. At inference, optimize a finite action sequence toward a latent goal while holding the world model fixed.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

Selected method and limitation passages distinguish offline action-labeled dynamics learning from later planning, and retain short-horizon and data-coverage limits. Probes and surprise tests are not physical safety evidence. No study, code or proof was independently reproduced here.

## Failure Modes

Uses offline action-labeled trajectories with coverage requirements and short planning horizons. Latent structure or surprise detection is not complete physical understanding or a safety certificate.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
