# Source Note: k-means++: The Advantages of Careful Seeding

| Field | Value |
|---|---|
| Source ID | `ext_kmeans_plus_plus_2007` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://research.google/pubs/k-means-the-advantages-of-careful-seeding/> |
| Citation label | Arthur and Vassilvitskii (2007), k-means++ |
| Review scope | Author publication record and Bessa et al., Section 4.1 and Appendix G. |

## Thesis

Distance-weighted seeding gives an expected objective guarantee for the initial centers.

## Mechanisms

After the first seed, sample each next center with probability proportional to squared distance from the closest seed. Lloyd updates can then refine the centers.

## Evidence

Theorem 1.1 bounds the expected initial squared-distance cost by 8(ln k + 2) times the optimal cost. It averages over random initialization. [Authors’ paper](https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf) The e-means comparison distinguishes original and greedy k-means++.

## Failure Modes

Seeding adds setup cost and leaves the number of centers and the choice of distance to the caller.

## Book Chapters Supported

- `virtual-context-abi` — [Clustering the retrieval index](../../chapters/virtual-context-abi.qmd#clustering-the-retrieval-index)

## Additional primary references

- <https://arxiv.org/html/2611.09501v1>

## Claims To Add Or Update

Include careful seeding as a baseline and count its cost separately from later Lloyd iterations.

## Open Questions

At the target corpus size, does the reduction in iteration cost pay for initialization?
