# Source Note: Understanding Black-box Predictions via Influence Functions

| Field | Value |
|---|---|
| Source ID | `ext_influence_functions_2017` |
| Source title | Understanding Black-box Predictions via Influence Functions |
| Source version / URL | <https://proceedings.mlr.press/v70/koh17a.html> |
| Ingestion date | 2026-07-24 |

## Thesis

Koh and Liang use influence-function approximations to trace predictions
through a learning algorithm to influential training examples. This can
support debugging, data inspection, and attack analysis under stated
smoothness and optimization assumptions.

## Mechanisms

- approximate parameter change under infinitesimal example upweighting;
- estimate prediction change through inverse-Hessian-vector products;
- rank influential training points;
- inspect harmful or mislabeled examples and targeted perturbations.

## Evidence

The paper reports useful approximations and applications in studied models.
Influence estimates are not exact causal provenance, membership proof, privacy
erasure, or proof that removing a point removes its learned effect.

## Failure Modes

- non-convexity, poor Hessian approximation, or optimizer-path dependence;
- distributed influence not captured by individual rankings;
- correlations mistaken for legal or causal responsibility;
- stale estimates after continued training;
- cohort deletion certified from behavioral change alone;
- privacy leakage through attribution tooling.

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`
- `data-engines-continual-learning-and-unlearning`

## Claims To Add Or Update

- Training attribution should record method, assumptions, checkpoint,
  granularity, uncertainty, and validation interventions.
- Behavioral cohort removal, estimated influence reduction, privacy
  protection, and storage erasure require separate evidence.

## Open Questions

- Which attribution methods remain useful at foundation-model scale?
- How can estimates be validated without exposing private examples?
- What interventions distinguish approximate influence from actual causality?
