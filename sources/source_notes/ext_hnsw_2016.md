# Source Note: Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs

| Field | Value |
|---|---|
| Source ID | `ext_hnsw_2016` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/1603.09320> |
| Citation label | Malkov and Yashunin (2016), HNSW |
| Review scope | Author preprint abstract and hierarchical proximity graph construction. |

## Thesis

A hierarchy of neighbor graphs can guide approximate search without imposing a centroid partition.

## Mechanisms

Searches a hierarchy of proximity graphs over vectors. The graph can serve vector lookup without assigning the corpus to centroid buckets.

## Evidence

Provides a graph-based nearest-neighbor index comparison to an inverted file and exact scan.

[Section 4, graph construction and search-layer algorithms](https://arxiv.org/pdf/1603.09320).

## Failure Modes

Evaluate recall, tail latency, graph storage, and updates under the application workload. Search neighbors still require source admission.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](../../chapters/virtual-context-abi.qmd#choose-the-grouping-by-what-the-reader-needs)

## Claims To Add Or Update

Use exact-search recall at matched query latency when deciding between graph and centroid routes.

## Open Questions

After incremental insertion, which query families lose a required neighbor?
