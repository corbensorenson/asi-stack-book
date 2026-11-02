# Source Note: CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL

| Field | Value |
|---|---|
| Source ID | `ext_catch_reward_hacking_2026` |
| Review date | 2026-11-02 |
| Primary version | [2609.39533v3](https://arxiv.org/html/2609.39533v3) |
| Citation | Wang et al. (2026), CATCH |
| Published / updated | 2026-09-30 / 2026-10-02 |
| Review scope | Sections 3.2.2 and 4.3, Limitations; no execution or attack reproduction. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Separates a vulnerable training evaluator from a hardened execution-based audit. It also studies how monitor pressure changes the usefulness of reasoning and comments as evidence.

## Mechanisms

Train against a deliberately vulnerable proxy evaluator and separately execute a hardened audit of the underlying algorithmic task. Compare mitigation conditions while retaining the audit’s outcome labels.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The source studies controlled Qwen3-4B coding RL and reports changing monitor informativeness under optimization pressure. It explicitly leaves larger-model and natural-repository transport open. No study, code or proof was independently reproduced here.

## Failure Modes

Constructed software-wrapped algorithmic tasks and Qwen3-4B RL are the tested setting. Known-loophole gold labels do not define every real-repository failure or general deceptive intent.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `policy-optimization-and-learning-from-feedback`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
