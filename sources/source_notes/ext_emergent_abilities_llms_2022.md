# Source Note: Emergent Abilities of Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_emergent_abilities_llms_2022` |
| Source title | Emergent Abilities of Large Language Models |
| Source version / URL | <https://openreview.net/forum?id=yzkSU5zdwD> |
| Ingestion date | 2026-07-24 |

## Thesis

Wei and colleagues organize examples of task performance reported as absent in
smaller language models and present in larger ones. The work motivates direct
study of sharpness and predictability under scaling.

## Mechanisms

- cross-scale task evaluation;
- thresholded or exact-match metrics;
- comparison of smaller and larger model families;
- task-level identification of apparently abrupt performance changes.

## Evidence

The paper reports observations across selected tasks and model series. It does
not prove a universal phase transition, common causal mechanism, or
unpredictability theorem.

## Failure Modes

- coarse model checkpoints hiding a smooth transition;
- discontinuous scoring making gradual ability appear abrupt;
- small test sets and ceiling or floor effects;
- prompt, contamination, and model-family changes confounded with scale;
- retrospective task selection.

## Book Chapters Supported

- `learning-theory-generalization-and-scaling-science`

## Claims To Add Or Update

- Emergence claims require explicit task, metric, model series, sampling,
  uncertainty, and competing smooth-scaling explanations.
- Observed abruptness and architectural phase transition remain separate
  hypotheses.

## Open Questions

- Which continuous measurements best expose precursor competence?
- How much apparent emergence survives denser scale sweeps?
- Can mechanistic changes predict capability transitions prospectively?
