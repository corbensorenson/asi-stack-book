# Source Note: Neuron-based Personality Trait Induction in Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_neuron_personality_trait_induction_2024` |
| Review date | 2026-11-02 |
| Primary source | [Deng et al. (ICLR 2025; 2026 arXiv revision), NPTI](https://arxiv.org/html/2410.12327v2) |
| Version | 2410.12327v2 |
| Published / updated | 2024-10-16 / 2026-06-10 |
| Review scope | Sections 3.2–3.3 (neuron definition, identification and manipulation), abstract/experiment scope; ICLR 2025 proceedings record checked. Selected passages from the June 2026 v2 revision. |
| Storage | Authored note only; primary text/excerpts remain in ignored research cache. |

## Thesis

Induce Big Five trait expression by changing selected feed-forward activation coordinates during inference.

## Mechanisms

Contrasts positive activation probabilities on high/low-trait generations. It suppresses one selected set and adds an activation-scaled increment to the opposing set, leaving stored model weights fixed.

## Evidence

Reports PersonalityBench trait-expression and fluency comparisons. The manipulated objects are architectural FFN coordinates, not a discovered universal unit for a human personality.

## Failure Modes

Identification is contrast- and threshold-dependent; intervention sufficiency does not establish unique semantics or necessary causal structure. Trait and fluency scores do not establish stable cross-context personality, unchanged cognition or alignment.

## Claims To Add Or Update

Represent the intervention or hypothesis in the existing owner(s) below.
Stored model weights, runtime activation state, auxiliary controller training,
trait-expression scores and learned-objective integrity remain distinct. This
is no local implementation, experiment, support promotion or deployment claim.

## Open Questions

Which changes survive matched prompts, random-coordinate controls, doses, checkpoints and protected-capability tests?

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`

## Chapter Decision

Update existing owners through
`new_paper_triage_scenarios/persona_neuron_steering_2026_11_02.json` and
`research_backlog_records/persona_neuron_steering_2026_11_02.json`.
Selected-source review only, not full proof/code audit or independent replication.
