# Source Note: KTO: Model Alignment as Prospect Theoretic Optimization

| Field | Value |
|---|---|
| Source ID | `ext_kto_2024` |
| Source title | KTO: Model Alignment as Prospect Theoretic Optimization |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2402.01306, https://arxiv.org/abs/2402.01306 |
| Citation label | Ethayarajh et al. (2024), KTO |
| Published / updated | 2024-02-02 / 2024-11-19 |
| DOI | 10.48550/arXiv.2402.01306 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

KTO is useful because it treats alignment losses as human-aware objectives shaped by prospect-theory-like asymmetries, which fits the book's warning that reward signals encode human and institutional assumptions.

## Mechanisms

- Frame alignment objectives through prospect-theory-inspired human-aware losses.
- Use desirable and undesirable examples rather than requiring only paired preference comparisons.
- Compare loss families that encode asymmetric human valuation of gains and losses.
- Treat objective design itself as an assumption-bearing artifact.

## Evidence

- The source reports KTO method comparisons. This repo has not trained KTO, audited data assumptions, or validated prospect-theory fit for ASI Stack tasks.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Human-aware losses can encode the wrong human model or amplify dataset bias.
- Loss asymmetry does not make a reward signal true, safe, or governance-valid.
- Single-label desirable/undesirable data can be cheaper but less diagnostic than richer preference or evidence records.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note human-aware loss and binary-feedback alignment vocabulary. Do not use it as evidence that the stack has solved human preference modeling.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
