# Source Note: Ward’s Hierarchical Clustering Method: Clustering Criterion and Agglomerative Algorithm

| Field | Value |
|---|---|
| Source ID | `ext_ward_hierarchical_2014` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/1111.6285v2> |
| Citation label | Murtagh and Legendre (2014), Ward linkage |
| Review scope | Version 2 abstract and discussion of the Ward merge criterion. |

## Thesis

Ward's minimum-variance criterion depends on the distance convention used in the merge updates.

## Mechanisms

Builds a hierarchy by repeatedly merging groups. Ward linkage uses the increase in within-group squared error to choose a merge.

## Evidence

The paper reconciles implementations with different conventions for squared and unsquared distances.

[Sections 3.2 and 3.3, Ward1 and Ward2 conventions](https://arxiv.org/pdf/1111.6285v2).

## Failure Modes

A tree cut and linkage define which groups appear. Early merges affect every coarser level.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](../../chapters/virtual-context-abi.qmd#choose-the-grouping-by-what-the-reader-needs)

## Claims To Add Or Update

Before comparing dendrogram cuts, record the linkage implementation and its distance convention.

## Open Questions

Does a change in normalization alter the first irreversible merge involving a rare source?
