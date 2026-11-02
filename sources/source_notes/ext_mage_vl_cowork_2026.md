# Source Note: Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses

| Field | Value |
|---|---|
| Source ID | `ext_mage_vl_cowork_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.40747v1](https://arxiv.org/html/2610.40747v1) |
| Citation | Zhang et al. (2026), Mage-VL-Cowork |
| Published / updated | 2026-10-29 / 2026-10-29 |
| Review scope | Sections 3.1–3.2, 6.1 and 6.7 plus conclusion; published paper, not model-card headline alone. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

A concrete GUI/terminal policy trained from an evolved teacher harness and reusable task-generation workflows. Extra action channels can hurt the distilled student when they introduce ambiguous routing.

## Mechanisms

Evolve a fixed teacher model’s scaffold, tools, prompt and terminal environment, then distill trajectories into a GUI/terminal policy. Reusable skill workflows coordinate task instructions, setup artifacts and evaluators.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The selected controlled harness comparison contrasts teacher/student behavior with an extra channel. The OSWorld configuration has 361 tasks, two runs and a 50-step budget, excluding Google Drive; it is not permission-enforcement evidence. No study, code or proof was independently reproduced here.

## Failure Modes

The OSWorld result uses 361 tasks, excludes Google Drive, permits 50 steps and averages two runs. This configuration-specific result is not evidence of permission enforcement, general desktop safety or a drop-in runtime.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
