# Source Note: Eliciting Latent Knowledge

| Field | Value |
|---|---|
| Source ID | `ext_elk_report_2021` |
| Source title | Eliciting Latent Knowledge |
| Source version / URL | <https://www.alignment.org/blog/arcs-first-technical-report-eliciting-latent-knowledge/> |
| Ingestion date | 2026-07-24 |

## Thesis

ARC frames the problem of mapping from a model's internal world model to
human-understandable answers when ordinary training may reward a convincing
report rather than a true one. The report is a research agenda, not a solved
elicitation method.

## Mechanisms

- reporter training over a latent predictor;
- direct, consistency, and counterfactual training strategies;
- distinguishing the model's knowledge from what a reporter says;
- ontology translation and adversarial reporter alternatives.

## Evidence

The report develops problem statements, examples, and candidate approaches.
It does not provide a general empirical method that reliably recovers latent
truth from frontier models.

## Failure Modes

- a reporter optimized for human approval rather than latent truth;
- predictor and reporter sharing the same blind spot;
- probes reading correlates instead of the intended variable;
- ontology mismatch between model and evaluator;
- consistency tests satisfied by coordinated deception or shortcut features.

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`

## Claims To Add Or Update

- White-box evidence should preserve the distinction between latent state,
  probe or reporter output, evaluator ontology, intervention, and observed
  behavior.
- ELK remains an open research problem; probe readability does not establish
  faithful reporting or safety.

## Open Questions

- Which interventions distinguish truthful from merely consistent reporters?
- How can ontology mismatch be detected rather than assumed away?
- What independent evidence can validate a reporter on naturally novel cases?
