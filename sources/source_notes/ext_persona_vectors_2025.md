# Source Note: Persona Vectors: Monitoring and Controlling Character Traits in Language Models

| Field | Value |
|---|---|
| Source ID | `ext_persona_vectors_2025` |
| Review date | 2026-11-02 |
| Primary source | [Chen et al. (2025), Persona Vectors](https://arxiv.org/html/2507.21509v3) |
| Version | 2507.21509v3 |
| Published / updated | 2025-07-29 / 2025-09-05 |
| Review scope | Sections 2.1–2.2, 3.1–3.3, 5.1–5.2 and 8; selected extraction, monitoring, inference/training intervention and limitation passages. |
| Storage | Authored note only; primary text/excerpts remain in ignored research cache. |

## Thesis

Contrastively extracted residual-stream directions can monitor or alter expressed character traits.

## Mechanisms

Generates trait prompts, questions and a scoring rubric, filters contrastive responses and differences mean response activations. Layer-specific vectors support projection monitoring and additive inference steering. Preventative steering supplies the undesired direction during finetuning, with a different inference role.

## Evidence

Reports two-model studies centered on harmful expression, sycophancy and hallucination. Strong post-hoc suppression can degrade MMLU; preventative training-time steering reports a different capability tradeoff.

## Failure Modes

Supervised trait selection, small question sets and model-judge labels limit coverage. Dense vectors are not single neurons or a complete objective representation. Suppression under a hook is not evidence that a learned objective was removed.

## Claims To Add Or Update

Represent the intervention or hypothesis in the existing owner(s) below.
Stored model weights, runtime activation state, auxiliary controller training,
trait-expression scores and learned-objective integrity remain distinct. This
is no local implementation, experiment, support promotion or deployment claim.

## Open Questions

Does improvement survive independent behavioral assessment, removal of the intervention, new contexts and capability controls?

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`
- `inner-alignment-mesa-optimization-and-learned-objective-integrity`

## Chapter Decision

Update existing owners through
`new_paper_triage_scenarios/persona_neuron_steering_2026_11_02.json` and
`research_backlog_records/persona_neuron_steering_2026_11_02.json`.
Selected-source review only, not full proof/code audit or independent replication.
