# Source Note: Model evaluation for extreme risks

| Field | Value |
|---|---|
| Source ID | `ext_model_evaluation_extreme_risks_2023` |
| Source title | Model evaluation for extreme risks |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2305.15324, https://arxiv.org/abs/2305.15324 |
| Citation label | Shevlane et al. (2023), Model evaluation for extreme risks |
| Published / updated | 2023-05-24 / 2023-09-22 |
| DOI | 10.48550/arXiv.2305.15324 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the governance/evals literature queue; paper not vendored into this repository and no evaluation reproduced. |

## Thesis

This source belongs in the benchmark and readiness chapters as the external reference for evaluating dangerous capabilities and alignment-relevant failures before deployment decisions.

## Mechanisms

- Separate capability evaluations from alignment evaluations.
- Treat extreme-risk evaluation as decision support for deployment and security controls.
- Connect evaluation results to governance actions, not merely score reporting.
- Motivate residual escrow when evaluations are incomplete, inconclusive, or narrowly scoped.

## Evidence

- The source contributes external governance/evaluation framing.
- This repository has not reproduced any model evaluation, eval suite, threshold, or deployment decision from the paper.
- Use it to frame readiness gates and benchmark ratchets, not as evidence that the book's evaluations exist or are sufficient.

## Failure Modes

- Treating an evaluation checklist as proof of safety.
- Overgeneralizing benchmark performance to deployment readiness.
- Hiding failed, inconclusive, or out-of-scope evals from the release record.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `recursive-self-improvement-boundaries` (Recursive Self-Improvement Boundaries)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to compare the ASI Stack's readiness gates and benchmark records against external model-evaluation practice.
- Do not claim that any ASI Stack extreme-risk evaluation has been run.
- Keep support state at `argument` unless future eval artifacts and accepted transitions justify more.

## Open Questions

- Which dangerous-capability and alignment-failure checks belong in the first ASI Stack evaluation packet?
- How should release records represent inconclusive evals?
- What evaluator independence standard should be required before deployment claims move?
