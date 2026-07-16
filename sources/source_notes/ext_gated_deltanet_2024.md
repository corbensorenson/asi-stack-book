# Source Note: Gated Delta Networks

| Field | Value |
|---|---|
| Source ID | `ext_gated_deltanet_2024` |
| Source title | Gated Delta Networks: Improving Mamba2 with Delta Rule |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2412.06464v3, https://arxiv.org/abs/2412.06464 |
| Ingestion basis | Primary preprint abstract and architecture/evaluation descriptions reviewed; no reproduction. |

## Thesis

Gated DeltaNet combines adaptive memory erasure with targeted delta-rule updates
and supplies parallel training algorithms for a linear recurrent sequence model.

## Mechanisms

- A gate controls how quickly recurrent memory is erased.
- A delta update targets changes to selected associations rather than only
  accumulating state.
- Hybrid variants combine Gated DeltaNet with sliding-window attention or
  Mamba-2 layers.

## Evidence

The paper reports language modeling, reasoning, retrieval, length-extrapolation,
long-context, and training-efficiency comparisons. No local training, kernel,
retrieval, extrapolation, or hardware result exists.

## Failure Modes

- Approximate recurrent memory may still fail exact identity or obligation tracking.
- Hybrid gains can hide attention, adapter, routing, and kernel costs.
- Source-reported retrieval gains may not survive changed task distributions or hardware.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat memory update and erasure rules as separately testable ABI properties.
- Include Gated DeltaNet-class linear recurrence and its hybrids in matched tournaments.

## Open Questions

- Which update rule best preserves exact state under distractors and overwrite pressure?
- Do hybrid gains remain after total lifecycle, routing, and hardware cost is counted?
