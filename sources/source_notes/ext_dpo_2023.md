# Source Note: Direct Preference Optimization: Your Language Model is Secretly a Reward Model

| Field | Value |
|---|---|
| Source ID | `ext_dpo_2023` |
| Source title | Direct Preference Optimization: Your Language Model is Secretly a Reward Model |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2305.18290, https://arxiv.org/abs/2305.18290 |
| Citation label | Rafailov et al. (2023), Direct Preference Optimization |
| Published / updated | 2023-05-29 / 2024-07-29 |
| DOI | 10.48550/arXiv.2305.18290 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

DPO is useful to the book as the cleanest offline preference-optimization comparison point: preferences can train behavior without running an explicit online reward-model RL loop.

## Mechanisms

- Use pairwise preference data over model generations.
- Reparameterize preference optimization so the language model can be trained directly against preference pairs.
- Avoid a separately trained reward model and online policy-optimization loop in the basic method framing.
- Compare preference optimization to RLHF-style pipelines in the source setting.

## Evidence

- The paper reports experimental preference-optimization results. This repository has not trained a DPO model or inspected preference datasets.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Offline preferences can encode shallow style, annotator bias, or distribution-specific artifacts.
- Static preference optimization does not automatically solve truthfulness, tool safety, or governance authority.
- Preference data quality and holdout design determine how far any support can travel.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note offline preference-optimization vocabulary. Do not use it to claim that ASI Stack policies have been preference-trained.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
