# Source Note: Proximal Policy Optimization Algorithms

| Field | Value |
|---|---|
| Source ID | `ext_ppo_2017` |
| Source title | Proximal Policy Optimization Algorithms |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:1707.06347, https://arxiv.org/abs/1707.06347 |
| Citation label | Schulman et al. (2017), Proximal Policy Optimization Algorithms |
| Published / updated | 2017-07-20 / 2017-08-28 |
| DOI | 10.48550/arXiv.1707.06347 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

PPO belongs in the book as the standard proximal online-RL baseline for update constraints: it keeps repeated minibatch updates simple enough to run while trying to preserve some trust-region-like discipline.

## Mechanisms

- Alternate environment interaction with optimization of a surrogate objective.
- Enable multiple epochs of minibatch updates from sampled data.
- Use proximal constraints as a practical alternative to heavier trust-region machinery.
- Report comparisons on simulated locomotion and Atari-style benchmarks in the source setting.

## Evidence

- The source reports empirical PPO performance and frames PPO as simpler and more sample-efficient than prior online policy-gradient baselines in its evaluated tasks.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- A proximal objective is still only as meaningful as the reward and evaluation environment.
- PPO tuning, critic behavior, and rollout distribution can dominate apparent improvement.
- PPO-like updates can optimize style, latency, or reward artifacts unless governance and verifier boundaries are explicit.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note PPO-style online updates and update-constraint vocabulary. Do not treat PPO as a governance grant or proof of alignment.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
