# Source Note: Lost in the Middle: How Language Models Use Long Contexts

| Field | Value |
|---|---|
| Source ID | `ext_lost_in_middle_2023` |
| Source title | Lost in the Middle: How Language Models Use Long Contexts |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2307.03172, https://arxiv.org/abs/2307.03172 |
| Citation label | Liu et al. (2023), Lost in the Middle |
| Published / updated | 2023-07-06 / 2023-11-20 |
| DOI | 10.48550/arXiv.2307.03172 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the long-context evaluation queue; paper not vendored into this repository and no evaluation reproduced. |

## Thesis

This source belongs in the context and verification-bandwidth chapters as an external warning that long context is not the same as usable context. It reinforces the book's distinction between context length, admission, adequacy, and verified use.

## Mechanisms

- Evaluate language models on tasks requiring relevant information inside long inputs.
- Vary the position of relevant information.
- Compare performance when information appears at the beginning, middle, or end.
- Provide protocols for evaluating long-context use.

## Evidence

- The source reports position sensitivity and degraded use of middle-position information.
- This repository has not reproduced the multi-document QA or key-value retrieval evaluations.
- Use it as context-evaluation literature, not as a local result about any ASI Stack model.

## Failure Modes

- Long context can create false confidence in adequacy.
- Relevant evidence can be present but unused.
- Context compaction can hide whether evidence was actually consumed.

## Book Chapters Supported

- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)

## Claims To Add Or Update

- Use this note to support the book's context adequacy backlog.
- Do not claim any local model has passed long-context position-sensitivity tests.
- Keep support state at `argument` until a context adequacy harness exists.

## Open Questions

- What VCM fixture should test relevant evidence in edge, middle, and compressed positions?
- How should context receipts record evidence that was available but unused?
- Which claims require context-use tests before source-derived promotion?
