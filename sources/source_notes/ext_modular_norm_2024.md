# Source Note: Scalable Optimization in the Modular Norm

| Field | Value |
|---|---|
| Source ID | `ext_modular_norm_2024` |
| Ingestion date | 2026-07-21 |
| Source | Large et al., arXiv:2405.14813, https://arxiv.org/abs/2405.14813 |
| Ingestion basis | Primary architecture-recursive norm, scaling argument, update normalization, theoretical assumptions, and experiments reviewed. |

## Thesis and mechanism

The modular norm assigns natural input/output sensitivities to atomic modules
and composes them recursively into a norm for the full architecture. It can
normalize updates from a base optimizer so one learning rate is more
transferable across width and depth under the framework's assumptions.

## Evidence and limits

The paper supplies Lipschitz results for “well-behaved” module compositions and
source-reported transfer experiments. The architecture decomposition, module
norms, base optimizer, and assumptions remain identity-bearing. It does not
prove transfer to arbitrary recurrent, sparse, hybrid, or dynamically changing
substrates.

## Book use

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the architecture-aware geometry family and as an interface to
Replaceable Cognitive Substrates. A new substrate must declare its module
geometry and earn transfer; it cannot inherit the result by terminology.
