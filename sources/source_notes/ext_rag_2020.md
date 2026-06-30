# Source Note: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

| Field | Value |
|---|---|
| Source ID | `ext_rag_2020` |
| Source title | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2005.11401, https://arxiv.org/abs/2005.11401 |
| Citation label | Lewis et al. (2020), Retrieval-Augmented Generation |
| Published / updated | 2020-05-22 / 2021-04-12 |
| DOI | 10.48550/arXiv.2005.11401 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the retrieval/context literature queue; paper not vendored into this repository and no model result reproduced. |

## Thesis

RAG belongs in the memory and context chapters as the external baseline for combining parametric generation with explicit non-parametric retrieval. It grounds the ASI Stack distinction between model memory, retrieved context, provenance, and updateable knowledge stores.

## Mechanisms

- Pair a pretrained generator with a retrieval mechanism.
- Use a dense vector index as non-parametric memory.
- Condition generation on retrieved passages.
- Compare retrieved-context generation with parametric-only baselines in the source setting.

## Evidence

- The source reports performance and factuality improvements in its evaluated tasks.
- This repository has not reproduced the retriever, index, datasets, fine-tuning recipe, or evaluations.
- Use it as external context for retrieval/context interfaces, not as evidence that VCM or semantic pages work.

## Failure Modes

- Retrieval can supply irrelevant, stale, or contaminated evidence.
- Provenance can be displayed without being adequate for the claim.
- RAG-style performance does not prove context adequacy or source interpretation.

## Book Chapters Supported

- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)

## Claims To Add Or Update

- Use this note to ground retrieval-augmented context as external literature.
- Do not claim local retrieval performance, factuality improvement, or VCM conformance.
- Require context-adequacy tests before any support-state promotion.

## Open Questions

- What context transaction should record retrieval provenance, staleness, and taint?
- Which fixture tests whether retrieved context is adequate for a specific claim?
- How should source updates invalidate stale generated claims?
