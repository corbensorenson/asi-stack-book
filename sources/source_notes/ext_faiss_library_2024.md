# Source Note: The Faiss Library

| Field | Value |
|---|---|
| Source ID | `ext_faiss_library_2024` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2401.08281> |
| Citation label | Douze et al. (2024), Faiss |
| Review scope | Author paper sections on inverted files, graph-based search and compressed codes, with the official Faiss index documentation. |

## Thesis

Coarse routing, vector storage and approximate distance computation are independently configurable.

## Mechanisms

An inverted file uses coarse centroids to organize postings. Vector quantization can instead encode a vector using centroid IDs, including separate subspace codes in product quantization.

## Evidence

The index documentation distinguishes full-vector IVF postings, product-quantized postings, flat search, and HNSW graph search.

[Section 4 on compression and the discussion of non-exhaustive search](https://arxiv.org/pdf/2401.08281).

## Failure Modes

A routing centroid can coexist with full stored vectors. A quantized reconstruction and search over a subset of postings have separate error and cost budgets.

## Book Chapters Supported

- `virtual-context-abi` — [Clustering the retrieval index](../../chapters/virtual-context-abi.qmd#clustering-the-retrieval-index)
- `rankfold-neuralfold-and-artifact-compression` — [Count the vector codebook and its reconstruction error](../../chapters/rankfold-neuralfold-and-artifact-compression.qmd#vector-codebook-cost)

## Additional primary references

- <https://github.com/facebookresearch/faiss/wiki/Faiss-indexes/aeda38e6c323d6e3f0a207db875918f1185aa7bb>

## Claims To Add Or Update

Record the scanned posting budget and the stored representation separately in every index comparison.

## Open Questions

At fixed memory, does pruning postings or compressing their vectors lose the decisive evidence first?
