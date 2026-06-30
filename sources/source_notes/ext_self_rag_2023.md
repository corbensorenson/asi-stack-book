# Source Note: Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

| Field | Value |
|---|---|
| Source ID | `ext_self_rag_2023` |
| Source title | Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2310.11511, https://arxiv.org/abs/2310.11511 |
| Citation label | Asai et al. (2023), Self-RAG |
| Published / updated | 2023-10-17 / 2023-10-17 |
| DOI | 10.48550/arXiv.2310.11511 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the retrieval/reflection literature queue; model checkpoints, datasets, reflection-token training, and evaluations are not imported into this repository. |

## Thesis

Self-RAG belongs in the VCM, semantic-page, verification-bandwidth, and claim-ledger chapters as an external reference for adaptive retrieval and retrieval-aware critique. It helps the ASI Stack separate retrieval necessity, passage relevance, generated answer quality, and self-critique from the mere presence of a context window.

## Mechanisms

- Retrieve passages on demand rather than always injecting a fixed number of passages.
- Generate and reflect on retrieved passages and generated content.
- Use reflection tokens to make behavior controllable during inference.
- Evaluate retrieval-augmented factuality, citation accuracy, open-domain question answering, reasoning, and fact verification.

## Evidence

- The source reports Self-RAG performance gains against selected LLM and retrieval-augmented baselines in its evaluation setting.
- This repository has not trained Self-RAG, imported checkpoints, run its datasets, or reproduced citation/factuality scores.
- Use this source as external vocabulary for adaptive retrieval and critique loops, not as local VCM behavior evidence.

## Failure Modes

- Self-reflection can become self-certification if critique tokens are treated as evidence rather than as model outputs requiring validation.
- Adaptive retrieval can skip necessary evidence if the retrieval-necessity policy is wrong.
- Citation-accuracy gains in one setup cannot be imported into ASI Stack claim-ledger support without local traces.

## Book Chapters Supported

- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)

## Claims To Add Or Update

- Use this note to compare VCM admission and adequacy records against adaptive retrieval/reflection behavior.
- Do not claim the ASI Stack implements Self-RAG, improves factuality, or improves citation accuracy.
- Keep support state at `argument` until local retrieval traces, critique fixtures, benchmark runs, or accepted evidence transitions exist.

## Open Questions

- Which VCM adequacy record should decide whether retrieval is necessary before generation?
- How should critique outputs be stored so they remain reviewable but cannot promote their own claims?
- What fixture would reveal an adaptive retriever skipping evidence because the context looked sufficient?
