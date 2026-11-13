# Source Note: Hierarchical Density Estimates for Data Clustering, Visualization, and Outlier Detection

| Field | Value |
|---|---|
| Source ID | `ext_hdbscan_2015` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://doi.org/10.1145/2733381> |
| Citation label | Campello et al. (2015), HDBSCAN |
| Review scope | Primary paper summary and implementation-author documentation on mutual reachability, the condensed tree and cluster extraction. |

## Mechanism

Builds a density hierarchy and extracts stable groups, with some points left as noise.

## Evidence

A density hierarchy supports discovery at several neighborhood scales. The implementation FAQ discusses high-dimensional separation and sensitivity to minimum samples.

## Limits and failure modes

Small groups can be lost under the minimum cluster size. Rare or novel evidence may be labeled noise and needs an independent retention decision.

## Book chapters supported

- `virtual-context-abi`

## Additional primary references

- <https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html>
- <https://hdbscan.readthedocs.io/en/latest/faq.html>
