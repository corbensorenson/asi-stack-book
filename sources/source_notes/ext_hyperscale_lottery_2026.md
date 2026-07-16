# Source Note: The Hyperscale Lottery

| Field | Value |
|---|---|
| Source ID | `ext_hyperscale_lottery_2026` |
| Source title | The Hyperscale Lottery: How State-Space Models Have Sacrificed Edge Efficiency |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2604.07935v1 (submitted 2026-04-09), https://arxiv.org/abs/2604.07935 |
| Ingestion basis | Primary preprint abstract and reported edge-latency comparison reviewed; no implementation or result reproduced. |

## Thesis

State-space architectures optimized to saturate hyperscale GPUs can lose part of
their expected efficiency on smaller edge targets, so asymptotic complexity and
cloud throughput are not sufficient deployment-cost measures.

## Mechanisms

- Platform-stratified latency measurement across Mamba-family variants.
- Separation of algorithmic complexity from realized hardware utilization.
- Pressure against treating cloud-scale kernel design as device-neutral.

## Evidence

The preprint reports a 28-percent latency increase for a tested 880M-parameter
Mamba-3 configuration and a 48-percent increase at 15M parameters relative to
its selected earlier-Mamba comparison. These figures are source-reported,
hardware- and implementation-specific, and unreproduced in this repository.

## Failure Modes

- Selected edge devices, kernels, or model configurations may not generalize.
- Latency alone can hide quality, throughput, memory, and energy tradeoffs.
- A negative hardware result can be overextended into a verdict on SSM quality.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Compare cloud throughput, edge latency, peak and resident memory, and energy
  separately before calling a substrate efficient.
- Bind architecture qualification to exact hardware and runtime versions.

## Open Questions

- Which Mamba-family features drive the reported edge penalty?
- Do optimized edge kernels change the quality-cost frontier?
- How stable are the results across accelerators, quantization, and batch size?
