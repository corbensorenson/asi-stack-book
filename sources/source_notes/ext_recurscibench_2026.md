# RecurSciBench: Benchmarking Recursive Self-Improvement in Data-Driven Scientific Research

| Field | Value |
|---|---|
| Source ID | `ext_recurscibench_2026` |
| Publication | Xu et al. (2026). [Primary source](https://arxiv.org/abs/2611.32508v1) |
| Review | November 27, 2026. [Selected source text](https://arxiv.org/html/2611.32508v1) |

## Thesis

Preserve per-task losses alongside overall transfer.

## Mechanisms

Freeze initial and evolved agent states and test transfer on separate scientific modeling tasks.

## Evidence

The four-system comparison reports variation across domains and individual regressions under positive overall gains.

## Failure Modes

Performance of a frozen successor on independent tasks measures transfer of the resulting agent. It leaves its ability to produce better future agents open.

## Book Chapters Supported

- `recursive-self-improvement-boundaries`

## Claims To Add Or Update

Use this source to frame the worked comparison in [recursive-self-improvement-boundaries](../../chapters/recursive-self-improvement-boundaries.qmd). The chapter core retains argument-level support.

## Open Questions

Which individual tasks regress even when mean performance improves?
