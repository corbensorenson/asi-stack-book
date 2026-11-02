# Source Note: Persona Dosing: Calibrated Activation Steering for Graded Trait Control

| Field | Value |
|---|---|
| Source ID | `ext_persona_dosing_2026` |
| Review date | 2026-11-02 |
| Primary source | [Jin et al. (2026), Persona Dosing](https://arxiv.org/html/2609.36388v1) |
| Version | 2609.36388v1 |
| Published / updated | 2026-09-28 / 2026-09-28 |
| Review scope | Sections 3.1–3.3 and 6–7: controller, calibration/reachability, update effects and limitations. Selected held-out results and denominator distinctions. |
| Storage | Authored note only; primary text/excerpts remain in ignored research cache. |

## Thesis

A steering coefficient is not a behavioral trait intensity; calibrated requests require a measured response curve.

## Mechanisms

A shared description-conditioned FLAS flow controller transforms residual activations in a frozen language model. It is trained separately; isotonic fitting and interpolation map requested mean rubric scores to controller strength.

## Evidence

Reports reachable-target and held-out intensity/coherence results for seven trained traits in three models. Reachability, error over reachable requests and held-out coherence are different quantities.

## Failure Modes

Mean targets do not constrain each answer. Coherence is intelligibility, not factual correctness or safety. Reachable request sets differ between methods, so MAEs are not a paired common-request advantage. Some held-out coherence floors fail; stale-map error after controller update is not measured.

## Claims To Add Or Update

Represent the intervention or hypothesis in the existing owner(s) below.
Stored model weights, runtime activation state, auxiliary controller training,
trait-expression scores and learned-objective integrity remain distinct. This
is no local implementation, experiment, support promotion or deployment claim.

## Open Questions

How stable is the calibrated response on new populations, conversations, traits, judges and checkpoint/controller revisions?

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`

## Chapter Decision

Update existing owners through
`new_paper_triage_scenarios/persona_neuron_steering_2026_11_02.json` and
`research_backlog_records/persona_neuron_steering_2026_11_02.json`.
Selected-source review only, not full proof/code audit or independent replication.
