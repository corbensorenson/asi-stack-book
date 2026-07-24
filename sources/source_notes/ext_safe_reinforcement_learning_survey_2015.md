# Source Note: A Comprehensive Survey on Safe Reinforcement Learning

| Field | Value |
|---|---|
| Source ID | `ext_safe_reinforcement_learning_survey_2015` |
| Source title | A Comprehensive Survey on Safe Reinforcement Learning |
| Ingestion date | 2026-07-24 |
| Source version / URL | JMLR 16(42), https://www.jmlr.org/papers/v16/garcia15a.html |
| Citation label | García and Fernández (2015), Safe Reinforcement Learning Survey |
| Published / updated | 2015-04-27 / 2015-04-27 |
| DOI | not assigned in the inspected record |
| Ingestion basis | Primary JMLR abstract, metadata, and taxonomy inspected; no surveyed algorithm reproduced. |

## Thesis

Safe reinforcement learning changes either what is optimized or how exploration
is allowed. Safety during learning and safety during deployment are distinct
requirements.

## Mechanisms

- Modify optimality criteria with risk or safety factors.
- Constrain exploration using external knowledge, teacher policies, or risk
  metrics.
- Separate learning-time and deployment-time safety questions.

## Evidence

This is a peer-reviewed survey of then-current work. It supplies taxonomy and
comparators, not evidence that a particular physical agent is safe.

## Failure Modes

- Unsafe exploration before a policy becomes competent.
- A risk proxy that misses the actual hazard.
- Deployment constraints assumed from training-time behavior.
- Reward and safety constraints that become infeasible together.

## Book Chapters Supported

- `embodied-agency-real-time-control-and-physical-safety`
- `policy-optimization-and-learning-from-feedback`

## Claims To Add Or Update

- A control lease must specify both exploration and deployment authority.
- Safe fallback remains necessary when a learning constraint fails.

## Open Questions

- Which constraint and shield baselines are strong enough for the first
  embodied campaign?
- How should the system account for useful-task loss caused by safety filters?
