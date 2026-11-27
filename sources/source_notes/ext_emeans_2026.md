# Source Note: e-means: outperforming k-means (in one-tenth the epochs)

| Field | Value |
|---|---|
| Source ID | `ext_emeans_2026` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://arxiv.org/html/2611.09501v1> |
| Citation label | Bessa et al. (2026), e-means |
| Review scope | Sections 2–4 and Appendices C, H, J, L and M, plus the Faiss training-label and timing documentation. |

## Thesis

A running estimate of center statistics can reduce the fitting work needed for a fixed-k index.

## Mechanisms

EMA of per-center batch sums and counts fits the standard fixed-k squared-distance objective. Cosine annealing, empirical batch and step defaults, donor splitting, and finalization shape the finite-budget recipe.

## Evidence

Table 4 reports 1.4–2.6 epochs and 9.5–45.5× fitting speed against Flash-KMeans at 25 iterations on the tested H100 setups. The billion-vector cells use eight GPUs and one seed per configuration. Appendix L compares IVF Recall@10 at fixed search selectivities. Section 3.4 and Appendix M use approximate centroid assignment at extreme scale.

## Failure Modes

The warm fitting protocol excludes loading, initial-center selection, warm-up and scoring. Default scaling fits are weaker for very small or low-dimensional datasets. Training labels may predate the final centers. Retrieval recall in a vector benchmark leaves downstream evidence delivery and semantic adequacy open.

## Book Chapters Supported

- `virtual-context-abi` — [Clustering the retrieval index](../../chapters/virtual-context-abi.qmd#clustering-the-retrieval-index)
- `rankfold-neuralfold-and-artifact-compression` — [Count the vector codebook and its reconstruction error](../../chapters/rankfold-neuralfold-and-artifact-compression.qmd#vector-codebook-cost)

## Additional primary references

- <https://github.com/facebookresearch/faiss/blob/main/contrib/e_means/README.md>
- <https://github.com/facebookresearch/faiss/blob/main/benchs/e_means/README.md>

## Claims To Add Or Update

Charge initialization and final assignment when estimating total rebuild time, then test retrieval with the final centers.

## Open Questions

Does the faster fit preserve evidence recall at the service's actual search budget?
