# Source Note: MemGPT: Towards LLMs as Operating Systems

| Field | Value |
|---|---|
| Source ID | `ext_memgpt_2023` |
| Source title | MemGPT: Towards LLMs as Operating Systems |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2310.08560, https://arxiv.org/abs/2310.08560 |
| Citation label | Packer et al. (2023), MemGPT |
| Published / updated | 2023-10-12 / 2024-02-12 |
| DOI | 10.48550/arXiv.2310.08560 |
| Ingestion basis | Primary arXiv abstract and metadata inspected for the retrieval/context literature queue; paper not vendored into this repository and no MemGPT code, data, or evaluation reproduced. |

## Thesis

MemGPT belongs in the VCM, semantic-page, context-transaction, verification-bandwidth, and procedural-memory chapters as an external comparison point for OS-inspired virtual context management. It gives the ASI Stack a third-party vocabulary for memory tiers, context-window scarcity, and explicit data movement without implying that VCM implements MemGPT or reproduces MemGPT results.

## Mechanisms

- Treat limited model context as a scarce fast-memory region.
- Move information between different memory tiers to create the appearance of larger usable context.
- Use OS-inspired control-flow ideas, including interrupts, to manage interaction between the system and user.
- Evaluate the source system in document-analysis and multi-session chat settings where long-lived context matters.

## Evidence

- The source reports an OS-inspired design, released code/data links, and evaluations in the paper's own settings.
- This repository has not run MemGPT, imported its code or data, evaluated document-analysis tasks, or reproduced multi-session chat results.
- Use this source for context-management vocabulary and comparison, not as evidence that VCM, semantic pages, or procedural memory work.

## Failure Modes

- OS memory metaphors can hide model-specific failure modes such as summary drift, stale memory, contamination, or unverified retrieval.
- Tiered memory movement can appear disciplined while losing claim-level provenance, taint, or deletion obligations.
- A long-running chat result cannot justify local context adequacy without a replayable task, memory trace, and evaluation boundary.

## Book Chapters Supported

- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `procedural-memory-and-cognitive-loop-closure` (Procedural Memory and Cognitive Loop Closure)

## Claims To Add Or Update

- Use this note to compare VCM's ABI and transaction vocabulary against external virtual context management.
- Do not claim local MemGPT compatibility, code import, result reproduction, or memory adequacy.
- Keep support state at `argument` until a context-management trace, replayable memory task, or accepted evidence transition exists.

## Open Questions

- Which VCM receipt fields correspond to memory-tier movement, eviction, summarization, and recall?
- What trace would show that a context-management decision preserved claim provenance?
- How should procedural memory distinguish useful long-term state from stale or contaminated state?
