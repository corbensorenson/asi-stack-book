# Source Note: Simulated Control Evals

| Field | Value |
|---|---|
| Source ID | `ext_simulated_control_evals_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.31593v1](https://arxiv.org/html/2610.31593v1) |
| Citation | Olmo, Zhang and Tracy (2026), Simulated Control Evals |
| Published / updated | 2026-10-22 / 2026-10-22 |
| Review scope | Sections 2.1–2.3 and 4; simulator access, sampling denominator and trust/transfer limitations. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Ground tool-response simulations in honest trajectories and code snapshots, then compare predicted safeguard performance against actual execution. Directly relevant to the simulation-to-evidence boundary.

## Mechanisms

Simulate tool responses using an honest reference trajectory and read access to an environment snapshot. Compare simulated control metrics with repeated executed task pairs and a distinct control setting; separate bias, run variance and task sampling.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The paper calibrates predictions primarily against LinuxArena execution. Its selected limitations retain trusted-simulator assumptions, distinguish realism from control fidelity and leave broad deployment transfer unresolved. No study, code or proof was independently reproduced here.

## Failure Modes

Validated primarily on LinuxArena and assumes a trusted simulator. Plausibility and low discriminability do not establish control-relevant fidelity. Task-pair draws include repeated selections; these are not independent worlds.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `scalable-oversight-and-adversarial-ai-control`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
