# Loop-Count Schedules in Looped Transformers: An Empirical Study

| Field | Value |
|---|---|
| Source ID | `ext_loop_schedule_2026` |
| Publication | Kolokolov (2026). [Source version](https://arxiv.org/abs/2611.29704v1) |

## Thesis

How a model is trained to spend its loops affects what happens when the inference depth changes.

## Mechanisms

The distribution of loop counts during training affects how a gated recurrent update acts at later inference depths.

## Evidence

In the fixed-depth setting the residual direction could converge even as loss diverged.

## Failure Modes

The November preprint studies a 46M–110M ladder on 2B tokens.

## Book Chapters Supported

- [Governed Deliberation and Test-Time Scaling](../../chapters/governed-deliberation-and-test-time-scaling.qmd)

## Claims To Add Or Update

External comparison under the existing chapter support state.

## Open Questions

Does this trade-off persist at matched quality, latency and memory on the intended workload?
