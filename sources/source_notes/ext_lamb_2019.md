# Source Note: Large Batch Optimization for Deep Learning

| Field | Value |
|---|---|
| Source ID | `ext_lamb_2019` |
| Ingestion date | 2026-07-21 |
| Source | You et al., arXiv:1904.00962, https://arxiv.org/abs/1904.00962 |
| Ingestion basis | Primary LAMB rule, LARS comparison, convergence scope, batch scaling, and BERT/ResNet reports reviewed. |

## Thesis

LAMB applies an Adam-like update and rescales it by a layer-wise trust ratio
derived from parameter and update norms. It targets regimes where very large
global batches make ordinary optimizer recipes difficult to scale.

## Mechanisms

The comparison unit must bind layerwise trust ratios, moment and decay policy,
batch construction, schedule, quality target, and hardware topology.

## Evidence

The source reports BERT target quality with a batch of 32,868 and a 76-minute
training time on a TPUv3 Pod, alongside other tasks. Those numbers are bound to
the exact model, quality target, implementation, hardware, batch arithmetic,
and tuning opportunity. Large batches can change data efficiency and critical
batch behavior even when wall time improves.

## Failure Modes

Large-batch speed can hide worse token efficiency, different quality targets,
weak baselines, unstable trust ratios, or hardware-specific advantage.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the layer-scaled/large-batch family representative and as a warning that
hardware time, optimizer steps, examples, tokens, and total compute must all be
reported together.

## Claims To Add Or Update

- Use LAMB as the layer-scaled large-batch comparator.
- Separate wall time, steps, examples, tokens, total compute, and final quality.

## Open Questions

- Where is the critical-batch boundary for each model and data regime?
- Do layerwise trust ratios help after matching batch, schedule, and tuning?
