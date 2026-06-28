# Source Note: Measuring Massive Multitask Language Understanding

| Field | Value |
|---|---|
| Source ID | `ext_mmlu_2020` |
| Source title | Measuring Massive Multitask Language Understanding |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2009.03300, https://arxiv.org/abs/2009.03300 |
| Citation label | Hendrycks et al. (2020), MMLU |
| Published / updated | 2020-09-07 / 2021-01-12 |
| DOI | 10.48550/arXiv.2009.03300 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the benchmark-science literature queue; benchmark not vendored into this repository and no model result reproduced. |

## Thesis

MMLU belongs in the benchmark-ratchet and evidence chapters as an external reference for broad multitask evaluation. It is useful precisely because it exposes both breadth and residual failure rather than proving general intelligence.

## Mechanisms

- Evaluate across many academic and professional tasks.
- Use task breadth to reveal uneven model performance.
- Compare model accuracy against random chance and expert-level targets.
- Treat wrong-answer awareness and subject-specific weakness as evaluation concerns.

## Evidence

- The source reports benchmark results for evaluated models in its setting.
- This repository has not run MMLU, imported the dataset, or reproduced any model score.
- Use it as external benchmark context, not as evidence of ASI Stack capability.

## Failure Modes

- A broad benchmark can become a single score that hides weak domains.
- Saturation or contamination can reduce evidential value.
- Benchmark improvement does not prove source grounding, authority compliance, or deployment readiness.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to ground broad benchmark vocabulary and residual reporting.
- Do not claim local MMLU scores.
- Keep support state at `argument` until benchmark records, commands, and results exist.

## Open Questions

- What would a benchmark-ratchet packet need before citing MMLU as local evidence?
- How should the book preserve per-domain failures rather than a single average?
- Which contamination checks would be required?
