# Source Note: EngramEdit: Decoupled Knowledge Updates in LLMs through Conditional Memory

| Field | Value |
|---|---|
| Source ID | `ext_engramedit_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.10533v1](https://arxiv.org/html/2610.10533v1) |
| Citation | Cai et al. (2026), EngramEdit |
| Published / updated | 2026-10-07 / 2026-10-07 |
| Review scope | Sections 3.3, 4.1 and 6, including the ethics statement; no proof or code audit. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Provides a concrete memory-parameter update surface: edit shared n-gram embeddings across expressions with reuse-sensitive regularization while the backbone stays fixed.

## Mechanisms

Compute target conditional-memory representations across fact expressions, construct their shared n-gram mapping, and allocate joint embedding updates with reuse-weighted regularization. The backbone is fixed while the table parameters change.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

CounterFact, ZsRE and MQuAKE measure different edit and transfer properties on LongCat-Flash-Lite. The selected ethics passage explicitly separates counterfactual edit targets from verified factual truth. No study, code or proof was independently reproduced here.

## Failure Modes

Experiments use LongCat-Flash-Lite. Editing success, paraphrase transfer, unrelated knowledge and multi-hop use remain separate. Counterfactual benchmark targets are not established facts; editing is not erasure.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `data-engines-continual-learning-and-unlearning`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
