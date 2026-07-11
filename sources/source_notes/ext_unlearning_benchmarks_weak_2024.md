# Source Note: LLM Unlearning Benchmarks are Weak Measures

| Field | Value |
|---|---|
| Source ID | `ext_unlearning_benchmarks_weak_2024` |
| Source title | Position: LLM Unlearning Benchmarks are Weak Measures of Progress |
| Ingestion date | 2026-07-11 |
| Source version / URL | arXiv:2410.02879, https://arxiv.org/abs/2410.02879 |
| Citation label | Thaker et al. (2024), LLM Unlearning Benchmarks are Weak Measures |
| Published / updated | 2024-10-03 / 2024-10-03 |
| DOI | 10.48550/arXiv.2410.02879 |
| Ingestion basis | Primary position paper abstract and analysis of benchmark modifications, dependencies, and target ambiguity reviewed. |

## Thesis

Popular LLM-unlearning benchmarks can give misleading progress signals when
targets are ambiguous or forget/retain information is artificially separable.

## Mechanisms

- Benign benchmark modifications and dependency perturbations.
- Re-evaluation of retained degradation and residual accessibility.
- Analysis of target ambiguity and test-query overfitting.

## Evidence

The paper demonstrates weaknesses in existing benchmark settings. It does not
validate P3; it raises the standard for interpreting P3's synthetic outcomes.

## Failure Modes

Query overfitting can look like forgetting; retained effects can be hidden;
loosely dependent information can reveal residual knowledge.

## Book Chapters Supported

- `data-engines-continual-learning-and-unlearning`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `evidence-states-and-claim-discipline`

## Claims To Add Or Update

Treat P3 as bounded causal bookkeeping and reject any move from behavioral
change to privacy, influence, or storage claims without dedicated evidence.

## Open Questions

- Which benign mutations should become permanent P3 regressions?
- How should target ambiguity be represented in deletion receipts?
