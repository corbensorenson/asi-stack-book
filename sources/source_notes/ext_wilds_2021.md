# Source Note: WILDS

| Field | Value |
|---|---|
| Source ID | `ext_wilds_2021` |
| Source title | WILDS: A Benchmark of in-the-Wild Distribution Shifts |
| Ingestion date | 2026-07-24 |
| Source version / URL | ICML 2021, https://proceedings.mlr.press/v139/koh21a.html |
| Citation label | Koh et al. (2021), WILDS |
| Published / updated | 2021-07-18 / 2021-07-18 |
| DOI | not assigned in the inspected record |
| Ingestion basis | Primary PMLR abstract, dataset scope, and reported baseline summary inspected; no dataset or model run locally. |

## Thesis

Naturally occurring shifts across institutions, geography, time, and data
collection can create material performance gaps that standard IID benchmarks
underrepresent.

## Mechanisms

- Curate ten datasets with documented real-world shifts.
- Standardize loading, models, hyperparameters, and evaluation.
- Report in-distribution and out-of-distribution performance separately.

## Evidence

The benchmark and gaps are source-reported. WILDS is not a universal OOD suite
and does not cover every modality, task, safety consequence, or adaptive agent.

## Failure Modes

- One synthetic corruption suite standing in for natural shift.
- Aggregate accuracy hiding subgroup or environment tails.
- Benchmark-specific robustness failing on a new shift.
- Test-domain information leaking into selection.

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- World-model evidence needs both designed perturbations and natural shifts.
- Environment and cohort denominators remain explicit.

## Open Questions

- Which WILDS-style split best matches observation-to-action governance?
- How should the book represent shift severity and operator cost jointly?
