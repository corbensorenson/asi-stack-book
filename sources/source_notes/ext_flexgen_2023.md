# Source Note: FlexGen

| Field | Value |
|---|---|
| Source ID | `ext_flexgen_2023` |
| Source title | FlexGen: High-Throughput Generative Inference of Large Language Models with a Single GPU |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2303.06865v2, https://arxiv.org/abs/2303.06865 |
| Ingestion basis | Public arXiv abstract and metadata inspected; paper and code not reproduced locally. |

## Thesis

FlexGen is the clearest source for workload-aware planning across GPU, CPU, and
disk. It targets latency-insensitive batched generation and therefore also
provides the book with a critical negative boundary: high throughput through
batch amortization is not interactive inference.

## Mechanisms

- Aggregate memory and computation across GPU, CPU, and disk.
- Solve a linear program to select tensor storage and access patterns.
- Increase the batch-size search space under a limited GPU-memory budget.
- Optionally compress weights and attention cache to 4-bit representations.

## Evidence

- The abstract reports source-specific OPT-175B and HELM throughput results on
  a single 16 GB GPU.
- Those results are scoped to the reported workload, models, compression,
  planning, and hardware.
- This repository has not reproduced the planner, compressed state, throughput,
  latency, quality, or storage behavior.

## Failure Modes

- Applying a latency-insensitive result to interactive batch-1 service.
- Crediting paging when batching or compression created the measured gain.
- Treating negligible reported accuracy loss as exactness.
- Optimizing a hardware cost model that omits thermal, endurance, recovery, or
  human wait cost.

## Book Chapters Supported

- `fast-generation-architectures`
- `personal-compute-hives-and-federated-edge-intelligence`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Add planned tensor placement as distinct from fixed layer streaming.
- Require workload-specific policy and separate batch throughput from latency.
- Require factorial accounting when placement, batching, and quantization are
  combined.

## Open Questions

- Can a current planner optimize first-token and inter-token latency without
  sacrificing stability?
- Which cost-model parameters must be measured rather than assumed?
- How does the result change under concurrent long-context KV pressure?
