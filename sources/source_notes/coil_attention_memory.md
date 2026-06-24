# Source Note: Coil Attention and Memory

| Field | Value |
|---|---|
| Source ID | `coil_attention_memory` |
| Source title | Coil Attention and Memory |
| Ingestion date | 2026-06-24 |
| Source version / URL | Public project source in inventory |
| Ingestion basis | local project source text; raw source text is not copied here |

## Thesis

Coil Attention and Memory frames cyclic memory, KV-cache freshness, sparse-attention coverage, recurrence schedules, loop-exit certificates, and alias diagnostics as structural contracts for hybrid attention systems. It does not propose replacing all attention with fixed circles; the target is a hybrid of local attention, global/content-gated attention, selected coil paths, and auditable recurrence schedules.

## Mechanisms

- Model cyclic memory slots as finite modulo addresses while tracking winding/provenance to expose aliasing.
- Use KV-cache ring-buffer certificates to reason about retained tokens, stale reads, duplicate-free requests, sink-window policy, and live-window slot coverage.
- Use stride/orbit coverage to decide which positive lags a sparse-attention plan covers, which gaps remain, and what local-window repair would be needed.
- Use recurrence schedules to expose loop depth, active/inactive token counts, exit steps, work savings, periodic shifts, and overthinking boundaries.
- Separate fixed-coil reachability, hand-coded route selection, learned finite route tables, and hybrid local+coil coverage fixtures.

## Evidence

- The source is a proof-linked AI application paper with Lean theorem references, Python/CLI fixture descriptions, and explicit non-claims.
- It describes structural contracts and deterministic synthetic fixtures for cyclic memory, KV-cache freshness, candidate reachability, sparse-attention coverage, and recurrence work budgets.
- The source repeatedly states that these fixtures are not evidence of better retrieval, language modeling, long-context scaling, speed, memory, or model quality.
- No Circle sidecar tests, contract generators, Lean builds, or learned-model experiments were run from this repo as part of this note.

## Failure Modes

- Treating a cyclic memory slot as proof of useful language-model memory.
- Hiding alias collisions by recording only residue without winding/provenance.
- Replacing full or content-gated attention with fixed sparse paths where arbitrary dependencies matter.
- Treating recurrence schedules as proof of reasoning quality, context-length extension, speed, or parameter efficiency.
- Ignoring stale reads, duplicate requests, sink-window assumptions, or ordinary KV-cache implementation details.

## Book Chapters Supported

- `coil-attention-cyclic-memory-and-recurrence-contracts` (Coil Attention, Cyclic Memory, and Recurrence Contracts)

## Claims To Add Or Update

- The source can support source-derived discussion of cyclic memory contracts, KV-cache freshness checks, sparse-attention coverage, recurrence work-budget accounting, and alias visibility.
- It should not be used to claim learned model-quality improvements without named workloads, baselines, metrics, and reports.

## Open Questions

- Which recurrence and KV-cache facts should become ASI Stack Lean targets versus external Circle citations?
- How should cyclic memory chapters require winding/provenance when residue slots are reused?
- What is the first public-safe sparse-attention fixture worth implementing in this repo?

