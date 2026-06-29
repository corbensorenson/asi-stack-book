# Source Note: Reinforcement Learning Under Moral Uncertainty

| Field | Value |
|---|---|
| Source ID | `ext_reinforcement_learning_moral_uncertainty_2020` |
| Source title | Reinforcement Learning Under Moral Uncertainty |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:2006.04734, https://arxiv.org/abs/2006.04734 |
| Citation label | Ecoffet and Lehman (2020), Reinforcement Learning Under Moral Uncertainty |
| Published / updated | 2020-06-08 / 2021-07-19 |
| DOI | 10.48550/arXiv.2006.04734 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the moral-uncertainty grounding queue; paper not vendored into this repository and no reinforcement-learning experiment reproduced. |

## Thesis

This source gives the value-conflict chapter an AI-specific moral-uncertainty baseline. It treats disagreement among moral theories as a problem for agent behavior, which maps to the book's warning that value conflict should not disappear into one reward function.

## Mechanisms

- Frame ethical agent behavior as action under disagreement among moral theories.
- Contrast training under one moral theory with acting under moral uncertainty.
- Provide a reinforcement-learning setting for exploring moral-uncertainty handling.
- Motivate explicit records for uncertainty, value axes, bounded decisions, and residual obligations.

## Evidence

- The source contributes AI-specific moral-uncertainty framing and experimental reinforcement-learning context.
- This repository has not reproduced its experiments, imported its environments, or validated ASI Stack value-conflict records against its results.
- Use it as external literature for moral-uncertainty positioning, not as evidence that the ASI Stack solves moral uncertainty.

## Failure Modes

- Treating an aggregation method or reward design as a solved moral theory.
- Hiding disagreement inside a scalar reward and losing dissent, stakeholder, or revisit information.
- Overgeneralizing from simple agent environments to high-stakes governed systems.

## Book Chapters Supported

- `moral-uncertainty-and-value-conflict` (Moral Uncertainty and Value Conflict)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to replace the value-conflict chapter's external-baseline exception with a source-noted moral-uncertainty comparator.
- Keep the ASI Stack value-conflict claim at `argument` support until record-preservation, review-quality, and runtime-policy evidence exist.
- Do not treat moral-uncertainty RL as evidence for the book's governance-rights or tribunal designs.

## Open Questions

- Which moral-uncertainty concepts should become fields on the value-conflict record?
- What test would show that a bounded decision preserves moral uncertainty rather than hiding it?
- How should reward-based moral-uncertainty methods relate to review, dissent, and authority narrowing?
