# Source Note: Decoupled Weight Decay Regularization

| Field | Value |
|---|---|
| Source ID | `ext_adamw_2019` |
| Ingestion date | 2026-07-21 |
| Source | Loshchilov and Hutter, ICLR 2019, https://openreview.net/forum?id=Bkg6RiCqY7 |
| Ingestion basis | Primary algorithms, weight-decay/L2 distinction, tuning study, and generalization experiments reviewed. |

## Thesis

For adaptive methods, adding an L2 penalty to the loss is not equivalent to
multiplicatively shrinking parameters. AdamW decouples weight decay from the
adaptive gradient update, making decay and the gradient transformation distinct
operations and reducing one important hyperparameter coupling in the reported
settings.

## Mechanisms

The comparison unit must distinguish decoupled weight decay from an L2 term and
record exclusions, scaling, schedule, warmup, clipping, epsilon, and precision.

## Evidence

The source reports broader useful tuning regions and competitive generalization
in its studied vision settings. It does not prove that AdamW is universally
best. Parameter exclusions, decay scaling, schedule, warmup, clipping, epsilon,
precision, and parameterization materially alter the actual policy.

## Failure Modes

Coupled regularization disguised as AdamW, inconsistent parameter exclusions,
or unequal tuning budgets can invalidate both positive and negative comparisons.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use AdamW as the modern reference baseline, not a straw baseline. Every
comparison must record exact decay semantics and parameter groups; the label
`AdamW` alone is insufficient.

## Claims To Add Or Update

- Treat AdamW as the modern reference baseline when competently tuned.
- Keep decay semantics and parameter groups inside optimizer identity.

## Open Questions

- Which decay and schedule policies transfer across model size and modality?
- When does a competing optimizer win after equal tuning and lifecycle cost?
