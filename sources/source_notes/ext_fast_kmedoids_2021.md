# Source Note: Fast and Eager k-Medoids Clustering: O(k) Runtime Improvement of the PAM, CLARA, and CLARANS Algorithms

| Field | Value |
|---|---|
| Source ID | `ext_fast_kmedoids_2021` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2008.05171v2> |
| Citation label | Schubert and Rousseeuw (2021), FasterPAM |
| Review scope | Version 2 abstract and PAM/FasterPAM mechanism description. |

## Thesis

An observed object can represent a group even when a meaningful arithmetic mean is unavailable.

## Mechanisms

Uses actual observations as representatives and minimizes assigned dissimilarity. FasterPAM improves swap search.

## Evidence

The comparison reports faster swaps for medoid methods and describes sampling variants.

[Section 3.2, Algorithm 4 and the breakdown of time spent on swaps and distances](https://arxiv.org/pdf/2008.05171v2).

## Failure Modes

Pairwise dissimilarity can dominate cost. A representative document still needs provenance and can omit important exceptions.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](../../chapters/virtual-context-abi.qmd#choose-the-grouping-by-what-the-reader-needs)

## Claims To Add Or Update

Charge distance computation and swaps before preferring a medoid for an evidence index.

## Open Questions

Does the selected representative retain the exception that changes the answer?
