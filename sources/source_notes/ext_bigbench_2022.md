# Source Note: Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models

| Field | Value |
|---|---|
| Source ID | `ext_bigbench_2022` |
| Source title | Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2206.04615, https://arxiv.org/abs/2206.04615 |
| Citation label | Srivastava et al. (2022), BIG-bench |
| Published / updated | 2022-06-09 / 2023-06-12 |
| DOI | 10.48550/arXiv.2206.04615 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the benchmark-science literature queue; benchmark not vendored into this repository and no model result reproduced. |

## Thesis

BIG-bench belongs in the benchmark and readiness chapters as an external reference for broad, community-contributed capability evaluation and scale-sensitive behavior. It reinforces why benchmark ratchets need residuals, baselines, and anti-Goodhart boundaries.

## Mechanisms

- Use a large set of diverse tasks contributed by many authors.
- Evaluate models across scale, architecture classes, and task types.
- Include human-rater baselines for comparison.
- Track calibration, scale trends, brittle metrics, and social-bias behavior.

## Evidence

- The source reports model behavior on BIG-bench tasks in its setting.
- This repository has not run BIG-bench, imported tasks, or reproduced any score.
- Use it as external benchmark-science context, not as evidence for local capability or efficiency claims.

## Failure Modes

- Broad task suites can still underrepresent real deployment risk.
- Breakthrough-looking behavior can be metric-sensitive.
- Social-bias or calibration residuals can be hidden by aggregate capability scores.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)

## Claims To Add Or Update

- Use this note to source benchmark breadth, human baseline, and scale-trend vocabulary.
- Do not claim BIG-bench reproduction or ASI Stack benchmark performance.
- Keep support state at `argument` unless local run records and evidence transitions exist.

## Open Questions

- Which benchmark ratchet should preserve human baseline and calibration residuals?
- How should scale-trend claims be bounded in the book?
- What hidden-test or contamination policy should future benchmark packets require?
