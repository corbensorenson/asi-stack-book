# Source Note: Scalable Optimization in the Modular Norm

| Field | Value |
|---|---|
| Source ID | `ext_modular_norm_2024` |
| Ingestion date | 2026-07-21 |
| Source | Large et al., arXiv:2405.14813, https://arxiv.org/abs/2405.14813 |
| Ingestion basis | Primary architecture-recursive norm, scaling argument, update normalization, theoretical assumptions, and experiments reviewed. |

## Thesis

The modular norm assigns natural input/output sensitivities to atomic modules
and composes them recursively into a norm for the full architecture. It can
normalize updates from a base optimizer so one learning rate is more
transferable across width and depth under the framework's assumptions.

## Mechanisms

The comparison unit must bind module geometry, norm choice, update
normalization, parameterization, architecture, and transfer policy.

## Evidence

The paper supplies Lipschitz results for “well-behaved” module compositions and
source-reported transfer experiments. The architecture decomposition, module
norms, base optimizer, and assumptions remain identity-bearing. It does not
prove transfer to arbitrary recurrent, sparse, hybrid, or dynamically changing
substrates.

## Failure Modes

Misclassified modules, architecture-specific tuning, or inherited geometry
assumptions can create unstable updates or false transfer claims.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use as the architecture-aware geometry family and as an interface to
Replaceable Cognitive Substrates. A new substrate must declare its module
geometry and earn transfer; it cannot inherit the result by terminology.

## Claims To Add Or Update

- Treat modular norms as architecture-aware optimizer policy.
- Require each replaceable substrate to declare and qualify its module geometry.

## Open Questions

- Which geometry taxonomy transfers across attention, recurrence, convolution, and KANs?
- What diagnostics reveal a wrong module norm before costly training?
