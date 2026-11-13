# Source Note: A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise

| Field | Value |
|---|---|
| Source ID | `ext_dbscan_1996` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://cdn.aaai.org/KDD/1996/KDD96-037.pdf> |
| Citation label | Ester et al. (1996), DBSCAN |
| Review scope | Sections 3 and 4 on density reachability, noise and the neighborhood rule. |

## Mechanism

Expands groups through connected core neighborhoods under a distance radius and minimum neighbor count.

## Evidence

The authors demonstrate nonconvex groups and noise handling on spatial datasets.

## Limits and failure modes

A single neighborhood scale can merge nearby groups or discard sparse groups. Noise status depends on the metric and settings.

## Book chapters supported

- `virtual-context-abi`
