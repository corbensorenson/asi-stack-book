# Source Note: Cooperative Inverse Reinforcement Learning

| Field | Value |
|---|---|
| Source ID | `ext_cooperative_inverse_rl_2016` |
| Source title | Cooperative Inverse Reinforcement Learning |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:1606.03137, https://arxiv.org/abs/1606.03137 |
| Citation label | Hadfield-Menell et al. (2016), Cooperative Inverse Reinforcement Learning |
| Published / updated | 2016-06-09 / 2024-02-17 |
| DOI | 10.48550/arXiv.1606.03137 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the human-intent external-positioning queue; paper not vendored into this repository and no CIRL algorithm or experiment reproduced. |

## Thesis

Cooperative inverse reinforcement learning is an external comparator for formalizing alignment as a cooperative setting where the system is uncertain about the human objective. It helps the human-intent chapter distinguish explicit intent contracts from broader preference or value-inference problems.

## Mechanisms

- Model a human and a robot as cooperating under partial information.
- Treat the human reward function as unknown to the robot.
- Derive value-alignment behavior from active learning, teaching, and communicative action.
- Reduce the formal setup to a POMDP in the source framing.

## Evidence

- The source provides formal framing and reported algorithmic analysis under its own assumptions.
- This repository has not implemented CIRL, solved a CIRL game, reproduced experiments, or validated policy behavior.
- Use this source as an external baseline for objective uncertainty and cooperative intent inference, not as support for ASI Stack intent-contract execution.

## Failure Modes

- Inferring a reward function is not the same as preserving an authorized contract.
- Human behavior may be noisy, strategic, mistaken, conflicted, or under-informed.
- A cooperative formal model does not by itself capture tool permissions, stop conditions, publication authority, or evidence duties.
- Value-inference claims can be overread as permission to act without explicit approval.

## Book Chapters Supported

- Proposed: `governed-objective-formation-value-learning-and-goal-integrity`
- `human-intent-as-a-formal-input` (Human Intent as a Formal Input)

## Claims To Add Or Update

- Use CIRL to position human intent as partly uncertain and cooperative rather than directly observable from text.
- Keep ASI Stack intent contracts framed as a governance surface that can preserve ambiguity and require re-contracting.
- Do not claim CIRL implementation, value-alignment solution, or human-reward inference evidence.

## Open Questions

- Which intent-contract states should represent uncertainty about the human's true objective?
- How should an intent contract record the difference between inferred preference and explicit authorization?
- What negative-control scenario should block a reward-inference route from becoming execution authority?
