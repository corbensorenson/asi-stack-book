# Source Note: Adam: A Method for Stochastic Optimization

| Field | Value |
|---|---|
| Source ID | `ext_adam_2015` |
| Ingestion date | 2026-07-21 |
| Source | Kingma and Ba, arXiv:1412.6980, https://arxiv.org/abs/1412.6980 |
| Ingestion basis | Primary abstract, algorithm, analysis, and experiment descriptions reviewed; no run reproduced. |

## Thesis

Adam combines exponential moving averages of the gradient and squared gradient,
corrects their initialization bias, and divides the first-moment estimate by the
square root of the second-moment estimate plus a stabilizer. The update is
coordinate-adaptive and invariant to diagonal rescaling of gradients under the
paper's formulation. Its state includes both moment tensors and the step count.

## Mechanisms

The comparison unit must bind moment equations, bias correction, epsilon
placement, precision, parameter groups, clipping, decay, and schedule.

## Evidence

The paper supplies online-convex analysis and source-reported experiments. That
does not establish universal convergence or superiority in nonconvex,
large-scale, mixed-precision model training. Epsilon placement, parameter
groups, decay semantics, precision, schedule, clipping, and implementation
version remain identity-bearing.

## Failure Modes

Implementation drift, weak tuning, mixed-precision instability, excessive state,
or a mismatched schedule can make an `Adam` arm incompetent or non-comparable.

## Book Chapters Supported

Use as the adaptive-moment baseline in `governed-model-training-distributed-optimization-and-scaling`.
Do not treat the paper's default hyperparameters as universally adequate or an
optimizer name as a complete training policy.

## Claims To Add Or Update

- Use Adam as an adaptive-moment baseline with exact policy identity.
- Do not infer universal convergence or superiority from the original paper.

## Open Questions

- Which Adam policy is the strongest matched baseline for each model family?
- How do state, communication, stability, and time-to-quality change with scale?
