# Source Note: LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression

| Field | Value |
|---|---|
| Source ID | `ext_longllmlingua_2023` |
| Source title | LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression |
| Ingestion date | 2026-06-28 |
| Source version / URL | arXiv:2310.06839, https://arxiv.org/abs/2310.06839 |
| Citation label | Jiang et al. (2023), LongLLMLingua |
| Published / updated | 2023-10-10 / 2024-08-12 |
| DOI | 10.48550/arXiv.2310.06839 |
| Ingestion basis | Primary arXiv metadata and abstract inspected for the context-compression literature queue; code, compressed prompts, task outputs, and latency/cost evaluations are not imported into this repository. |

## Thesis

LongLLMLingua belongs in the VCM, context-transaction, verification-bandwidth, and resource-economics chapters as an external reference for prompt compression in long-context scenarios. It gives the ASI Stack vocabulary for key-information density, position bias, token-budget pressure, latency, cost, and compression-induced adequacy risk.

## Mechanisms

- Compress long prompts to preserve key information while reducing token count.
- Address long-context computational cost, performance degradation, and position bias.
- Evaluate compressed prompts across long-context scenarios and compare cost, latency, and task performance.
- Treat compression ratio, key-information perception, and end-to-end latency as measurable surfaces.

## Evidence

- The source reports cost, latency, and performance improvements in its own long-context evaluation settings.
- This repository has not run LongLLMLingua, imported its code, reproduced its benchmarks, or verified compression fidelity on ASI Stack context packets.
- Use the source as external context-compression vocabulary, not as evidence that VCM compression is safe or adequate.

## Failure Modes

- Compression can delete the very evidence needed for verification, provenance, or authority review.
- Cost and latency improvements can hide degraded support for rare, middle-position, or contradictory evidence.
- Compression benchmarks cannot justify ASI Stack context adequacy without local before/after packets and review records.

## Book Chapters Supported

- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `context-transactions-snapshots-mounts-and-taint` (Context Transactions, Snapshots, Mounts, and Taint)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `the-efficient-asi-hypothesis` (The Efficient ASI Hypothesis)
- `resource-economics-and-token-budgets` (Resource Economics and Token Budgets)

## Claims To Add Or Update

- Use this note to ground context-compression discussion in long-context cost, latency, and adequacy tradeoffs.
- Do not claim VCM compression fidelity, token savings, latency improvements, or benchmark gains without local runs.
- Keep support state at `argument` until compression receipts, adequacy checks, benchmark traces, or accepted evidence transitions exist.

## Open Questions

- What compression receipt should record deleted evidence, retained evidence, and adequacy risk?
- Which VCM packet fixture should fail if compression removes an authority, provenance, or contradiction marker?
- How should resource-economics accounting balance token savings against verification bandwidth?
