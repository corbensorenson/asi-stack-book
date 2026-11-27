# Source Note: Flash-KMeans: Fast and Memory-Efficient Exact K-Means

| Field | Value |
|---|---|
| Source ID | `ext_flash_kmeans_2026` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2603.09229v2> |
| Citation label | Yang et al. (2026), Flash-KMeans |
| Review scope | Version 2 abstract and Bessa et al., Section 4 and Appendix C for the exact comparison configuration. |

## Thesis

A full-batch assignment can avoid materializing all point-center distances in device memory.

## Mechanisms

Fuses distance calculation with nearest-center selection to avoid writing the full distance matrix and groups centroid updates into reductions.

## Evidence

The paper evaluates a GPU implementation of full-batch k-means. The separate e-means paper compares with flash_kmeans 0.3.1.

[Section 4, especially FlashAssign (§4.1) and the grouped centroid update](https://arxiv.org/pdf/2603.09229v2).

## Failure Modes

Exact refers to the algorithmic assignment strategy at the chosen numerical precision. Initialization, stopping, hardware and workload affect a timing comparison.

## Book Chapters Supported

- `virtual-context-abi` — [Clustering the retrieval index](https://corbensorenson.github.io/asi-stack-book/chapters/virtual-context-abi.html#clustering-the-retrieval-index)

## Claims To Add Or Update

Compare the same precision, stopping rule and end-to-end cost before attributing a speed difference to a new objective.

## Open Questions

When does the grouped centroid update become the limiting operation?
