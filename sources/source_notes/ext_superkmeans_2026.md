# Source Note: A Super Fast K-means for Indexing Vector Embeddings

| Field | Value |
|---|---|
| Source ID | `ext_superkmeans_2026` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/html/2603.20009v1> |
| Citation label | Kuffo et al. (2026), SuperKMeans |
| Review scope | Sections 2.3, 3.1–3.3, 4.3 and 4.4. |

## Thesis

A retrieval index can stop gaining recall before the clustering objective stops improving.

## Mechanisms

Rotates embeddings for probabilistic partial-distance pruning. Optional early termination monitors nearest-neighbor recall on query examples.

## Evidence

The experiments distinguish clustering runtime, retrieval recall and the number of vectors explored. Recall can flatten before the clustering iterations finish.

[GEMM and PRUNING phases, random rotation and recall-based termination](https://arxiv.org/html/2603.20009v1).

## Failure Modes

Early stopping depends on query representativeness and nearest-neighbor ground truth. Large and small k regimes have different pruning economics.

## Book Chapters Supported

- `virtual-context-abi` — [Clustering the retrieval index](../../chapters/virtual-context-abi.qmd#clustering-the-retrieval-index)

## Claims To Add Or Update

Choose the stopping rule using representative queries and charge the cost of acquiring recall labels.

## Open Questions

Do infrequent evidence queries lose recall after the aggregate curve flattens?
