# Source Note: ZeRO: Memory Optimizations Toward Training Trillion Parameter Models

| Field | Value |
|---|---|
| Source ID | `ext_zero_optimizer_2019` |
| Source title | ZeRO: Memory Optimizations Toward Training Trillion Parameter Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:1910.02054v3, https://arxiv.org/abs/1910.02054 |
| Citation label | Rajbhandari et al. (2020), ZeRO |
| Published / updated | 2019-10-04 / 2020-05-13 |
| DOI | 10.1109/SC41405.2020.00024 |
| Ingestion basis | Primary paper reviewed, especially Sections 2--6; no implementation or reported result reproduced. |

## Thesis

Large-model memory is dominated not only by parameters but by optimizer state,
gradients, activations, fragmentation, and temporary buffers. ZeRO partitions
these state families across data-parallel ranks to reduce redundancy while
retaining data-parallel semantics.

## Mechanisms

- Progressive partitioning of optimizer states, gradients, and parameters.
- Partitioned activation checkpointing and explicit residual-state management.
- Mixed-precision accounting that distinguishes lower-precision parameters
  from FP32 master parameters, moments, and variance state.
- Communication-volume and memory analyses for alternative sharding stages.

## Evidence

The paper reports large memory reductions and scaling results across hundreds
of GPUs. Those figures are source-reported and configuration-dependent. The
paper is used here to enumerate state and compare a sharded design, not to claim
local scale or superiority.

## Failure Modes

- Checkpointing only weights while omitting partitioned optimizer or gradient
  state required for faithful continuation.
- Calling sharding transparent while topology-specific identities and
  collective assumptions are lost.
- Treating activation recomputation and persistent recovery checkpoints as the
  same mechanism.
- Counting theoretical capacity as a successfully trained model.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- Boundary context: `model-weight-custody-and-hardware-roots-of-trust`

## Claims To Add Or Update

- Make parameter, optimizer, gradient, scaler, and activation policies distinct
  run-manifest fields.
- Require checkpoint readers to prove shard completeness and canonical
  reconstruction or reject the resume.

## Open Questions

- Which transient states must be captured for trajectory equivalence rather
  than only eventual convergence?
- How should checkpoint authority change when topology or sharding degree
  changes?
