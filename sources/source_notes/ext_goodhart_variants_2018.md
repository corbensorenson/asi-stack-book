# Source Note: Categorizing Variants of Goodhart's Law

| Field | Value |
|---|---|
| Source ID | `ext_goodhart_variants_2018` |
| Source title | Categorizing Variants of Goodhart's Law |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:1803.04585, https://arxiv.org/abs/1803.04585 |
| Citation label | Manheim and Garrabrant (2018), Goodhart Variants |
| Published / updated | 2018-03-13 / 2019-02-24 |
| DOI | 10.48550/arXiv.1803.04585 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the anti-Goodhart and metric-failure literature queue; no formal model, taxonomy implementation, or benchmark audit is imported into this repository. |

## Thesis

The Goodhart variants paper belongs in the benchmark, policy-optimization, steward, and evidence-state chapters as an external taxonomy for metric failure. It helps the ASI Stack keep regressive, extremal, causal, and adversarial metric failures separate when designing benchmark ratchets and policy update gates.

## Mechanisms

- Distinguish several ways proxy metrics can stop tracking the target after optimization.
- Separate distributional, causal, and adversarial sources of proxy failure.
- Treat metric design and selection pressure as a system-risk problem.
- Provide vocabulary for diagnosing why a benchmark or reward signal became unsafe to optimize.

## Evidence

- The source provides a taxonomy and examples in its own theoretical scope.
- This repository has not implemented the taxonomy, audited benchmark ratchets with it, or produced evaluator-gaming results.
- Use the source as external anti-Goodhart vocabulary, not as evidence that ASI Stack benchmarks resist metric gaming.

## Failure Modes

- A metric can fail because the selected examples move to extremes.
- A proxy can fail because optimization changes the causal relation between proxy and target.
- An optimizer or evaluator can exploit the proxy rather than improve the intended property.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)

## Claims To Add Or Update

- Use this note to classify benchmark and reward failures by Goodhart variant instead of treating all metric drift as one risk.
- Do not claim anti-Goodhart protection, evaluator-gaming resistance, or benchmark validity without local checks.
- Keep support state at `argument` until local benchmark-ratchet audits or accepted evidence transitions exist.

## Open Questions

- Which Goodhart variant should each benchmark-ratchet fixture detect first?
- How should policy updates record proxy-target divergence?
- What steward action should trigger when an improvement is metric-only but residuals worsen?
