# Source Note: ORPO: Monolithic Preference Optimization without Reference Model

| Field | Value |
|---|---|
| Source ID | `ext_orpo_2024` |
| Source title | ORPO: Monolithic Preference Optimization without Reference Model |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2403.07691, https://arxiv.org/abs/2403.07691 |
| Citation label | Hong et al. (2024), ORPO |
| Published / updated | 2024-03-12 / 2024-03-14 |
| DOI | 10.48550/arXiv.2403.07691 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

ORPO is useful as a reference-model-free preference-optimization comparison point: it pushes the book to separate preference data, reference-model dependence, and supervised fine-tuning assumptions.

## Mechanisms

- Treat supervised fine-tuning and preference alignment as a monolithic optimization path.
- Penalize disfavored generation styles while strengthening preferred outputs.
- Avoid a separate reference model in the method framing.
- Evaluate preference alignment under the source paper's language-model settings.

## Evidence

- The paper reports method results for ORPO. This repo has not reproduced ORPO training or compared it with local preference baselines.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Reference-free optimization can still inherit preference-data bias and reward misspecification.
- Combining SFT and preference terms can make attribution of improvements harder.
- A method can improve benchmark preference win rates without satisfying governance or truth constraints.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note reference-free offline preference optimization. Do not use it to claim local alignment improvement.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
