# Source Note: On the Convergence of Adam and Beyond

| Field | Value |
|---|---|
| Source ID | `ext_amsgrad_2018` |
| Ingestion date | 2026-07-21 |
| Source | Reddi, Kale, and Kumar, ICLR 2018, https://openreview.net/forum?id=ryQu7f-RZ |
| Ingestion basis | Primary paper's counterexample, AMSGrad algorithm, theorem assumptions, and empirical scope reviewed. |

## Thesis and mechanism

The paper constructs stochastic-convex settings in which the original Adam
update does not converge and identifies problematic effective learning-rate
behavior. AMSGrad retains the coordinate-wise maximum of past second-moment
estimates so its normalizer does not decrease in the same way.

## Evidence and limits

The counterexample establishes a real theoretical limitation under its stated
conditions. It is not evidence that every Adam implementation or practical run
fails, nor that AMSGrad wins on modern foundation-model training. The proof and
practical recipes use different scheduling assumptions in places, which the
book must keep visible.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as a failure/counterexample source and to teach why effective step-size
history belongs in optimizer identity. A failed Adam arm still requires a
competent implementation, tuning, and task-valid comparison before any broader
negative inference.
