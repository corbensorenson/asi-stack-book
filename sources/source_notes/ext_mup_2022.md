# Source Note: Tensor Programs V

| Field | Value |
|---|---|
| Source ID | `ext_mup_2022` |
| Ingestion date | 2026-07-21 |
| Source | Yang et al., arXiv:2203.03466, https://arxiv.org/abs/2203.03466 |
| Ingestion basis | Primary maximal-update parameterization, muTransfer protocol, Transformer/ResNet experiments, and transfer boundaries reviewed. |

## Thesis

Maximal Update Parametrization prescribes width-dependent parameter and update
scalings intended to preserve feature-learning dynamics as width changes.
muTransfer tunes selected hyperparameters on a smaller proxy model expressed in
that parameterization and transfers them to a wider target.

## Mechanisms

The comparison unit must bind base shape, width mapping, parameter
multipliers, initialization, learning rates, and optimizer policy together.

## Evidence

The paper reports substantial tuning savings and competitive BERT/GPT settings.
The result depends on the prescribed parameterization and studied transfer
axis. It does not establish arbitrary transfer across depth, duration, data,
architecture, optimizer family, or objective.

## Failure Modes

Incorrect parameter classes, hidden retuning, or changing architecture/data can
break transfer while leaving the run mislabeled as muP.

## Book Chapters Supported

Primary chapter: `governed-model-training-distributed-optimization-and-scaling`.

Use to separate optimizer choice from parameterization and to require a
prospective transfer axis. Standard parameterization versus muP is itself an
experimental arm, not an invisible implementation detail.

## Claims To Add Or Update

- Make parameterization a first-class training-policy axis.
- Do not attribute transferred hyperparameters to the optimizer alone.

## Open Questions

- Which tuning transfers survive changes in depth, modality, and architecture?
- How should a run receipt prove correct base-to-target parameter mapping?
