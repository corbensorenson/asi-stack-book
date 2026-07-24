# Source Note: CacheBlend

| Field | Value |
|---|---|
| Source ID | `ext_cacheblend_2025` |
| Source title | CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion |
| Ingestion date | 2026-07-23 |
| Source version / URL | arXiv:2405.16444v3, https://arxiv.org/abs/2405.16444 |
| Ingestion basis | Primary paper abstract and paper record inspected; no code or benchmark reproduced. |

## Thesis

Independent KV caches for retrieved chunks cannot simply be concatenated when
the chunks occupy new positions or depend on preceding context. Selective
recomputation can restore part of the missing cross-attention while retaining
some reuse.

## Mechanisms

- Cache KV state for reusable knowledge chunks.
- Retrieve several chunk caches for one RAG request.
- Selectively recompute token KV state to account for new context.
- Pipeline recomputation with slower-tier KV retrieval.

## Evidence

The paper reports time-to-first-token and throughput improvements without
measured quality loss on its named models and datasets. Those results remain
source-reported.

## Failure Modes

- Naïve concatenation omits cross-attention and can change the answer.
- The selector can recompute too little to preserve quality.
- Retrieval and storage overhead can erase the latency benefit.
- A quality result on a few tasks does not establish exact equivalence.
- Cached chunks can be stale, revoked, or unauthorized even when numerically reusable.

## Book Chapters Supported

- `fast-generation-architectures`
- `resource-economics-and-token-budgets`

## Claims To Add Or Update

- Classify non-prefix KV fusion as approximate unless full recomputation or an
  accepted equivalence argument restores the same computation.
- Require method-specific quality tests for selective recomputation.
- Keep context validity separate from numerical cache compatibility.

## Open Questions

- Which token-selection signals transfer across models and tasks?
- What exactness or quality contract should govern partial recomputation?
- How should cache reuse interact with changing retrieval order?
