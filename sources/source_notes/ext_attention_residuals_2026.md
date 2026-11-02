# Source Note: Attention Residuals

| Field | Value |
|---|---|
| Source ID | `ext_attention_residuals_2026` |
| Review date | 2026-11-02 |
| Primary version | [2603.15031v1](https://arxiv.org/pdf/2603.15031v1) |
| Citation | Kimi Team (2026), Attention Residuals |
| Published / updated | 2026-03-16 / 2026-03-16 |
| Review scope | PDF Sections 3.1–3.2 and the large-scale training discussion around Section 5.2. arXiv HTML is an incomplete conversion; use the primary PDF. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Adds learned softmax aggregation over network depth; its block variant trades fine-grained access for lower activation-storage and communication burden.

## Mechanisms

Use a learned pseudo-query and normalized keys to form softmax weights over earlier layer outputs. Block AttnRes sums local layer outputs and attends across fewer block representations, exchanging fine-grained access for lower memory/communication burden.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The paper compares a trained Block AttnRes architecture with its baseline and discusses large-scale pretraining. The incomplete HTML is not the review basis; the selected primary PDF supplies these passages. No study, code or proof was independently reproduced here.

## Failure Modes

This is a trained architecture, not a demonstrated post-hoc upgrade to any checkpoint. Depth attention and sequence attention have different scaling variables; quoted overhead needs its distributed implementation and workload.

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
