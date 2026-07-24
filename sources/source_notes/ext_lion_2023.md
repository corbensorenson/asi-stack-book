# Source Note: Symbolic Discovery of Optimization Algorithms

| Field | Value |
|---|---|
| Source ID | `ext_lion_2023` |
| Ingestion date | 2026-07-21 |
| Source | Chen et al., arXiv:2302.06675, https://arxiv.org/abs/2302.06675 |
| Ingestion basis | Primary optimizer-search method, Lion update, comparisons, scaling observations, and limitations reviewed. |

## Thesis

The paper casts optimizer discovery as symbolic program search and derives
Lion, a sign-based momentum optimizer. Lion retains one momentum state rather
than Adam's first and second moments, and its update magnitude is determined by
the sign operation rather than a coordinate-wise variance denominator.

## Mechanisms

The comparison unit must bind the discovered sign-based update, momentum
coefficients, decay, schedule, precision, and search-to-evaluation separation.

## Evidence

The source reports gains across several vision, language, and diffusion
settings, larger benefits at larger batches, a smaller appropriate learning
rate than Adam, and cases where differences are small or insignificant. Search
transfer and reported wins remain source- and budget-scoped.

## Failure Modes

Search leakage, unequal tuning, unstable sign updates, or failure to preserve
the exact discovered rule can turn a claimed Lion comparison into a different arm.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use both as a practical low-state family and as an example of optimizer search.
Any self-improving system must version the discovered rule and requalify it;
search provenance is not performance evidence.

## Claims To Add Or Update

- Treat Lion as both a low-state optimizer and an optimizer-search case study.
- Requalify a discovered rule under independent held-out evaluation.

## Open Questions

- Which advantages survive equal tuning, compute, and model-family transfer?
- How should optimizer-search provenance constrain recursive improvement?
