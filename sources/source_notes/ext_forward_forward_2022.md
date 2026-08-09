# Source Note: The Forward-Forward Algorithm

| Field | Value |
|---|---|
| Source ID | `ext_forward_forward_2022` |
| Source version / URL | <https://arxiv.org/abs/2212.13345> |
| Ingestion date | 2026-08-09 |

## Thesis

The Forward-Forward proposal replaces a global forward-and-backward pass with
separate positive and negative forward passes and local layer objectives. It is
a useful counterexample to treating reverse-mode backpropagation as the only
conceivable credit-assignment architecture.

## Mechanisms

Each layer processes positive data that should have high local “goodness” and
negative data that should have low goodness. Learning uses local forward
computations instead of propagating one global error derivative backward
through every layer.

## Evidence

The paper explicitly presents preliminary investigations on comparatively small
problems. Its conceptual value exceeds its present evidence for large-scale
language models.

## Failure Modes

Positive/negative data construction, local goodness functions, layerwise update
order, and inference procedure are part of method identity. Local objectives
may fail to coordinate into a useful global representation. No claim of
large-scale parity or biological plausibility is imported here.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`
- `learning-theory-generalization-and-scaling-science`

## Claims To Add Or Update

- Local forward-only credit is a distinct learning route that a plural training
  stack should be able to describe and evaluate.
- Preliminary feasibility must not be transported into a foundation-model
  efficiency or generalization claim.

## Open Questions

- Can local goodness objectives coordinate at foundation-model scale?
- What state, phase ordering, negative-data policy, and inference conversion are
  required for faithful checkpoint and resume?
