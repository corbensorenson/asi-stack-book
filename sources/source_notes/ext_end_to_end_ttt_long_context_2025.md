# Source Note: End-to-End Test-Time Training for Long Context

| Field | Value |
|---|---|
| Source ID | `ext_end_to_end_ttt_long_context_2025` |
| Review date | 2026-11-02 |
| Primary version | [2512.23675v2](https://arxiv.org/html/2512.23675v2) |
| Citation | Tandon et al. (2025), End-to-End Test-Time Training |
| Published / updated | 2025-12-29 / 2025-12-31 |
| Review scope | Sections 2.1–2.3, 3.7, and abstract experiment envelope. Selected derivation and timing limitations; no kernel/code execution. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Meta-learn a model initialization for next-token updates on the context supplied at inference.

## Mechanisms

Uses sliding-window attention and adaptive MLP weights. The outer training objective differentiates through inner context updates; mini-batches address update efficiency and stability. This differs from updating a memory database.

## Evidence

Reports 3B-model/164B-token experiments and H100 prefill timing. The 2.7-times comparison at 128K is a prefill result; decode is discussed compositionally rather than separately benchmarked.

## Failure Modes

Training latency remains a limitation: the reported implementation is slower than full attention at short context, despite favorable long-context prefill. Fixed per-step state/latency does not make total context processing constant cost or guarantee task retention.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

When does adaptive-weight context memory repay update and training costs under realistic workloads and isolation policies?

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
