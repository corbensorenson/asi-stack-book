# Source Note: CodeBLEU: a Method for Automatic Evaluation of Code Synthesis

| Field | Value |
|---|---|
| Source ID | `ext_codebleu_2020` |
| Source title | CodeBLEU: a Method for Automatic Evaluation of Code Synthesis |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2009.10297, https://arxiv.org/abs/2009.10297 |
| Citation label | Ren et al. (2020), CodeBLEU |
| Published / updated | 2020-09-22 / 2020-09-27 |
| DOI | 10.48550/arXiv.2009.10297 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the artifact-utility and benchmark-science literature queue; evaluator code, datasets, and metric results are not imported into this repository. |

## Thesis

CodeBLEU belongs in the benchmark, compression, steward, and prototype chapters as an external reference for artifact-quality metrics that go beyond surface string overlap. It helps the ASI Stack state that generated or compressed code-like artifacts need syntax, data-flow, semantic, and execution-aware checks before quality claims move.

## Mechanisms

- Combine n-gram overlap with code-specific syntax matching.
- Include data-flow matching as a program-structure signal.
- Compare generated code against references with code-aware evaluation components.
- Use the metric as an evaluation aid rather than a substitute for task execution.

## Evidence

- The source reports CodeBLEU evaluation behavior in its own code-synthesis setting.
- This repository has not imported CodeBLEU, run it on ASI Stack artifacts, or compared it with execution results.
- Use the source as external artifact-metric vocabulary, not as evidence that any local artifact is correct.

## Failure Modes

- Metric agreement can miss semantic failure, security risk, or authority violation.
- Reference-based metrics can reward imitation rather than useful behavior.
- Code-quality metrics can become Goodhart targets if they are treated as release authority.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `prototype-roadmap` (Prototype Roadmap)

## Claims To Add Or Update

- Use this note to compare artifact utility metrics with executable tests, regression checks, and steward approval.
- Do not claim local CodeBLEU evaluation, code-synthesis quality, or release fitness.
- Keep support state at `argument` until local metric runs and execution/regression checks exist.

## Open Questions

- Which artifact classes need code-aware metrics before release?
- How should metric receipts link to executable tests and human review?
- What anti-Goodhart guard prevents a steward from promoting a metric-only improvement?
