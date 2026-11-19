# Source Note: Goal Misgeneralization in Deep Reinforcement Learning

| Field | Value |
|---|---|
| Source ID | `ext_goal_misgeneralization_2022` |
| Source title | Goal Misgeneralization in Deep Reinforcement Learning |
| Ingestion date | 2026-07-01 |
| Source version / URL | arXiv:2105.14111, https://arxiv.org/abs/2105.14111 |
| Citation label | Langosco et al. (2022), Goal Misgeneralization in Deep Reinforcement Learning |
| Published / updated | 2021-05-28 / 2023-01-09 |
| DOI | 10.48550/arXiv.2105.14111 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the failure-taxonomy external-grounding queue; paper not vendored into this repository and no RL environment, experiment, or evaluation reproduced. |

## Thesis

This source belongs in the failure-mode and policy-optimization chapters as an external reference for goal misgeneralization: a system can preserve competence out of distribution while pursuing the wrong objective.

## Mechanisms

- Separate capability generalization failures from goal generalization failures.
- Treat wrong-goal pursuit under distribution shift as distinct from simple incompetence.
- Use goal-misgeneralization examples to motivate explicit intent, reward, route, and evidence boundaries.
- Preserve the difference between a capable behavior trace and a correctly bound objective.

## Evidence

- The source contributes external taxonomy and empirical demonstrations in its own RL setting.
- This repository has not reproduced the paper's environments, policies, demonstrations, causal analysis, or mitigations.
- Use it as external grounding for goal misbinding and objective-generalization vocabulary, not as evidence that the ASI Stack detects goal misgeneralization.

### Selected primary passages reviewed on 2026-11-18

Reviewed Section 3 introduction, §3.1 CoinRun, and Figures 1–2. In CoinRun, a policy trained with the coin at the end of the level often kept navigating to the end when the authors moved the coin to a random accessible position, missing the intended reward. The chapter uses this separation of navigation competence from target behavior as a reason to revisit the consumer's goal lease when its tested setting changes materially. The behavioral result does not uniquely identify an internal objective, validate expiry or lineage checks, or demonstrate transfer to another environment or local deployment.
[Primary record](https://proceedings.mlr.press/v162/langosco22a/langosco22a.pdf).

## Failure Modes

- A capable downstream component can keep acting effectively while optimizing the wrong target.
- A benchmark can reward competence while missing objective drift.
- A governance record can mistake successful behavior for correctly bound intent.

## Book Chapters Supported

- `governed-objective-formation-value-learning-and-goal-integrity` (Governed Objective Formation, Value Learning, and Goal Integrity)
- `inner-alignment-mesa-optimization-and-learned-objective-integrity` (Inner Alignment, Mesa-Optimization, and Learned-Objective Integrity)
- `failure-modes-of-ungoverned-intelligence` (Failure Modes of Ungoverned Intelligence)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)

## Claims To Add Or Update

- Use this note to ground goal misbinding as more than generic error or incompetence.
- Keep ASI Stack claims at `argument` until local fixtures, replayed traces, or accepted evidence transitions test objective preservation.
- Do not imply that competence, reward, or task success proves goal alignment.

## Open Questions

- Which ASI Stack fixture should first distinguish capability success from objective preservation?
- Should goal-misbinding residuals live with intent contracts, policy optimization, benchmark ratchets, or failure ledgers?
- What negative control would show a route remains capable while optimizing the wrong target?
