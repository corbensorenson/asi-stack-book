# Source Note: Holistic Evaluation of Language Models

| Field | Value |
|---|---|
| Source ID | `ext_helm_2022` |
| Source title | Holistic Evaluation of Language Models |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2211.09110, https://arxiv.org/abs/2211.09110 |
| Citation label | Liang et al. (2022), HELM |
| Published / updated | 2022-11-16 / 2023-10-01 |
| DOI | 10.48550/arXiv.2211.09110 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the benchmark-science literature queue; benchmark not vendored into this repository and no model result reproduced. |

## Thesis

HELM belongs in the benchmark and living-book methodology chapters as an external reference for multi-scenario, multi-metric, transparent, living evaluation. It matches the book's preference for evidence surfaces that reveal tradeoffs and missing coverage.

## Mechanisms

- Taxonomize scenarios and metrics.
- Evaluate models across multiple desiderata instead of accuracy alone.
- Disclose underrepresented scenarios and missing metrics.
- Release raw prompts/completions and maintain a modular evaluation toolkit in the source setting.

## Evidence

- The source reports standardized evaluations across many models and scenarios.
- This repository has not run HELM, imported prompts/completions, or reproduced any model result.
- Use it as external benchmark-governance context, not as evidence that the ASI Stack has a living benchmark.

## Failure Modes

- Even holistic benchmarks can omit important scenarios.
- Multi-metric reports can still be reduced to a leaderboard.
- Transparency artifacts do not replace independent review or deployment gates.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `living-book-methodology` (Living Book Methodology)

## Claims To Add Or Update

- Use this note to source multi-metric evaluation and living-benchmark vocabulary.
- Do not claim HELM reproduction or local evaluation coverage.
- Keep support state at `argument` until local benchmark artifacts and review records exist.

## Open Questions

- What minimum metric set should an ASI Stack benchmark packet require?
- How should missing coverage be represented in release records?
- Which raw outputs need preservation for future audit?
