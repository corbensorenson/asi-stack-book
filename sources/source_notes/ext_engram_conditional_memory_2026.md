# Source Note: Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_engram_conditional_memory_2026` |
| Review date | 2026-11-02 |
| Primary version | [2601.07372v2](https://arxiv.org/html/2601.07372v2) |
| Citation | Cheng et al. (2026), Engram |
| Published / updated | 2026-01-12 / 2026-07-12 |
| Review scope | Sections 2.2–2.5 and 6.4; mechanism and hardware-bound timing scope. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Adds learned, hashed n-gram lookup and context-dependent gating as an axis alongside conditional computation. Distinguish this model component from document retrieval and agent episodic memory.

## Mechanisms

Normalize token IDs, hash multiple n-gram orders into learned tables, gate retrieved embeddings with the current hidden state, and apply a short causal convolution. Addresses are predictable before the layer executes, enabling overlapped host-memory prefetch.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The selected system experiment uses a large offloaded table on dense backbones in a prototype harness. This bounds the inference-cost observation; the source’s broader modeling results were not independently reproduced. No study, code or proof was independently reproduced here.

## Failure Modes

Constant-time addressing is not constant physical cost. The reported CPU-offload throughput experiment uses a specific prototype, dense backbones and workload; it is not a general MoE serving result.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
