# Source Note: k-means++: The Advantages of Careful Seeding

| Field | Value |
|---|---|
| Source ID | `ext_kmeans_plus_plus_2007` |
| Ingestion date | 2026-11-13 |
| Primary source | <https://research.google/pubs/k-means-the-advantages-of-careful-seeding/> |
| Citation label | Arthur and Vassilvitskii (2007), k-means++ |
| Review scope | Author publication record and Bessa et al., Section 4.1 and Appendix G. |

## Mechanism

After the first seed, sample each next center with probability proportional to squared distance from the closest seed. Lloyd updates can then refine the centers.

## Evidence

The source studies careful seeding for the squared-distance objective. The e-means comparison distinguishes original and greedy k-means++.

## Limits and failure modes

Seeding adds setup cost and leaves the number of centers and the choice of distance to the caller.

## Book chapters supported

- `virtual-context-abi`

## Additional primary references

- <https://arxiv.org/html/2611.09501v1>
