# Source Note: A Systematic Analysis of the Impact of Persona Steering on LLM Capabilities

| Field | Value |
|---|---|
| Source ID | `ext_persona_steering_capabilities_2026` |
| Review date | 2026-11-02 |
| Primary source | [Chen et al. (2026), Persona Steering and Capabilities](https://arxiv.org/html/2604.11048v2) |
| Version | 2604.11048v2 |
| Published / updated | 2026-04-13 / 2026-05-12 |
| Review scope | Methodology and experimental procedure; Leveraging Persona-Task Regularities including reference/test split, hit definition and mixed task outcomes. May v2; CogSci 2026 reference in arXiv metadata. |
| Storage | Authored note only; primary text/excerpts remain in ignored research cache. |

## Thesis

Persona steering can change cognitive benchmark performance as well as style, with task-dependent benefits and harms.

## Mechanisms

Uses NPTI coordinate modulation under paired same-input deterministic decoding. A retrieval-based proof of concept recommends persona sets from performance on reference questions.

## Evidence

Reports six-benchmark comparisons across selected model families/scales. The routing metric is a hit when any persona in the recommended set solves the test item; it is not the accuracy of a committed single choice.

## Failure Modes

The intervention bundles a named trait with activation changes; it does not isolate a human psychological construct as the unique cause. Small held-out subsets, best-static comparisons and set-valued success limit routing conclusions. Cross-species directional agreement is not shared biological mechanism evidence.

## Claims To Add Or Update

Represent the intervention or hypothesis in the existing owner(s) below.
Stored model weights, runtime activation state, auxiliary controller training,
trait-expression scores and learned-objective integrity remain distinct. This
is no local implementation, experiment, support promotion or deployment claim.

## Open Questions

Do benefits survive a single-choice held-out router, independent repeats and equal total inference budgets?

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`

## Chapter Decision

Update existing owners through
`new_paper_triage_scenarios/persona_neuron_steering_2026_11_02.json` and
`research_backlog_records/persona_neuron_steering_2026_11_02.json`.
Selected-source review only, not full proof/code audit or independent replication.
