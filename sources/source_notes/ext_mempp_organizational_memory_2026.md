# Source Note: Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents

| Field | Value |
|---|---|
| Source ID | `ext_mempp_organizational_memory_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.02002v1](https://arxiv.org/html/2610.02002v1) |
| Citation | Yehia et al. (2026), Mem++ |
| Published / updated | 2026-10-01 / 2026-10-01 |
| Review scope | Sections 3.1–3.4, 4.2–4.3, including graph temporal leakage, missing author metadata and ablation limits. |
| Storage | Authored public-safe note only; full primary HTML is an ignored local research cache. |

## Thesis

Whole dated documents can be a strong alternative to irreversible fact extraction at write time.

## Mechanisms

Stores original text and event dates, embeds and indexes it, then applies an as-of date before rank fusion. Main runs disable optional consolidation. Only supersession metadata changes; readout does not automatically enforce those links.

## Evidence

Reports organizational and conversational QA comparisons. Plain RAG wins some contradiction/bi-temporal categories; the graph variant sees additional context. Some author tags are empty because the benchmark supplies no author field.

## Failure Modes

Graph triples lack dates and can leak future information into as-of questions. Whole-text retention does not remove encoder truncation, reader-context limits or privacy/deletion obligations; no local utility or erasure result.

## Claims To Add Or Update

Add a bounded comparator through the existing owner below. Architectural core,
proof targets and experiment/support dispositions remain unchanged. The source
is evidence about its own formulation or reported envelope, not a new local
performance, safety or deployment result.

## Open Questions

When do exact documents beat extracted facts once context, provenance, retention rights and query budgets are matched?

## Book Chapters Supported

- `durable-semantic-memory-and-knowledge-lattices`

## Chapter Decision

Update the existing owner under
`new_paper_triage_scenarios/recent_frontier_2026_11_02.json` and
`research_backlog_records/recent_frontier_2026_11_02.json`. Selected passage
review only; no complete reference audit, code execution or independent model
replication. This note does not assign novelty to the ASI Stack.
