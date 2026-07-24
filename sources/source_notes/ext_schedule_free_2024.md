# Source Note: The Road Less Scheduled

| Field | Value |
|---|---|
| Source ID | `ext_schedule_free_2024` |
| Ingestion date | 2026-07-21 |
| Source | Defazio et al., arXiv:2405.15682, https://arxiv.org/abs/2405.15682 |
| Ingestion basis | Primary scheduling/averaging theory, algorithms, experiments, and evaluation-mode requirements reviewed. |

## Thesis

The paper unifies learning-rate scheduling and iterate averaging, then derives
schedule-free momentum and AdamW-like methods that do not require the stopping
step `T` to define a decay schedule. Multiple maintained iterates and the choice
of which is used for training or evaluation are part of the method.

## Mechanisms

The comparison unit must bind all averaging iterates, train/eval mode changes,
moment policy, warmup assumptions, decay, and checkpoint/resume semantics.

## Evidence

The source reports competitive results across convex and deep-learning tasks
and an AlgoPerf self-tuning result. “Schedule-free” does not mean
hyperparameter-free: base learning rate, momentum, warmup, weight decay,
evaluation iterate, and stopping remain consequential.

## Failure Modes

Lost averaging state, wrong evaluation mode, mismatched warmup, or a scheduler
hidden in the baseline can invalidate both resume and efficiency comparisons.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use to make scheduler state and evaluation mode first-class optimizer-policy
fields. A checkpoint that restores weights but loses the averaging iterates is
not a faithful schedule-free resume.

## Claims To Add Or Update

- Treat schedule-free state and evaluation mode as optimizer identity.
- Compare against strong scheduled and tuned baselines at matched quality.

## Open Questions

- Which workloads benefit once tuning and averaging-state cost are counted?
- Can exact resume preserve all iterates across topology and version changes?
