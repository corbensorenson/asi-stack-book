# Source Note: Manifold-Constrained Hyper-Connections for Parameter-Efficient Finetuning

| Field | Value |
|---|---|
| Source ID | `ext_mhc_peft_2026` |
| Review date | 2026-11-02 |
| Primary version | [2607.18130v2](https://arxiv.org/html/2607.18130v2) |
| Citation | Oldenburg et al. (2026), mHC Finetuning |
| Published / updated | 2026-07-20 / 2026-10-07 |
| Review scope | Sections 3–5 and Appendix A; current October 7 revision, not the older abstract. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

A necessary counterpoint: frozen-backbone finetuning can benefit from retaining identity residual mixing and learning read/write access instead. Residual topology is not one universally superior recipe.

## Mechanisms

Wrap frozen Transformer branches in multiple residual streams and adapt read/write gates or mixing. Compare static/dynamic and identity-preserving variants while accounting for activation storage.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The current revision reports that identity mixing helps the studied finetuning configurations and that standalone mHC does not outperform established PEFT baselines overall. Cross-family hardware differences limit timing and energy comparison. No study, code or proof was independently reproduced here.

## Failure Modes

Standalone mHC does not beat established PEFT baselines overall. Few trainable parameters do not eliminate multi-stream activation costs; LoRA and mHC timing/energy measurements use different GPU types.

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
