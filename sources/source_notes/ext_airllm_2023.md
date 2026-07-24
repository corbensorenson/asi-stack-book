# Source Note: AirLLM

| Field | Value |
|---|---|
| Source ID | `ext_airllm_2023` |
| Source title | AirLLM: Scaling Large Language Models on Low-End Commodity Computers |
| Ingestion date | 2026-07-23 |
| Source version / URL | Official main-branch repository and v3.0-era README, https://github.com/lyogavin/airllm |
| Ingestion basis | Official implementation README inspected; no local installation, model conversion, inference run, or benchmark. |

## Thesis

AirLLM is a practical layer-streaming implementation that trades storage and
I/O time for low accelerator residency. Its book value is the concrete claim
that model capacity can be decoupled from total VRAM when only a bounded shard
is resident, while making the disk-bandwidth and conversion costs impossible
to ignore.

## Mechanisms

- Decompose a downloaded model and save it in layer-wise shards.
- Keep roughly one layer on the GPU at a time.
- Prefetch a subsequent layer to overlap storage loading and compute.
- Optionally apply block-wise 4-bit or 8-bit weight compression to reduce the
  storage-loading bottleneck.
- Optionally delete the original downloaded model after transformation, while
  retaining the transformed copy.

## Evidence

- The official README reports support for very large contemporary models on
  small-VRAM devices and reports implementation-specific speed improvements
  from prefetch and compression.
- Those are maintainer-reported capabilities and measurements.
- This repository has not reproduced model loading, generation quality,
  latency, throughput, storage use, SSD wear, failure recovery, or hardware
  compatibility.

## Failure Modes

- “Fits in VRAM” can obscure unusable latency or total bytes read per token.
- Initial conversion can temporarily require both original and transformed
  copies and fail when storage is exhausted.
- Deleting the original changes recovery and derivative-custody obligations.
- Compression can be mistaken for exact paging.
- Layer-level predictability does not establish a general speculative-paging
  result for KV, experts, or future architectures.

## Book Chapters Supported

- `fast-generation-architectures`
- `personal-compute-hives-and-federated-edge-intelligence`
- `resource-economics-and-token-budgets`
- `model-weight-custody-and-hardware-roots-of-trust`
- `virtual-context-abi` (boundary comparator only: physical weight pages are not semantic context pages)

## Claims To Add Or Update

- Add AirLLM as an implementation comparator for deterministic layer streaming.
- Separate storage capacity from bandwidth, latency, endurance, and usability.
- Record transformed shards and deleted originals in model-family custody.
- Do not use the project README to claim independently verified speed, quality,
  model support, or hardware portability.

## Open Questions

- What exact shard identity and recovery contract does a converted model need?
- How much data is read per generated token under each model and cache setting?
- When does next-layer prefetch hide I/O, and when does it pollute memory or
  contend with KV traffic?
