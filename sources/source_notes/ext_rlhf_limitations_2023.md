# Source Note: Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback

| Field | Value |
|---|---|
| Source ID | `ext_rlhf_limitations_2023` |
| Source title | Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2307.15217, https://arxiv.org/abs/2307.15217 |
| Citation label | Casper et al. (2023), Open Problems and Fundamental Limitations of RLHF |
| Published / updated | 2023-07-27 / 2023-09-11 |
| DOI | 10.48550/arXiv.2307.15217 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the policy-optimization literature queue; paper not vendored into this repository and no training result reproduced. |

## Thesis

This survey is useful as the policy chapter's external caution source: feedback learning has known open problems, so the ASI Stack must keep reward sources, evaluator limits, residuals, and governance gates explicit.

## Mechanisms

- Survey open problems and fundamental limitations of RLHF and related methods.
- Organize issues around human feedback quality, reward-model behavior, distribution shift, gaming, and oversight limits.
- Discuss techniques to understand, improve, and complement RLHF in practice.
- Support the book's rule that reward signals are not truth signals or governance grants.

## Evidence

- The source is a survey of limitations and mitigation directions. This repo has not independently verified every surveyed result.
- This repository has not reproduced the paper's experiments, training environment, datasets, reward models, evaluator setup, or benchmark results.
- Use this source as external literature for method-family taxonomy and risk framing, not as evidence that any ASI Stack policy has improved.

## Failure Modes

- Using RLHF as a blanket alignment label can hide unresolved evaluator, feedback, and reward-model risks.
- Mitigation taxonomies do not replace local reward-hacking probes or run records.
- External surveys can guide risk framing but should not be converted into deployed-system guarantees.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source-note RLHF limitation categories and reward-hacking probes. Do not use it as proof that any ASI Stack reward process is safe.
- Keep support state at `argument` unless later passage review, implemented experiments, proof artifacts, or accepted evidence transitions justify a narrower promotion.
- Record negative, inconclusive, or failed local training results if any future experiment is attempted.

## Open Questions

- Which minimal toy task, holdout, and reward-hacking probe would test this method family inside the ASI Stack without overclaiming?
- What evidence record should separate reward improvement from truth, authority preservation, and downstream task success?
- Which planner, router, VCM, execution, generation-mode, or reasoning-budget policy would be the first safe target for a small reproduction?
