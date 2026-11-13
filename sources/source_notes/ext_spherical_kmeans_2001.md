# Source Note: Concept Decompositions for Large Sparse Text Data Using Clustering

| Field | Value |
|---|---|
| Source ID | `ext_spherical_kmeans_2001` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://www.cs.utexas.edu/~inderjit/public_papers/concept_mlj.pdf> |
| Citation label | Dhillon and Modha (2001), spherical k-means |
| Review scope | Author-hosted paper, abstract and spherical k-means formulation. |

## Mechanism

Clusters normalized document vectors by cosine similarity to unit-normalized mean directions.

## Evidence

The authors study sparse text vectors and compare their concept-vector subspaces with truncated singular-vector subspaces.

## Limits and failure modes

Normalization discards magnitude. Hard assignments can conceal overlap and depend on the geometry of the representation.

## Book chapters supported

- `virtual-context-abi`
