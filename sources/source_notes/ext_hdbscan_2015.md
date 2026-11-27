# Source Note: Hierarchical Density Estimates for Data Clustering, Visualization, and Outlier Detection

| Field | Value |
|---|---|
| Source ID | `ext_hdbscan_2015` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://doi.org/10.1145/2733381> |
| Citation label | Campello et al. (2015), HDBSCAN |
| Review scope | Primary paper summary and implementation-author documentation on mutual reachability, the condensed tree and cluster extraction. |

## Thesis

A density hierarchy can yield stable groups at different local density levels.

## Mechanisms

Builds a density hierarchy and extracts stable groups, with some points left as noise.

## Evidence

The authors describe extracting flat clusters by local cuts through the hierarchy, allowing different clusters to correspond to different density thresholds. [Authors’ publication record](https://researchonline.jcu.edu.au/47065/) The implementation FAQ discusses high-dimensional separation and sensitivity to minimum samples.

## Failure Modes

Small groups can be lost under the minimum cluster size. Rare or novel evidence may be labeled noise and needs an independent retention decision.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](../../chapters/virtual-context-abi.qmd#choose-the-grouping-by-what-the-reader-needs)

## Additional primary references

- <https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html>
- <https://hdbscan.readthedocs.io/en/latest/faq.html>

## Claims To Add Or Update

Retain rejected or low-stability points in a searchable fallback when clustering controls evidence access.

## Open Questions

How does the recovery of rare-source documents vary with minimum cluster size?
