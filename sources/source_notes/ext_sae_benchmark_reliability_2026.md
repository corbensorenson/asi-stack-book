# Source Note: Are Sparse Autoencoder Benchmarks Reliable?

| Field | Value |
|---|---|
| Source ID | `ext_sae_benchmark_reliability_2026` |
| Source title | Are Sparse Autoencoder Benchmarks Reliable? |
| Ingestion date | 2026-07-26 |
| Source version / URL | arXiv:2605.18229v1, https://arxiv.org/abs/2605.18229 |
| Citation label | Chanin (2026), Are Sparse Autoencoder Benchmarks Reliable? |
| Published / updated | 2026-05-18 / 2026-05-18 |
| DOI | 10.48550/arXiv.2605.18229 |
| Ingestion basis | Primary paper inspected at Sections 1–5 and 7, including reseed noise, training-trajectory discriminability, synthetic ground-truth validity, controls, practitioner recommendations, and stated limitations. No audit result was reproduced locally. |

## Thesis

An SAE benchmark must reliably distinguish better from worse extractors before
small metric differences can support architecture claims. The paper audits
selected SAEBench metrics through independent reseeds, discrimination across
training trajectories, and correlation with synthetic ground truth. It reports
that several metrics are noisier or less discriminative than assumed and that
TPP and SCR fail multiple checks at canonical settings.

## Mechanisms

- Re-run metrics with independent seeds on a fixed SAE to estimate evaluation
  noise.
- Track metrics along training trajectories and compare their discriminability
  with reconstruction error.
- Use synthetic hierarchical, correlated, and superposed features with known
  ground-truth directions and firing patterns.
- Include degraded controls and a perfect oracle to test whether a metric
  orders known-quality cases correctly.
- Compare metric reliability across tasks, hyperparameters, and SAE families.

## Evidence

Sections 3–5 report reseed noise, weak discrimination among related SAE
variants, and synthetic ground-truth failures for selected metrics. The
sae-probes variant of sparse probing is reported as the strongest of the
audited metrics while still having limited within-family discrimination. The
study excludes some SAEBench tasks and remains bounded to its configurations,
synthetic assumptions, and evaluated model/SAE panels.

## Failure Modes

- A noisy metric can crown different winners under different seeds.
- A metric can move in the wrong direction during otherwise successful
  training.
- Synthetic ground truth can expose invalid ordering while also simplifying
  real representation geometry.
- Canonical hyperparameters can fail even when a repaired variant might work.
- One benchmark audit can be laundered into a field-wide negative result.

## Book Chapters Supported

- Primary: `white-box-evidence-interpretability-and-activation-governance`
- Handoff: `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Require metric reliability, sensitivity, oracle, degraded-control, and
  repeated-seed checks before interpreting small SAE differences.
- A failed metric yields evidence about that metric and setting, not absence of
  interpretable structure or failure of all SAE methods.
- Preserve SAEBench's multi-dimensional framing while challenging the
  reliability of each constituent measure independently.

## Open Questions

- Which real-model tasks provide credible ground truth or positive controls for
  semantic and causal feature recovery?
- Can benchmark uncertainty be propagated into method-ranking and governance
  decisions?
- Which repairs improve TPP, SCR, and other metrics without optimizing directly
  to the audit?
