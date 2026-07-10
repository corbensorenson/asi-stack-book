# Source Note: Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory

| Field | Value |
|---|---|
| Source ID | `ext_mem0_2025` |
| Source title | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory |
| Ingestion date | 2026-07-10 |
| Source version / URL | Preprint, https://arxiv.org/abs/2504.19413 |
| Citation label | Chhikara et al. (2025), Mem0 |
| Published / updated | 2025-04-28 / 2025-04-28 |
| Ingestion basis | Metadata-first intake from the public preprint record and repository inventory; no production or benchmark claim is imported. |

## Thesis

Mem0 is a comparator for extracting, consolidating, retrieving, and graph-linking conversational memory under latency and token-cost constraints.

## Mechanisms

- The inventory records memory extraction, consolidation, retrieval, graph linking, latency, and token-cost framing.
- It is routed to context, transactions, procedural memory, resource economics, and benchmark discipline.

## Evidence

- This note preserves the inventory’s scoped description only.
- LOCOMO and LLM-judge results require passage review and separate local tests before any evidence transition.

## Failure Modes

- Treating extracted memories as correct facts or safe updates.
- Ignoring poisoning, retention, privacy, and evaluation-validity limits.

## Book Chapters Supported

- `virtual-context-abi`
- `context-transactions-snapshots-mounts-and-taint`
- `procedural-memory-and-cognitive-loop-closure`
- `resource-economics-and-token-budgets`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Use as a comparator for long-term-memory trade-offs, not as evidence of a local or production memory system.

## Open Questions

- What memory admission, deletion, and poisoned-retrieval fixtures would fairly test the claimed trade-offs?
