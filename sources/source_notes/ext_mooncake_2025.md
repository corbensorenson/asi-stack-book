# Source Note: Mooncake

| Field | Value |
|---|---|
| Source ID | `ext_mooncake_2025` |
| Source title | Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot |
| Ingestion date | 2026-07-23 |
| Source version / URL | FAST 2025 paper page, https://www.usenix.org/conference/fast25/presentation/qin |
| Ingestion basis | Primary conference paper and official conference record inspected; no deployment or trace reproduced. |

## Thesis

KV cache can be treated as a distributed storage object spanning accelerator,
host memory, network, and persistent tiers. Disaggregating prefill and decode
allows storage capacity and bandwidth to substitute for repeated computation
within a bounded operating region.

## Mechanisms

- Separate prefill and decode pools.
- Distributed KV-cache storage and transfer.
- Placement and scheduling around memory, network, and accelerator capacity.
- Reuse informed by production request characteristics.

## Evidence

The paper reports production-trace and serving-capacity results and received a
FAST 2025 best-paper award. None of its deployment scale, performance, or
economic results is reproduced by this repository.

## Failure Modes

- Network or storage transfer dominates saved prefill.
- Persistent KV state outlives its authority, tenant, model, or source epoch.
- Disaggregation moves a bottleneck rather than removing it.
- Warm trace distributions conceal cold misses and burst behavior.
- More stored state increases privacy, deletion, and incident scope.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Treat cross-worker KV reuse as distributed state with placement and lifecycle receipts.
- Compare saved computation with storage, transfer, lookup, and governance cost.
- Report cold, warm, burst, and failure regimes separately.

## Open Questions

- Which KV objects deserve persistence beyond one worker or session?
- How should deletion and revocation propagate across tiers?
- When does recomputation beat remote retrieval?
