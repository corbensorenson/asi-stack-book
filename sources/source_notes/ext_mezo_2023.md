# Source Note: Fine-Tuning Language Models with Just Forward Passes

| Field | Value |
|---|---|
| Source ID | `ext_mezo_2023` |
| Source version / URL | <https://arxiv.org/abs/2305.17333> |
| Ingestion date | 2026-08-09 |

## Thesis

MeZO adapts a memory-efficient zeroth-order estimator to language-model
fine-tuning and reconstructs perturbations in place from random seeds. It shows
that a forward-only update can approach the memory footprint of inference and
can optimize objectives for which gradients are unavailable.

## Mechanisms

MeZO estimates a directional derivative from perturbed forward evaluations and
regenerates perturbations from a random seed rather than storing a full
parameter-sized noise tensor. It applies the scalar estimate without retaining
a backward activation graph.

## Evidence

The paper reports up to twelve-fold memory reduction and, in selected settings,
up to two-fold GPU-hour reduction relative to its fine-tuning baselines. These
are source-reported, setting-bound results.

## Failure Modes

Results depend on task, scale, prompt regime, perturbation estimator, and
baseline competence. Forward-only does not mean evaluation-free, universally
faster, or lower variance; query count, objective calls, perturbation scale, and
seed policy remain part of method identity and total cost.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Backward activation memory is optional for some useful model updates, so a
  substrate ABI should not require reverse-mode differentiation.
- Memory footprint, query count, quality, and total GPU-hours must be compared
  jointly.

## Open Questions

- How does MeZO scale under competent parameter-efficient and full fine-tuning
  baselines on modern models?
- Which nondifferentiable objectives justify its estimator variance and query
  cost?
