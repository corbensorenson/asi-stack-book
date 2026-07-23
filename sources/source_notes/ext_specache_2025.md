# Source Note: SpeCache

| Field | Value |
|---|---|
| Source ID | `ext_specache_2025` |
| Source title | SpeCache: Speculative Key-Value Caching for Efficient Generation of LLMs |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2503.16163v1, https://arxiv.org/abs/2503.16163 |
| Ingestion basis | Public arXiv abstract and metadata inspected; paper, code, and benchmarks not reproduced locally. |

## Thesis

SpeCache keeps the complete KV cache in expandable CPU memory, preserves a
low-bit importance representation in VRAM, and predicts next-step KV pairs so
their transfer can overlap computation.

## Mechanisms

- Offload the complete KV cache to CPU memory.
- Keep a low-bit KV copy in VRAM for importance estimation.
- Dynamically fetch important KV pairs each decode step.
- Predict the next step's needed KV pairs and prefetch them early.
- Overlap host-to-device transfer with computation.

## Evidence

- The abstract reports LongBench and Needle-in-a-Haystack results, reduced VRAM,
  and source-specific quality behavior.
- These results remain source-reported and use a low-bit proxy plus dynamic
  selection.
- No local cache, quality, long-context, or performance result exists.

## Failure Modes

- Calling a low-bit proxy and selected fetch “no information loss” without
  checking output equivalence.
- Hidden host-memory requirements.
- Predictor drift, unused prefetch, cache pollution, and late-fetch stalls.
- Benchmark success that does not transfer to natural long-context workloads.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Add full-host-KV plus low-bit selection as a distinct speculative-paging arm.
- Require exact versus approximate output comparison and natural workload
  transfer.
- Charge host-memory capacity and low-bit proxy computation.

## Open Questions

- What is the actual fallback when an unselected KV pair becomes important?
- Does the low-bit proxy create distribution-specific blind spots?
- How should complete-host-cache custody and request isolation be checked?
