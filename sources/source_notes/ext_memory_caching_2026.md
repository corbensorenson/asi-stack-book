# Source Note: Memory Caching

| Field | Value |
|---|---|
| Source ID | `ext_memory_caching_2026` |
| Source title | Memory Caching: RNNs with Growing Memory |
| Ingestion date | 2026-07-15 |
| Source version / URL | arXiv:2602.24281v1, https://arxiv.org/abs/2602.24281 |
| Ingestion basis | Primary preprint abstract and memory-design description reviewed; no implementation reproduced. |

## Thesis

Caching recurrent hidden-state checkpoints lets effective memory grow with
sequence length and creates an explicit trade between fixed recurrent state and
the growing addressable memory used by attention.

## Mechanisms

- Periodic hidden-state checkpoint caching.
- Gated aggregation and sparse selective variants.
- A tunable compute/memory trade between fixed-state recurrence and growing memory.

## Evidence

The paper reports improvements over recurrent baselines on language and long-
context tasks while Transformers remain strongest on its in-context recall
tests. No local quality, cost, cache-policy, or hardware result exists.

## Failure Modes

- Cached states can recreate an attention-like memory burden under another name.
- Aggregate hidden states may not preserve exact identity or revocation semantics.
- Cache selection, storage, lookup, and invalidation costs can dominate central-model savings.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Treat memory capacity as a measured axis, not a fixed property of an architecture label.
- Charge cache creation, selection, storage, lookup, migration, and deletion to total-system cost.

## Open Questions

- Where is the quality/cost frontier between fixed state, cached state, sparse retrieval, and attention?
- Can cached recurrent state be selectively invalidated and restored without full replay?
