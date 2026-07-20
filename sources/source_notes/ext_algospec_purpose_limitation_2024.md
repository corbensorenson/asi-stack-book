# Source Note: AlgoSpec purpose-limitation enforcement

| Field | Value |
|---|---|
| Source ID | `ext_algospec_purpose_limitation_2024` |
| Source title | Being Transparent Is Merely the Beginning: Enforcing Purpose Limitation with Polynomial Approximation |
| Ingestion date | 2026-07-19 |
| Source version / URL | USENIX Security 2024, https://www.usenix.org/conference/usenixsecurity24/presentation/liu-shuofeng |
| Citation label | Liu et al. (2024), Being Transparent Is Merely the Beginning |
| Published / updated | 2024-08 / 2024-08 |
| DOI | none |
| Review state | Paper-body and official proceedings page reviewed. |
| Ingestion basis | Problem statement, polynomial design, security analysis, entropy and Naive Bayes evaluations, and limitations. Implementation was not run. |

## Thesis

Authorization records alone do not enforce purpose limitation. AlgoSpec
obscures data for use by an authorized algorithm or algorithm group,
illustrating one purpose-specific technical design.

## Mechanisms

- Approximate authorized computation with a polynomial and transform inputs to
  preserve that computation while restricting alternatives.

## Evidence

The source reports bounded accuracy and efficiency results. They are not
reproduced and do not establish broad enforcement for adaptive or generative models.

## Failure Modes

- Overbroad algorithm groups, approximation error, alternate recovery paths,
  and applicability limits.
- Treating one restriction as complete legal purpose limitation.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- Boundary: `security-kernel-and-digital-scifs`

## Claims To Add Or Update

- Include algorithm-specific restriction as a competing design; do not assume
  metadata alone enforces purpose.

## Open Questions

- Can restriction survive learned or adaptive computation?
- What natural-workload utility and governance costs result?
