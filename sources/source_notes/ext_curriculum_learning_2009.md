# Source Note: Curriculum Learning

| Field | Value |
|---|---|
| Source ID | `ext_curriculum_learning_2009` |
| Source title | Curriculum Learning |
| Source version / URL | <https://doi.org/10.1145/1553374.1553380> |
| Ingestion date | 2026-07-24 |

## Thesis

Bengio and colleagues propose ordering training material from easier concepts
or examples toward harder ones. Curriculum becomes an optimization policy,
not merely a property of the dataset.

## Mechanisms

- difficulty or competence scoring;
- example ordering and pacing;
- staged expansion of the admitted training distribution;
- promotion criteria and coverage accounting;
- interaction between ordering, optimization, and generalization.

## Evidence

The source reports benefits in studied settings. Those results are
configuration-bound and do not establish that one curriculum improves every
architecture, objective, or domain, especially under continual learning.

## Failure Modes

- biased or circular difficulty labels;
- easy-example overfitting and delayed hard-case exposure;
- forgotten rare or safety-critical cases;
- curriculum leakage into evaluation;
- ordering that accelerates a proxy objective while degrading target behavior;
- unrecorded policy changes that break run comparability.

## Book Chapters Supported

- `governed-model-training-distributed-optimization-and-scaling`
- `data-engines-continual-learning-and-unlearning`

## Claims To Add Or Update

- Curriculum is a versioned training policy with explicit difficulty,
  ordering, pacing, promotion, coverage, and rollback records.
- Any claimed benefit must be compared with shuffled, anti-curriculum, and
  strongest adaptive baselines on joint utility and safety outcomes.

## Open Questions

- Which difficulty measure remains stable as the model learns?
- How should curricula preserve tail and adversarial coverage?
- When should a curriculum adapt online, and who may authorize that change?
