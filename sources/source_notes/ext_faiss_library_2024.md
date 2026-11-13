# Source Note: The Faiss Library

| Field | Value |
|---|---|
| Source ID | `ext_faiss_library_2024` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/abs/2401.08281> |
| Citation label | Douze et al. (2024), Faiss |
| Review scope | Author paper sections on inverted files, graph-based search and compressed codes, with the official Faiss index documentation. |

## Mechanism

An inverted file uses coarse centroids to organize postings. Vector quantization can instead encode a vector using centroid IDs, including separate subspace codes in product quantization.

## Evidence

The index documentation distinguishes full-vector IVF postings, product-quantized postings, flat search, and HNSW graph search.

## Limits and failure modes

A routing centroid can coexist with full stored vectors. A quantized reconstruction and search over a subset of postings have separate error and cost budgets.

## Book chapters supported

- `virtual-context-abi`
- `rankfold-neuralfold-and-artifact-compression`

## Additional primary references

- <https://github.com/facebookresearch/faiss/wiki/Faiss-indexes/aeda38e6c323d6e3f0a207db875918f1185aa7bb>
