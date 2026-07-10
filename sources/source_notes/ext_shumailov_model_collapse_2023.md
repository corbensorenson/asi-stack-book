# Source Note: The Curse of Recursion: Training on Generated Data Makes Models Forget

| Field | Value |
|---|---|
| Source ID | `ext_shumailov_model_collapse_2023` |
| Source title | The Curse of Recursion: Training on Generated Data Makes Models Forget |
| Ingestion date | 2026-07-10 |
| Source version / URL | arXiv:2305.17493, https://arxiv.org/abs/2305.17493 |
| Citation label | Shumailov et al. (2023), The Curse of Recursion |
| Published / updated | 2023-05-27 / 2024-04-14 |
| DOI | 10.48550/arXiv.2305.17493 |
| Ingestion basis | Primary preprint passages on the recursive-data model, theoretical assumptions, language-model experiment, and stated provenance limits reviewed; the paper is not a deployed-data-governance result and was not reproduced. |

## Thesis

Shumailov et al. analyze a recursive training setting in which generated outputs
enter later generations' training data. Under their models and experiments,
finite sampling and approximation errors can compound, with low-probability
regions of the original distribution disappearing or becoming distorted.

## Mechanisms

- Model later-generation training as fitting to data that increasingly include
  earlier model outputs.
- Distinguish statistical sampling error from functional approximation error;
  both can compound in the modeled recursive loop.
- Analyze idealized discrete and Gaussian cases, then demonstrate degradation
  patterns in GMM, VAE, and fine-tuned language-model settings.
- Preserve access to data from the original distribution and distinguish the
  provenance of generated versus non-generated data as a proposed safeguard.

## Evidence

- The paper supplies theoretical analyses under stated assumptions and
  experiments in its own generative-model and language-model settings.
- Its language-model experiment is a proof-of-concept sequential fine-tuning
  setup, not a measurement of all modern pretraining pipelines or a universal
  law about every use of synthetic data.
- This repository has not classified data provenance, trained a recursive
  model sequence, measured a tail-loss metric, or reproduced any result.

## Failure Modes

- The work does not license the blanket claim that all synthetic data is
  harmful or that every mixed real/synthetic training pipeline collapses.
- Provenance itself can be unavailable, spoofed, or too coarse to establish
  whether a sample is safe to retain.
- Model collapse is not identical to ordinary catastrophic forgetting or to
  adversarial data poisoning, although a governed data engine must consider
  all three risks.

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback` (Policy Optimization and
  Learning from Feedback)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and
  Cognitive Loop Closure)
- `benchmark-ratchets-and-anti-goodhart-evidence` (Benchmark Ratchets and
  Anti-Goodhart Evidence)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and
  Bibliography Plan)

## Claims To Add Or Update

- Add provenance class, source-generation lineage, and distribution-coverage
  residuals to the prospective data-engine receipt.
- Treat synthetic-data admission as a measured, versioned decision with a
  declared replacement-versus-accumulation policy and an explicit failure
  detector.
- Do not claim that the ASI Stack has detected model collapse, preserved a
  human-data distribution, or validated synthetic-data safety.

## Open Questions

- Which measurable coverage, calibration, tail, or task-retention signals can
  safely trigger quarantine of a data source?
- How can a data engine record provenance when source data are transformed,
  distilled, augmented, or mixed across model generations?
- Which experiment could falsify a local claim that a retention policy avoids
  relevant degradation in a declared workload?
