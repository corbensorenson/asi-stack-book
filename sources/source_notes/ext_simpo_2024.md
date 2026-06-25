# Source Note: SimPO: Simple Preference Optimization with a Reference-Free Reward

| Field | Value |
|---|---|
| Source ID | `ext_simpo_2024` |
| Source title | SimPO: Simple Preference Optimization with a Reference-Free Reward |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2405.14734, https://arxiv.org/abs/2405.14734 |
| Citation label | Meng et al. (2024), SimPO |
| Published / updated | 2024-05-23 / 2024-11-01 |
| DOI | 10.48550/arXiv.2405.14734 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

SimPO is useful to compare reference-free preference optimization with DPO-style objectives, especially where average sequence log probability is treated as an implicit reward.

## Mechanisms

- Use offline preference data with a simpler objective than DPO-style reference-model formulations.
- Treat average sequence log probability as an implicit reward signal.
- Avoid a separate reference model in the method framing.
- Report preference-optimization comparisons in the source setting.

## Evidence

- The source reports SimPO evaluation results. This repo has not reproduced them or tested sequence-level reward effects locally.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Sequence-level reward framing can reward length, style, or likelihood artifacts if not controlled.
- Reference-free simplicity does not remove the need for holdouts, residuals, rollback, and reward-hacking probes.
- Preference wins do not directly imply truth, tool safety, or governed deployment readiness.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note simple reference-free preference optimization. Do not use it to claim local SimPO performance.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
