# Source Note: Lyra’s Neuron Explorer: Steering-First Neuron Exploration

| Field | Value |
|---|---|
| Source ID | `ext_lyra_neuron_explorer_2026` |
| Review date | 2026-11-02 |
| Primary source | [Lyra (@_lyraaaa_), Neuron Explorer (2026)](https://github.com/lyramakesmusic/neuron-explorer/tree/7ec363d2d9686802a1b4aa7c6d8a2627b1759159) |
| Version | 7ec363d2d9686802a1b4aa7c6d8a2627b1759159 |
| Published / updated | 2026-10-18 / 2026-11-01 |
| Review scope | Pinned repository 7ec363d2d9686802a1b4aa7c6d8a2627b1759159: README; research_log.md framing and initial full-layer/control passages (lines 1–155); explorer/runtime.py loading/hook implementation (lines 1–155). lyraaaa.dev confirms project and Evil Qwen links. X post itself returned HTTP 403 and was not independently read. |
| Storage | Authored note only; primary text/excerpts remain in ignored research cache. |

## Thesis

Explore what raw MLP coordinates write by steering them, retaining rollouts and comparing matched controls.

## Mechanisms

The inspected runtime hooks the input of down_proj, where gated MLP activations live. Additive and multiplicative edits differ. The log distinguishes output-direction addition from ablation and normalizes additive doses to residual scale.

## Evidence

The author reports sweeps and cross-prompt themes with random-direction comparisons. The log also reports that random directions can change claimed maker identity, and strong pushes can damage coherence. The public site links the illustrative Evil Qwen demo.

## Failure Modes

Code inspection and author logs are not local execution or independent replication. A changed self-description, striking selected rollout or few-coordinate intervention does not identify a unique personality mechanism or stable objective. No provenance or popularity claim beyond the author-linked project is established.

## Claims To Add Or Update

Represent the intervention or hypothesis in the existing owner(s) below.
Stored model weights, runtime activation state, auxiliary controller training,
trait-expression scores and learned-objective integrity remain distinct. This
is no local implementation, experiment, support promotion or deployment claim.

## Open Questions

Do interpretations survive held-out prompts, matched-size random/off-target controls, sampling variation and capability checks?

## Book Chapters Supported

- `white-box-evidence-interpretability-and-activation-governance`

## Chapter Decision

Update existing owners through
`new_paper_triage_scenarios/persona_neuron_steering_2026_11_02.json` and
`research_backlog_records/persona_neuron_steering_2026_11_02.json`.
Selected-source review only, not full proof/code audit or independent replication.
