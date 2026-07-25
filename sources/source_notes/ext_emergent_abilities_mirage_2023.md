# Source Note: Are Emergent Abilities of Large Language Models a Mirage?

| Field | Value |
|---|---|
| Source ID | `ext_emergent_abilities_mirage_2023` |
| Source title | Are Emergent Abilities of Large Language Models a Mirage? |
| Source version / URL | <https://proceedings.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html> |
| Ingestion date | 2026-07-24 |

## Thesis

Schaeffer and colleagues show in studied settings that discontinuous metrics
and small test sets can turn smooth underlying changes into apparently abrupt
emergence. Metric choice is therefore a mandatory competing explanation.

## Mechanisms

- transform discontinuous task scores into continuous alternatives;
- analyze how measurement nonlinearity changes scaling curves;
- compare apparent sharpness across metrics and sample sizes;
- retain uncertainty near floors and thresholds.

## Evidence

The result demonstrates metric-induced emergence in analyzed cases. It does
not prove that every capability transition is a mirage or exclude genuine
mechanistic phase changes.

## Failure Modes

- treating exact match as a continuous competence measure;
- ignoring binomial uncertainty and test-set size;
- replacing one arbitrary metric with another without construct validation;
- generalizing from studied tasks to all emergent-capability claims;
- using smooth aggregate scores to hide critical threshold crossings.

## Book Chapters Supported

- `learning-theory-generalization-and-scaling-science`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Scaling audits should compare continuous, probabilistic, thresholded, and
  task-completion metrics with confidence intervals.
- A metric artifact is a competing explanation, not an automatic dismissal of
  abrupt operational risk.

## Open Questions

- Which metrics track real-world task completion without creating false cliffs?
- How should policy thresholds treat smooth capability growth near a sharp
  consequence boundary?
- What evidence distinguishes measurement artifacts from mechanistic change?
