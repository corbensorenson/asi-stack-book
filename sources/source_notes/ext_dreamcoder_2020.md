# Source Note: DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning

| Field | Value |
|---|---|
| Source ID | `ext_dreamcoder_2020` |
| Source title | DreamCoder: Growing generalizable, interpretable knowledge with wake-sleep Bayesian program learning |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2006.08381, https://arxiv.org/abs/2006.08381 |
| Citation label | Ellis et al. (2020), DreamCoder |
| Published / updated | 2020-06-15 / 2020-06-15 |
| DOI | 10.48550/arXiv.2006.08381 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the program-synthesis and representation-compression literature queue; code, tasks, libraries, and synthesis results are not imported into this repository. |

## Thesis

DreamCoder belongs in the cognitive-compilation, compression, artifact-compression, and search-substrate chapters as an external reference for learning reusable symbolic abstractions from solved tasks. It helps the ASI Stack distinguish compression by abstraction from compression by weight reduction or prompt shortening.

## Mechanisms

- Search for programs that solve tasks.
- Infer reusable library components from discovered solutions.
- Use wake-sleep style learning to improve recognition models and guide later synthesis.
- Treat learned abstractions as interpretable knowledge that can reduce future search burden.

## Evidence

- The source reports program-synthesis and library-learning results in its own task environments.
- This repository has not run DreamCoder, imported task suites, learned libraries, or reproduced synthesis metrics.
- Use the source as external vocabulary for program synthesis and abstraction learning, not as evidence for ASI Stack cognitive compilation.

## Failure Modes

- Learned abstractions can overfit the task distribution that produced them.
- Reusable library components can hide residual obligations when later tasks differ.
- Interpretable programs still require provenance, authority, and regression tests before promotion.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir` (Cognitive Compilation and Semantic IR)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems and Residual Honesty)
- `rankfold-neuralfold-and-artifact-compression` (RankFold, NeuralFold, and Artifact Compression)
- `mathematical-and-search-substrates` (Mathematical and Search Substrates)

## Claims To Add Or Update

- Use this note to compare ASI Stack abstraction and compression proposals with program-synthesis library learning.
- Do not claim local synthesis, search reduction, library learning, or task generalization.
- Keep support state at `argument` until local synthesis traces, artifact records, or accepted evidence transitions exist.

## Open Questions

- Which artifact record should preserve a learned abstraction's training-task lineage?
- What regression suite should block a reusable abstraction from silently changing semantics?
- How should a future cognitive compiler expose residual tasks that were not compressed away?
