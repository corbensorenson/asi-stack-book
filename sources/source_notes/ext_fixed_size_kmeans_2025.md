# Source Note: Fixed-sized clusters k-Means

| Field | Value |
|---|---|
| Source ID | `ext_fixed_size_kmeans_2025` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2501.16113v1> |
| Citation label | Malinen and Fränti (2025), fixed-size k-means |
| Review scope | Version 1 abstract and fixed-size assignment formulation. |

## Thesis

A cardinality constraint changes the feasible assignments in a clustering problem.

## Mechanisms

Optimizes squared error subject to declared cluster sizes using a constrained assignment step.

## Evidence

Fixed-size assignment illustrates the difference between a resource constraint and a purely nearest-center partition.

[Algorithm 1 and section 3 on the assignment cost](https://arxiv.org/pdf/2501.16113v1).

## Failure Modes

Equal bucket populations do not guarantee equal query traffic. The exact Hungarian assignment is expensive at scale.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](../../chapters/virtual-context-abi.qmd#choose-the-grouping-by-what-the-reader-needs)

## Claims To Add Or Update

Measure the resulting query load as well as the enforced bucket sizes.

## Open Questions

Does enforcing equal populations reduce tail latency on the actual query distribution?
