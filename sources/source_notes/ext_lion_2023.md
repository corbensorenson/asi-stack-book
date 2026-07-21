# Source Note: Symbolic Discovery of Optimization Algorithms

| Field | Value |
|---|---|
| Source ID | `ext_lion_2023` |
| Ingestion date | 2026-07-21 |
| Source | Chen et al., arXiv:2302.06675, https://arxiv.org/abs/2302.06675 |
| Ingestion basis | Primary optimizer-search method, Lion update, comparisons, scaling observations, and limitations reviewed. |

## Thesis and mechanism

The paper casts optimizer discovery as symbolic program search and derives
Lion, a sign-based momentum optimizer. Lion retains one momentum state rather
than Adam's first and second moments, and its update magnitude is determined by
the sign operation rather than a coordinate-wise variance denominator.

## Evidence and limits

The source reports gains across several vision, language, and diffusion
settings, larger benefits at larger batches, a smaller appropriate learning
rate than Adam, and cases where differences are small or insignificant. Search
transfer and reported wins remain source- and budget-scoped.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use both as a practical low-state family and as an example of optimizer search.
Any self-improving system must version the discovered rule and requalify it;
search provenance is not performance evidence.
