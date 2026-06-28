# Source Note: Investigating Data Contamination in Modern Benchmarks for Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_benchmark_contamination_2023` |
| Source title | Investigating Data Contamination in Modern Benchmarks for Large Language Models |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2311.09783, https://arxiv.org/abs/2311.09783 |
| Citation label | Deng et al. (2023), Benchmark Contamination |
| Published / updated | 2023-11-16 / 2024-04-03 |
| DOI | 10.48550/arXiv.2311.09783 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the benchmark-contamination literature queue; detection method, datasets, prompts, and findings are not imported into this repository. |

## Thesis

This source belongs in the benchmark, evidence-state, readiness, and living-method chapters as an external reference for contamination pressure in modern LLM benchmarks. It helps the ASI Stack treat benchmark score provenance and training/test overlap as first-class evidence boundaries.

## Mechanisms

- Investigate whether benchmark items may appear in model pretraining data.
- Compare benchmark score interpretation against contamination risk.
- Treat detection as an evaluation-audit problem rather than a model-capability result.
- Emphasize that benchmark validity depends on provenance, freshness, and contamination checks.

## Evidence

- The source reports contamination investigation methods and findings in its own benchmark/model setting.
- This repository has not run the contamination detector, audited any benchmark dataset, or reproduced the paper's results.
- Use the source as external contamination-audit vocabulary, not as evidence that local tests are uncontaminated.

## Failure Modes

- Contamination detection can produce false positives or miss paraphrased leakage.
- Public benchmark questions can become training data after release.
- A score without dataset provenance and model-training disclosure can overstate readiness.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and Anti-Goodhart Evidence)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `readiness-gates-residual-escrow-and-quarantine` (Readiness Gates, Residual Escrow, and Quarantine)
- `living-book-methodology` (Living Book Methodology)

## Claims To Add Or Update

- Use this note to require contamination and provenance records before benchmark evidence is treated as stronger support.
- Do not claim local contamination audit, uncontaminated benchmark status, or score validity.
- Keep support state at `argument` until benchmark provenance checks and evidence transitions exist.

## Open Questions

- What contamination-risk field should every benchmark ratchet packet carry?
- How should a living release invalidate or quarantine scores when contamination is later suspected?
- Which local tests can remain useful as regression checks even if benchmark evidence cannot promote claims?
