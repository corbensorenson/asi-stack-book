# Source Note: Efficient Memory Management for Large Language Model Serving with PagedAttention

| Field | Value |
|---|---|
| Source ID | `ext_pagedattention_vllm_2023` |
| Source title | Efficient Memory Management for Large Language Model Serving with PagedAttention |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2309.06180, https://arxiv.org/abs/2309.06180 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation and resource-economics literature queues; paper not vendored into this repository. |

## Thesis

PagedAttention and vLLM treat KV-cache memory as a serving bottleneck. Their book value is to separate aggregate serving throughput and memory utilization from single-request verified-output quality: serving acceleration is a different evidence lane from decoding correctness.

## Mechanisms

- Partition KV-cache memory into paged blocks inspired by operating-system virtual memory.
- Reduce fragmentation and redundant cache duplication.
- Support flexible cache sharing across requests.
- Increase batching capacity and serving throughput under the paper's evaluated workloads.
- Treat scheduler and cache manager behavior as part of the generation substrate.

## Evidence

- The source reports throughput and latency results for vLLM compared with selected serving baselines.
- This repository has not deployed vLLM, reproduced PagedAttention benchmarks, or measured local KV-cache behavior.
- Use the source to support the KV-cache/serving taxonomy and the need for separate memory/throughput accounting.

## Failure Modes

- Aggregate throughput gains can be mistaken for lower single-request latency or better answer quality.
- Memory savings may depend on request length distribution, batching policy, hardware, and model architecture.
- Cache sharing creates its own isolation, taint, and scheduling questions in governed systems.
- Serving metrics do not replace verifier cost, accepted-output accounting, or task-success measurement.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)

## Claims To Add Or Update

- Use this source to source-note KV-cache and serving-layer acceleration as a separate mode family.
- Require fast-generation records to separate throughput, memory pressure, latency, and verified-output metrics.
- Use this source in resource economics to separate serving-memory and aggregate-throughput gains from verified-output quality and task-success claims.
- Do not use this note to claim local serving performance or quality improvement.

## Open Questions

- What local fixture should record KV-cache memory pressure without running a full serving benchmark?
- How should cache sharing interact with VCM taint, revocation, and authority labels?
- Which reader-facing diagram best separates serving throughput from verified cognition per second?
