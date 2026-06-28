# Source Note: Dynabench: Rethinking Benchmarking in NLP

| Field | Value |
|---|---|
| Source ID | `ext_dynabench_2021` |
| Source title | Dynabench: Rethinking Benchmarking in NLP |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2104.14337, https://arxiv.org/abs/2104.14337 |
| Citation label | Kiela et al. (2021), Dynabench |
| Published / updated | 2021-04-07 / 2021-04-07 |
| DOI | 10.48550/arXiv.2104.14337 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the benchmark-science literature queue; platform code, tasks, model submissions, and benchmark results are not imported into this repository. |

## Thesis

Dynabench belongs in the benchmark, readiness, policy-update, and steward chapters as an external reference for dynamic, adversarial, human-and-model-in-the-loop benchmarking. It helps the ASI Stack state why static benchmark packets should age, mutate, and preserve residual failures rather than turning into permanent authority.

## Mechanisms

- Collect examples through interaction between humans and models.
- Use model failures to drive future data collection.
- Treat benchmark construction as an evolving process rather than a fixed test set.
- Record task-level evaluation through a platform workflow.

## Evidence

- The source describes a dynamic benchmarking platform and reports examples in its own NLP setting.
- This repository has not run Dynabench, imported tasks, submitted models, or reproduced benchmark outcomes.
- Use the source as external dynamic-benchmarking vocabulary, not as evidence for local benchmark ratchets.

## Failure Modes

- Dynamic benchmarks still need governance over task selection, annotator incentives, and stale-score handling.
- Human-in-the-loop adversarial data can overfit to visible model failures.
- A benchmark platform does not by itself prove readiness, policy safety, or artifact release fitness.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)

## Claims To Add Or Update

- Use this note to compare ASI Stack benchmark ratchets with dynamic adversarial benchmark evolution.
- Do not claim Dynabench adoption, local task mutation, benchmark score validity, or readiness evidence.
- Keep support state at `argument` until local dynamic benchmark records and evidence transitions exist.

## Open Questions

- What mutation record should preserve why a benchmark example was added?
- How should readiness gates expire scores after benchmark drift?
- Which steward action should block release when dynamic failures accumulate?
