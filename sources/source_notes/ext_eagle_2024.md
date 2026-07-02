# Source Note: EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty

| Field | Value |
|---|---|
| Source ID | `ext_eagle_2024` |
| Source title | EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2401.15077, https://arxiv.org/abs/2401.15077 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

EAGLE reframes speculative acceleration around feature-level drafting. Instead of drafting only surface tokens, it predicts high-level model features and then verifies generated text against the target model. The ASI Stack should treat this as a latent-drafting route whose evidence boundary differs from token-level draft models.

## Mechanisms

- Draft at a second-to-top-layer feature level rather than only at the token level.
- Use a token sequence advanced by one step to address feature-prediction uncertainty.
- Verify generated candidates against the original model's decoding behavior.
- Evaluate latency and throughput under multiple model families and tasks.
- Preserve the distinction between feature proposal, token realization, and target-model verification.

## Evidence

- The source reports latency and throughput improvements while maintaining generated-text distribution under its method.
- This repository has not run EAGLE, inspected its code, or reproduced its model/hardware/task evaluations.
- Use the source to support feature-level drafting in the fast-generation taxonomy.

## Failure Modes

- Feature-level proposals can fail differently from token proposals, especially under domain shift.
- Distribution-preservation depends on the precise verification procedure.
- Feature predictors introduce their own lifecycle, training, and readiness concerns.
- Latency gains may disappear when verifier cost, memory pressure, or risk-tier policy is included.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)

## Claims To Add Or Update

- Use this source to source-note feature-level speculative drafting.
- Keep the chapter's claims at the architectural level: feature proposals must still expose verifier, acceptance, fallback, and accounting fields.
- Do not claim feature drafting has been validated for the book's workloads.

## Open Questions

- What schema fields should distinguish token-level, branch-level, and feature-level proposals?
- How should a verifier record show that a latent proposal did not change the task-relevant distribution?
- Which failure cases should be kept as residuals for feature-level drafting?
