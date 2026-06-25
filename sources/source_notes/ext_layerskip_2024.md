# Source Note: LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding

| Field | Value |
|---|---|
| Source ID | `ext_layerskip_2024` |
| Source title | LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2404.16710, https://arxiv.org/abs/2404.16710 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

LayerSkip treats early transformer layers as a draft path and later layers as a verifier/corrector path after training changes that make early exits more reliable. Its ASI Stack value is the early-exit/self-speculative family: one model can expose cheaper draft routes without a separate draft model.

## Mechanisms

- Train with layer dropout and an early-exit loss.
- Exit at earlier layers when confidence or policy allows.
- Use remaining layers for self-speculative verification and correction.
- Reduce memory footprint compared with two-model speculative setups under the paper's assumptions.
- Evaluate speedups across model sizes and tasks.

## Evidence

- The source reports task-specific speedups and open-source artifacts.
- This repository has not trained LayerSkip models, run its inference path, or reproduced its task results.
- Use the source to support early-exit and self-speculative taxonomy entries.

## Failure Modes

- Early exits can be unreliable without compatible training.
- Draft and verifier share a model lineage, which may reduce independence for high-risk verification.
- Speedups can be task-specific and may depend on confidence thresholds, hardware, and sequence length.
- Early acceptance can hide quality loss if final artifact tests are absent.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this source to source-note early-exit and self-speculative decoding.
- Keep the ASI Stack treatment tied to risk tiers, confidence thresholds, later-layer verification, and fallback.
- Do not use this note as evidence that early exits are safe for authority-bearing tasks.

## Open Questions

- How should a generation-mode record represent the layer at which a draft exited?
- When is same-model verification too weak for a high-risk claim?
- Which tasks should force full-depth generation regardless of early-exit confidence?
