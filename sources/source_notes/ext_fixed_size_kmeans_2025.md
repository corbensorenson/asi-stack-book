# Source Note: Fixed-sized clusters k-Means

| Field | Value |
|---|---|
| Source ID | `ext_fixed_size_kmeans_2025` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2501.16113v1> |
| Citation label | Malinen and Fränti (2025), fixed-size k-means |
| Review scope | Version 1 abstract and fixed-size assignment formulation. |

## Mechanism

Optimizes squared error subject to declared cluster sizes using a constrained assignment step.

## Evidence

Fixed-size assignment illustrates the difference between a resource constraint and a purely nearest-center partition.

## Limits and failure modes

Equal bucket populations do not guarantee equal query traffic. The exact Hungarian assignment is expensive at scale.

## Book chapters supported

- `virtual-context-abi`
