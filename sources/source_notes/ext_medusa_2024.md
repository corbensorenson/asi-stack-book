# Source Note: Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads

| Field | Value |
|---|---|
| Source ID | `ext_medusa_2024` |
| Source title | Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads |
| Ingestion date | 2026-06-25 |
| Source version / URL | arXiv:2401.10774, https://arxiv.org/abs/2401.10774 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the fast-generation literature queue; paper not vendored into this repository. |

## Thesis

Medusa accelerates LLM generation by attaching multiple decoding heads that propose future-token candidates and using tree-style verification to accept candidate continuations. Its book value is as an internal-draft-head family that avoids maintaining a separate draft model while still requiring acceptance accounting.

## Mechanisms

- Add extra decoding heads to predict multiple subsequent tokens.
- Construct candidate continuations with a tree-based attention mechanism.
- Verify multiple candidate branches in a decoding step.
- Distinguish frozen-backbone and jointly fine-tuned variants.
- Treat candidate branches as proposals that must be accepted, repaired, or rejected.

## Evidence

- The source reports speedups and quality comparisons under its evaluated models and training procedures.
- This repository has not trained Medusa heads, run its implementation, or reproduced its benchmarks.
- Use the source to support internal multi-head drafting as an external method family only.

## Failure Modes

- Head/backbone drift can lower candidate quality or acceptance rate.
- Training recipes can change the evidence boundary between lossless acceleration and quality-changing acceleration.
- Branch verification can add overhead or obscure which candidates were actually accepted.
- The method may not transfer unchanged to high-risk tasks where every accepted span needs stronger verification.

## Book Chapters Supported

- `fast-generation-architectures` (Fast Generation Architectures)

## Claims To Add Or Update

- Use this source to replace generic "multi-head decoding" queue language with a source-noted internal-draft-head example.
- Keep the chapter's claim about Medusa limited to taxonomy and benchmark design until local experiments exist.
- Do not treat reported speedups as ASI Stack test results.

## Open Questions

- How should a generation-mode record represent tree-branch proposals and accepted branches?
- What verifier cost should be charged to branch verification?
- Can Medusa-style heads be governed by the same readiness gate as separate specialist draft models?
