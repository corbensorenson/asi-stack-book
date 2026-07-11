# Source Note: OpenUnlearning

| Field | Value |
|---|---|
| Source ID | `ext_openunlearning_2025` |
| Source title | OpenUnlearning: Accelerating LLM Unlearning via Unified Benchmarking of Methods and Metrics |
| Ingestion date | 2026-07-11 |
| Source version / URL | NeurIPS 2025 Datasets and Benchmarks; arXiv:2506.12618 |
| Citation label | Dorna et al. (2025), OpenUnlearning |
| Published / updated | 2025 / 2025 |
| DOI | 10.48550/arXiv.2506.12618 |
| Ingestion basis | Primary NeurIPS proceedings abstract and framework scope reviewed; framework, methods, evaluations, and checkpoints were not run. |

## Thesis

Unlearning methods and metrics need standardized execution and meta-evaluation
because inconsistent implementations and unfaithful metrics block comparison.

## Mechanisms

- Unified methods, benchmarks, and evaluation interfaces.
- Public checkpoint collection and comparative evaluation suite.
- Meta-evaluation of metric faithfulness and robustness.

## Evidence

The paper reports a large framework over leading benchmarks. P3 does not
reproduce it; the source chiefly grounds evaluator-quality residuals.

## Failure Modes

Standardization can preserve weak metrics; checkpoints can be incomparable;
framework breadth does not establish erasure or legal compliance.

## Book Chapters Supported

- `data-engines-continual-learning-and-unlearning`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `living-book-methodology`

## Claims To Add Or Update

Version evaluators and treat metric validity as a separately owned residual;
do not equate schema uniformity with semantic validity.

## Open Questions

- Which P3 metrics survive independent reimplementation?
- How should metric-version changes invalidate prior dispositions?
