# Source Note: Ward’s Hierarchical Clustering Method: Clustering Criterion and Agglomerative Algorithm

| Field | Value |
|---|---|
| Source ID | `ext_ward_hierarchical_2014` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/1111.6285v2> |
| Citation label | Murtagh and Legendre (2014), Ward linkage |
| Review scope | Version 2 abstract and discussion of the Ward merge criterion. |

## Mechanism

Builds a hierarchy by repeatedly merging groups. Ward linkage uses the increase in within-group squared error to choose a merge.

## Evidence

The paper reconciles implementations with different conventions for squared and unsquared distances.

## Limits and failure modes

A tree cut and linkage define which groups appear. Early merges affect every coarser level.

## Book chapters supported

- `virtual-context-abi`
