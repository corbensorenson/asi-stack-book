# Source Note: mHC: Manifold-Constrained Hyper-Connections

| Field | Value |
|---|---|
| Source ID | `ext_mhc_2025` |
| Review date | 2026-11-02 |
| Primary version | [2512.24880v2](https://arxiv.org/html/2512.24880v2) |
| Citation | Xie et al. (2026 revision), mHC |
| Published / updated | 2025-12-31 / 2026-01-05 |
| Review scope | Sections 4.1–4.3 and 6; method and infrastructure claims, not independent theorem verification. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Adds constrained mixing across multiple residual streams, making network connectivity a design axis beyond token mixing, objectives and expert selection.

## Mechanisms

Expand residual streams and parameterize their read, write and mixing operations. Sinkhorn–Knopp iterations approximate the constrained mixer; custom fusion, recomputation and communication scheduling address its systems overhead.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The selected passages give an ideal constrained-mapping rationale and a specialized infrastructure implementation. Neither a whole-network stability proof nor deployment cost equivalence was independently checked. No study, code or proof was independently reproduced here.

## Failure Modes

Doubly stochastic residual mixing is a scoped mathematical constraint, not a guarantee of whole-network stability or behavior. Efficiency depends on specialized infrastructure. Read with the finetuning counterexample below.

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
