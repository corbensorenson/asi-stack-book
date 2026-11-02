# Source Note: Proving and Improving the Platonic Representation Hypothesis with JEPAs

| Field | Value |
|---|---|
| Source ID | `ext_platonic_representation_jepa_2026` |
| Ingestion date | 2026-11-02 |
| Primary version | [arXiv:2610.39302v1](https://arxiv.org/html/2610.39302v1) |
| Citation | Balestriero and LeCun (2026), Platonic representations with JEPAs |
| Published / updated | 2026-10-29 / 2026-10-29 |
| Review scope | Sections 2.1–2.3, 4.2–4.3, 5.1–5.2 and 7; selected Appendix A.2 coordinate-change and spectral proof steps. Scope reading only, not a full proof audit, code review or replication. |
| Custody | Public-safe authored note only; raw primary HTML remains in ignored local research cache. |

## Thesis
The paper makes shared positive-pair structure a sufficient condition for cross-modal agreement up to rotation in an idealized JEPA setting, and tests view construction as an alignment lever.

## Mechanisms
Section 2.1 assumes a finite world, injective renderings, shared positive-pair distribution/marginals, population minima and uniqueness up to rotation. A whitened squared-loss spectral case establishes uniqueness with an eigengap. The predictor is the identity; learned, action-conditioned world-model predictors are explicitly outside this analysis. Sections 2.2–2.3 bound spectral mismatch and distinguish independent observations of a scene from corruptions that share one observation's nuisance.

## Evidence
Sections 4.2–4.3 report 42-fold fewer training samples for one alignment comparison and a 109M text encoder exceeding evaluated LMs through 72B on specified alignment measures. These are authors' results, not local reproduction or general task superiority. The 42-fold comparison uses different scale recipes and no earlier next-token checkpoint; it is not a wall-time/energy ratio.

## Failure Modes
Section 7 states that no experiment exactly meets the principal theorem's assumptions. LeJEPA's full-distribution uniqueness remains assumed. Good views require scene grouping; large-scale captions include image-captioner distillation, hyperparameters favor the good-view recipe, and overlap/seed sensitivities remain relevant. Captioning fits a map on pairs; the pair-free classification experiment is separate. Invariance useful for alignment may discard camera pose needed by a controller.

## Claims To Add Or Update
Treat the theorem as conditional and the empirical comparisons as task-specific. Keep this source separate from Sorenson's semantic-constitution proposal.

## Open Questions
Which alignment improvements survive independent tasks, lossy modalities and stronger matched baselines?

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`
- `learning-theory-generalization-and-scaling-science`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Chapter Decision

Update existing owners through `new_paper_triage_scenarios/jepa_platonic_and_hnet_2026_11_02.json`. No new chapter, no claim-core promotion, no local model result.
