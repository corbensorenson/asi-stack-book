# Source Note: The Assistant Axis: Situating and Stabilizing the Default Persona of Language Models

| Field | Value |
|---|---|
| Source ID | `ext_assistant_axis_2026` |
| Review date | 2026-11-02 |
| Primary source | [Lu et al. (2026), The Assistant Axis](https://arxiv.org/html/2601.10387v1) |
| Version | 2601.10387v1 |
| Published / updated | 2026-01-15 / 2026-01-15 |
| Review scope | Sections 3.1–3.2, 5.1–5.2 and 8.1. Primary-paper capping formula and target-model limits take precedence over a simplified range description in the blog. |
| Storage | Authored note only; primary text/excerpts remain in ignored research cache. |

## Thesis

A contrast direction separates default Assistant behavior from sampled role-playing behavior and can stabilize selected persona-drift cases.

## Mechanisms

Subtracts mean role activations from default Assistant activations. The direction correlates with persona-space PC1 but is not defined as necessarily PC1. Capping imposes a lower bound on its projection, applied at selected multiple layers rather than constant vector addition everywhere.

## Evidence

Maps persona space in three open dense models and reports selected capping results in Qwen/Llama. A tuned setting reduces studied harmful responses while retaining scores on the selected capability battery.

## Failure Modes

Target models are not frontier or generally reasoning-trained; Qwen thinking is disabled. Synthetic conversations, incomplete persona elicitation and linear approximations limit transport. Selected benchmark preservation is not universal capability or deployment safety.

## Claims To Add Or Update

Represent the intervention or hypothesis in the existing owner(s) below.
Stored model weights, runtime activation state, auxiliary controller training,
trait-expression scores and learned-objective integrity remain distinct. This
is no local implementation, experiment, support promotion or deployment claim.

## Open Questions

How do independently selected caps behave on actual multi-turn users, reasoning/MoE models and held-out harms?

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`

## Chapter Decision

Update existing owners through
`new_paper_triage_scenarios/persona_neuron_steering_2026_11_02.json` and
`research_backlog_records/persona_neuron_steering_2026_11_02.json`.
Selected-source review only, not full proof/code audit or independent replication.
