# Source Note: Flash-KMeans: Fast and Memory-Efficient Exact K-Means

| Field | Value |
|---|---|
| Source ID | `ext_flash_kmeans_2026` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2603.09229v2> |
| Citation label | Yang et al. (2026), Flash-KMeans |
| Review scope | Version 2 abstract and Bessa et al., Section 4 and Appendix C for the exact comparison configuration. |

## Mechanism

Fuses distance calculation with nearest-center selection to avoid writing the full distance matrix and groups centroid updates into reductions.

## Evidence

The paper evaluates a GPU implementation of full-batch k-means. The separate e-means paper compares with flash_kmeans 0.3.1.

## Limits and failure modes

Exact refers to the algorithmic assignment strategy at the chosen numerical precision. Initialization, stopping, hardware and workload affect a timing comparison.

## Book chapters supported

- `virtual-context-abi`
