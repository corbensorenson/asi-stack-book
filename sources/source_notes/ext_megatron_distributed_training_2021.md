# Source Note: Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM

| Field | Value |
|---|---|
| Source ID | `ext_megatron_distributed_training_2021` |
| Source title | Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2104.04473v5, https://arxiv.org/abs/2104.04473 |
| Citation label | Narayanan et al. (2021), Efficient Large-Scale Language Model Training |
| Published / updated | 2021-04-09 / 2021-08-30 |
| DOI | 10.1145/3458817.3476209 |
| Ingestion basis | Primary paper reviewed, especially Sections 1--3 and 5--6; no code, cluster, run, or result reproduced. |

## Thesis

Tensor, pipeline, and data parallelism have interacting memory, communication,
batch, bubble, and optimizer-semantics costs. The paper composes them for large
GPU clusters and studies configuration tradeoffs rather than treating device
count as a sufficient explanation of scale.

## Mechanisms

- Tensor parallelism within layers, pipeline parallelism across stages, and
  data parallelism across replicas.
- Synchronized optimizer steps preserve strict optimizer semantics but force
  pipeline flushes.
- Interleaved schedules, microbatch choice, and topology-aware placement trade
  memory, communication, and idle time.
- Analytic and empirical configuration guidance rather than an automatic
  parallelism search.

## Evidence

The paper reports a trillion-parameter training iteration on 3,072 A100 GPUs,
502 petaFLOP/s aggregate throughput, and 52% of theoretical peak. These results
are tied to its exact model, cluster, software, and measurement definitions and
were not reproduced here.

## Failure Modes

- Combining individually sound parallelism methods without measuring their
  interactions.
- Tuning for throughput while silently changing optimizer semantics or global
  batch behavior.
- Reporting peak arithmetic without data processing, optimization,
  communication, bubbles, and failed-run denominators.
- Generalizing from a regular Transformer stack to asymmetric architectures or
  different networks.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- Boundary context: `replaceable-cognitive-substrates-beyond-transformer-monoculture`
  and `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Record the complete parallelism topology and optimizer synchronization
  semantics as part of run identity.
- Compare manual, sharded, and compiler-selected topologies under matched
  quality targets and full lifecycle cost.
- Keep source-reported throughput scoped to the measured configuration.

## Open Questions

- Which topology changes preserve numerical and data-order equivalence?
- How should topology search failures and rejected configurations remain in the
  run denominator?
