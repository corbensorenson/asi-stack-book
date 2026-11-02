# Source Note: Reinforced Planning with Latent World Models

| Field | Value |
|---|---|
| Source ID | `ext_reinforced_planning_rp1_2026` |
| Review date | 2026-11-02 |
| Primary version | [2608.18669v2](https://arxiv.org/html/2608.18669v2) |
| Citation | Sommer and Schilling (2026), Reinforced Planning |
| Published / updated | 2026-08-19 / 2026-09-27 |
| Review scope | v2 Sections 4, 7.4–7.5 and 8, compared with v1; September 27 revision narrows claims and clarifies selection costs. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Learns a multi-step plan-update rule using a critic, imagined rollouts and gradients through a world model. Distinguishes improving search from learning a direct action policy.

## Mechanisms

Learn a goal-conditioned critic and a plan-update operator. The operator consumes the current action sequence, predicted value and gradient through a differentiable world model rather than imitating a fixed optimizer.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The revised study distinguishes offline training from simulator-based checkpoint selection, and reports model-error exploitation and partial Dyna correction. Query counts, latency and complete training costs remain separate. No study, code or proof was independently reproduced here.

## Failure Modes

Planner training can be offline while checkpoint selection still uses simulator episodes. It can exploit world-model errors and needs retraining across model/horizon changes. Query reduction is not the same as latency or complete training cost.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `planning-as-a-control-layer`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
