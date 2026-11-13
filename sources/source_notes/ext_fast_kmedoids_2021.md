# Source Note: Fast and Eager k-Medoids Clustering: O(k) Runtime Improvement of the PAM, CLARA, and CLARANS Algorithms

| Field | Value |
|---|---|
| Source ID | `ext_fast_kmedoids_2021` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2008.05171v2> |
| Citation label | Schubert and Rousseeuw (2021), FasterPAM |
| Review scope | Version 2 abstract and PAM/FasterPAM mechanism description. |

## Mechanism

Uses actual observations as representatives and minimizes assigned dissimilarity. FasterPAM improves swap search.

## Evidence

The comparison reports faster swaps for medoid methods and describes sampling variants.

## Limits and failure modes

Pairwise dissimilarity can dominate cost. A representative document still needs provenance and can omit important exceptions.

## Book chapters supported

- `virtual-context-abi`
