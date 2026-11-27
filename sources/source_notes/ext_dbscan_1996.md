# Source Note: A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise

| Field | Value |
|---|---|
| Source ID | `ext_dbscan_1996` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://cdn.aaai.org/KDD/1996/KDD96-037.pdf> |
| Citation label | Ester et al. (1996), DBSCAN |
| Review scope | Sections 3 and 4 on density reachability, noise and the neighborhood rule. |

## Thesis

Connectivity between dense neighborhoods can recover groups with irregular shapes.

## Mechanisms

Expands groups through connected core neighborhoods under a distance radius and minimum neighbor count.

## Evidence

The authors demonstrate nonconvex groups and noise handling on spatial datasets.

[Density-reachability definitions and section 5 on synthetic and SEQUOIA data](https://cdn.aaai.org/KDD/1996/KDD96-037.pdf).

## Failure Modes

A single neighborhood scale can merge nearby groups or discard sparse groups. Noise status depends on the metric and settings.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](../../chapters/virtual-context-abi.qmd#choose-the-grouping-by-what-the-reader-needs)

## Claims To Add Or Update

Keep an explicit route for noise points when density clusters control access to source documents.

## Open Questions

Does a single radius preserve a small but distinct document family during index rebuild?
