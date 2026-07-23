# Source Note: PowerInfer

| Field | Value |
|---|---|
| Source ID | `ext_powerinfer_2024` |
| Source title | PowerInfer: Fast Large Language Model Serving with a Consumer-Grade GPU |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2312.12456v2 / SOSP 2024, https://arxiv.org/abs/2312.12456 |
| Ingestion basis | Public arXiv abstract and metadata inspected; full paper, models, predictors, and runtime not reproduced locally. |

## Thesis

PowerInfer uses source-reported power-law activation locality to split work
between GPU-resident hot neurons and CPU-executed cold neurons on a consumer
machine.

## Mechanisms

- Identify consistently hot and input-dependent cold neurons.
- Preload hot neurons on the GPU.
- Execute cold activated neurons on the CPU.
- Use adaptive predictors and neuron-aware sparse operators.
- Reduce GPU residency and CPU-GPU transfer through activation locality.

## Evidence

- The paper reports speed and accuracy results across selected models and
  hardware, including an RTX 4090.
- Those results are source-reported and depend on model sparsity, predictors,
  kernels, and comparison configuration.
- No predictor, sparse operator, accuracy, or performance result exists here.

## Failure Modes

- Assuming activation locality transfers to all architectures, fine-tunes,
  prompts, or distributions.
- Silent quality loss on predictor misses or cold-neuron undercoverage.
- Comparing a specialized sparse runtime to an under-tuned dense baseline.
- Describing predicted sparse execution as exact paging.

## Book Chapters Supported

- `fast-generation-architectures`
- `personal-compute-hives-and-federated-edge-intelligence`
- `resource-economics-and-token-budgets`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Add neuron-level hot/cold placement as an architecture-specific method.
- Require locality-shift and predictor-miss evaluation.
- Keep sparse execution, transfer reduction, and model quality as separate
  evidence lanes.

## Open Questions

- What is the correct exact fallback on a prediction miss?
- How stable is hot-neuron identity after fine-tuning or adapter changes?
- Which non-Transformer substrates admit analogous hot/cold object placement?
