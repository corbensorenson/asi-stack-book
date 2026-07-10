# Source Note: S-GRPO: Early Exit via Reinforcement Learning in Reasoning Models

| Field | Value |
|---|---|
| Source ID | `ext_s_grpo_2025` |
| Source title | S-GRPO: Early Exit via Reinforcement Learning in Reasoning Models |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2505.07686, https://arxiv.org/abs/2505.07686 |
| Citation label | Dai et al. (2025), S-GRPO |
| Published / updated | 2025-05-12 / 2025-05-17 |
| DOI | 10.48550/arXiv.2505.07686 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

S-GRPO is useful for the book's reasoning-budget boundary: RL can be aimed at when to stop reasoning, but shorter reasoning is not automatically better reasoning.

## Mechanisms

- Identify excessive chain-of-thought redundancy as a reasoning-model failure mode in the source framing.
- Use reinforcement learning to encourage early exit or stopping behavior.
- Compare reasoning-length control against task performance in the source setting.
- Connect to ASI Stack reasoning-budget penalties and verifier-aware stop conditions.

## Evidence

- The source reports early-exit RL behavior. This repo has not reproduced S-GRPO or measured reasoning-budget tradeoffs.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Length penalties can suppress necessary verification or exploration.
- Early-exit reward can optimize terse traces rather than correct answers.
- Reasoning-budget policies need task-risk tiers, adequacy checks, and residual records.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `governed-deliberation-and-test-time-scaling` (Governed Deliberation and Test-Time Scaling)

## Claims To Add Or Update

- Use this note to source-note early-exit/reasoning-budget RL. Do not claim a local reasoning-budget policy exists.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.
- Use the source to ground stop-policy tradeoffs while preserving the boundary
  that early exit cannot erase required verification or residual ownership.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
