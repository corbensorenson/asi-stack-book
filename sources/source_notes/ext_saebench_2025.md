# Source Note: SAEBench

| Field | Value |
|---|---|
| Source ID | `ext_saebench_2025` |
| Source title | SAEBench: A Comprehensive Benchmark for Sparse Autoencoders in Language Model Interpretability |
| Ingestion date | 2026-07-26 |
| Source version / URL | arXiv:2503.09532v4, https://arxiv.org/abs/2503.09532 |
| Citation label | Karvonen et al. (2025), SAEBench |
| Published / updated | 2025-03-12 / 2025-06-04 |
| DOI | 10.48550/arXiv.2503.09532 |
| Ingestion basis | Primary paper inspected at Sections 1, 3–6, the metric definitions, practitioner guidance, architecture and scale comparisons, and limitations. No SAE or benchmark was run locally. |

## Thesis

Sparse-autoencoder quality is multi-dimensional. Reconstruction at a chosen
sparsity, concept detection, automated interpretability, feature
disentanglement, and task-specific intervention behavior can disagree.
SAEBench supplies a standardized multi-metric comparison and argues against
using the sparsity–fidelity frontier as a complete proxy.

## Mechanisms

- Evaluate concept detection, interpretability, reconstruction, and feature
  disentanglement with eight metrics.
- Sweep SAE architectures, dictionary widths, sparsity levels, and
  intervention-set sizes.
- Compare practical and diagnostic metrics rather than collapsing them into a
  single score.
- Evaluate multiple directly comparable SAEs across a range of sparsities so a
  claimed improvement must move a relevant Pareto frontier.

## Evidence

Sections 4–5 report that architecture rankings vary across metrics and sparsity
regimes, that reconstruction rankings need not predict downstream
interpretability tasks, and that dictionary scaling can improve some metrics
while worsening concept isolation. The paper also states that its metrics
cannot be meaningfully collapsed into one global score and do not capture every
qualitative interpretability value.

## Failure Modes

- Optimizing reconstruction and sparsity can hide feature absorption,
  splitting, or poor downstream utility.
- Automated labels can score comprehensibility without causal faithfulness.
- A fixed intervention budget can interact with dictionary width.
- Benchmark conclusions may not transfer across model families, scales,
  layers, modalities, or use cases.
- Multi-metric breadth does not guarantee that each metric is reliable.

## Book Chapters Supported

- Primary: `white-box-evidence-interpretability-and-activation-governance`
- Handoff: `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Select metrics from the decision being supported; never mint one global SAE
  quality or governance score.
- Sweep sparsity, width, seed, checkpoint, and method family with directly
  comparable baselines.
- Preserve proxy, construct, causal, intervention, collateral, and transfer
  results as distinct evidence states.

## Open Questions

- Which metric bundle predicts useful mechanistic discoveries or safer
  interventions?
- How should benchmark noise and analyst cost enter a method-selection policy?
- What model- and task-specific evidence is required before an SAE-derived
  activation policy can be considered?
