# Source Note: Fast Inference from Transformers via Speculative Decoding

| Field | Value |
|---|---|
| Source ID | `ext_speculative_decoding_2022` |
| Source title | Fast Inference from Transformers via Speculative Decoding |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2211.17192, https://arxiv.org/abs/2211.17192 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

Speculative decoding treats slow autoregressive decoding as a serial bottleneck that can be reduced when a cheaper approximation model drafts several candidate tokens and the target model verifies those candidates in parallel. Its central architectural value for the ASI Stack is the separation between proposed tokens and accepted tokens.

## Mechanisms

- Use a smaller or cheaper approximation model to propose multiple future tokens.
- Run the target model in a verification step that accepts or rejects drafted tokens under the paper's sampling procedure.
- Preserve the target model's output distribution under the method's assumptions rather than merely approximate a faster output.
- Count acceleration through accepted candidates and wall-clock speed, not only through proposed tokens.
- Treat drafting and verification as separable stages that can map cleanly to a generate-verify-accept interface.

## Evidence

- The source reports empirical acceleration on its evaluated transformer models.
- The paper is external literature; this repository has not reproduced its experiments, benchmark environment, or distribution-preservation proof details.
- Use the source to support the existence of a draft-and-verify decoding family, not to claim local speedup or universal superiority.

## Failure Modes

- A weak draft model can produce low acceptance rates that erase acceleration.
- Verification can become the bottleneck if target-model checks, memory movement, or batching are poorly matched to the workload.
- Reported speedups may not transfer across model families, hardware, context lengths, sampling policies, or task risk tiers.
- Distribution-preservation claims depend on the exact algorithm and assumptions; variants must be audited separately.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this source to turn speculative decoding from a queued example into an externally source-noted generation-mode family.
- Keep the ASI Stack claim focused on proposed-versus-accepted token accounting, verifier cost, fallback, and risk-tier routing.
- Do not use this note to claim that the book has reproduced speculative decoding benchmarks.

## Open Questions

- What small benchmark suite should measure proposed tokens, accepted tokens, verifier cost, quality, and fallback rate?
- Which acceptance predicates are compatible with safety-critical or citation-bearing tasks?
- How should speculative decoding be represented in the generation-mode schema when the draft model and target model have different authority or memory access?
