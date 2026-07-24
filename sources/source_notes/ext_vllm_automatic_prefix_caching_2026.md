# Source Note: vLLM Automatic Prefix Caching

| Field | Value |
|---|---|
| Source ID | `ext_vllm_automatic_prefix_caching_2026` |
| Source title | Automatic Prefix Caching |
| Ingestion date | 2026-07-23 |
| Source version / URL | vLLM v0.14.1 design documentation, https://docs.vllm.ai/en/v0.14.1/design/prefix_caching/ |
| Ingestion basis | Official design documentation; no local vLLM deployment or benchmark. |

## Thesis

Completed KV blocks can be content-addressed by their parent hash, token block,
and relevant extra identity so later requests with the same prefix reuse
prefill state. Memory pressure still requires eviction, and shared
infrastructure needs explicit isolation.

## Mechanisms

- Chained block hashing for exact prefix identity.
- Extra identity for adapters and multi-modal inputs.
- Least-recently-used eviction among unreferenced cached blocks.
- Optional per-request cache salt to partition hash reuse and reduce timing
  inference across trust domains.

## Evidence

The documentation specifies the design and security option. It does not prove
collision behavior, latency improvement, eviction quality, or tenant isolation
for this repository.

## Failure Modes

- Reusing a block across incompatible adapters or multi-modal content.
- Hash collision or incomplete identity.
- Cross-tenant timing leakage.
- Eviction churn that makes lookup and hashing cost exceed reuse benefit.
- Counting resident blocks as reusable while they are still referenced or stale.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`
- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Make the parent chain and extra identity part of a cache receipt.
- Partition shared caches by trust domain where timing itself can disclose use.
- Report eviction and lookup work, not only hit count.

## Open Questions

- Which cryptographic or non-cryptographic hash policy is appropriate by threat model?
- How should distributed workers agree on invalidation epochs?
- What workload produces a net benefit after hashing and eviction?
