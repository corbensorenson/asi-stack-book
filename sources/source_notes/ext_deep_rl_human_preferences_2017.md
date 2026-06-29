# Source Note: Deep Reinforcement Learning from Human Preferences

| Field | Value |
|---|---|
| Source ID | `ext_deep_rl_human_preferences_2017` |
| Source title | Deep Reinforcement Learning from Human Preferences |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:1706.03741, https://arxiv.org/abs/1706.03741 |
| Citation label | Christiano et al. (2017), Deep RL from Human Preferences |
| Published / updated | 2017-06-12 / 2023-02-17 |
| DOI | 10.48550/arXiv.1706.03741 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the human-intent and policy-optimization external-positioning queues; paper not vendored into this repository and no preference-learning experiment reproduced. |

## Thesis

Deep reinforcement learning from human preferences is an external comparator for communicating complex goals through preference comparisons. It helps the ASI Stack distinguish preference signals from explicit intent contracts: preferences can shape behavior, but they do not automatically define authority, stop conditions, or evidence requirements.

## Mechanisms

- Collect human preferences between pairs of trajectory segments.
- Train a reward model or feedback signal from preference comparisons.
- Use the learned signal to train reinforcement-learning policies.
- Evaluate behavior under the source paper's tasks and feedback budget.

## Evidence

- The source reports preference-learning experiments in Atari and simulated robot locomotion settings under its own setup.
- This repository has not reproduced the tasks, feedback collection, reward-model training, policy training, or evaluation results.
- Use this source as a comparator for preference communication and human-feedback learning, not as evidence that ASI Stack intent contracts or policy updates work.

## Failure Modes

- Preference comparisons can encode style, local satisfaction, bias, or task-specific reward proxies.
- Preference signals do not by themselves specify allowed means, authority ceilings, affected parties, publication scope, or stop conditions.
- A learned reward can be optimized beyond the context in which preferences were elicited.
- Human-feedback efficiency claims do not imply governance adequacy.

## Book Chapters Supported

- `human-intent-as-a-formal-input` (Human Intent as a Formal Input)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this source to position preference-learning as a neighboring approach for communicating complex goals.
- In the human-intent chapter, keep preference signals separate from explicit authorization and contract state.
- In the policy-optimization chapter, use it as historical feedback-learning context without claiming local reproduction.

## Open Questions

- Should preference signals enter the stack through the intent contract, evidence ledger, or policy-update record?
- What validator would prevent preference-derived reward from widening authority?
- Which preference-learning failure case best illustrates the need for explicit stop conditions and re-contract triggers?
