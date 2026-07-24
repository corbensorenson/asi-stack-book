# Source Note: SOAP: Improving and Stabilizing Shampoo using Adam

| Field | Value |
|---|---|
| Source ID | `ext_soap_2024` |
| Ingestion date | 2026-07-21 |
| Source | Vyas et al., arXiv:2409.11321, https://arxiv.org/abs/2409.11321 |
| Ingestion basis | Primary Shampoo/Adafactor connection, SOAP update, preconditioning-frequency ablation, and language-model results reviewed. |

## Thesis

SOAP interprets Shampoo as adaptive optimization in a preconditioner eigenbasis
and runs Adam-like moments in that slowly changing basis. It continues updating
moments between eigendecompositions, aiming to retain useful curvature
information when the expensive basis refresh is less frequent.

## Mechanisms

The comparison unit must bind the preconditioned basis, moment updates,
basis-refresh cadence, numerical approximation, distribution, and checkpoint state.

## Evidence

The paper reports large-batch improvements over AdamW and Shampoo on 360M and
660M language-model pretraining. Preconditioning frequency remains an extra
hyperparameter; basis construction, state, communication, and hardware kernels
remain part of total cost.

## Failure Modes

Stale bases, expensive refresh, mismatched grafting, lost state, or uncounted
systems overhead can turn iteration gains into worse wall-clock performance.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the bridge between coordinate-adaptive and matrix-preconditioned
families. Report both iteration and wall-clock effects, and preserve the exact
basis-refresh and moment-state semantics in checkpoints.

## Claims To Add Or Update

- Use SOAP as a bridge between adaptive moments and matrix preconditioning.
- Report iteration, wall-clock, memory, communication, and resume behavior.

## Open Questions

- Which refresh cadence offers the best quality-adjusted lifecycle cost?
- How robust are basis and moment states to sharding, faults, and model transfer?
