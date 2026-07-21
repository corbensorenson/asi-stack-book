# Source Note: Decoupled Weight Decay Regularization

| Field | Value |
|---|---|
| Source ID | `ext_adamw_2019` |
| Ingestion date | 2026-07-21 |
| Source | Loshchilov and Hutter, ICLR 2019, https://openreview.net/forum?id=Bkg6RiCqY7 |
| Ingestion basis | Primary algorithms, weight-decay/L2 distinction, tuning study, and generalization experiments reviewed. |

## Thesis and mechanism

For adaptive methods, adding an L2 penalty to the loss is not equivalent to
multiplicatively shrinking parameters. AdamW decouples weight decay from the
adaptive gradient update, making decay and the gradient transformation distinct
operations and reducing one important hyperparameter coupling in the reported
settings.

## Evidence and limits

The source reports broader useful tuning regions and competitive generalization
in its studied vision settings. It does not prove that AdamW is universally
best. Parameter exclusions, decay scaling, schedule, warmup, clipping, epsilon,
precision, and parameterization materially alter the actual policy.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use AdamW as the modern reference baseline, not a straw baseline. Every
comparison must record exact decay semantics and parameter groups; the label
`AdamW` alone is insufficient.
