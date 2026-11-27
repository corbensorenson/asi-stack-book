# Source Note: Concept Decompositions for Large Sparse Text Data Using Clustering

| Field | Value |
|---|---|
| Source ID | `ext_spherical_kmeans_2001` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://www.cs.utexas.edu/~inderjit/public_papers/concept_mlj.pdf> |
| Citation label | Dhillon and Modha (2001), spherical k-means |
| Review scope | Author-hosted paper, abstract and spherical k-means formulation. |

## Thesis

Direction can serve as the clustering geometry for normalized sparse text vectors.

## Mechanisms

Clusters normalized document vectors by cosine similarity to unit-normalized mean directions.

## Evidence

The authors study sparse text vectors and compare their concept-vector subspaces with truncated singular-vector subspaces.

[Cosine similarity, normalized concept vectors and the concept decomposition](https://www.cs.utexas.edu/~inderjit/public_papers/concept_mlj.pdf).

## Failure Modes

Normalization discards magnitude. Hard assignments can conceal overlap and depend on the geometry of the representation.

## Book Chapters Supported

- `virtual-context-abi` — [Choose the grouping by what the reader needs](https://corbensorenson.github.io/asi-stack-book/chapters/virtual-context-abi.html#choose-the-grouping-by-what-the-reader-needs)

## Claims To Add Or Update

Choose cosine geometry only after deciding whether vector magnitude carries information the reader needs.

## Open Questions

Do rare documents change groups when length normalization or the vocabulary changes?
