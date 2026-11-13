# Source Note: Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs

| Field | Value |
|---|---|
| Source ID | `ext_hnsw_2016` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/1603.09320> |
| Citation label | Malkov and Yashunin (2016), HNSW |
| Review scope | Author preprint abstract and hierarchical proximity graph construction. |

## Mechanism

Searches a hierarchy of proximity graphs over vectors. The graph can serve vector lookup without assigning the corpus to centroid buckets.

## Evidence

Provides a graph-based nearest-neighbor index comparison to an inverted file and exact scan.

## Limits and failure modes

Evaluate recall, tail latency, graph storage, and updates under the application workload. Search neighbors still require source admission.

## Book chapters supported

- `virtual-context-abi`
