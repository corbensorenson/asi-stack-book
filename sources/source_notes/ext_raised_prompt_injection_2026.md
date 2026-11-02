# Source Note: RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents

| Field | Value |
|---|---|
| Source ID | `ext_raised_prompt_injection_2026` |
| Review date | 2026-11-02 |
| Primary version | [2610.06401v2](https://arxiv.org/html/2610.06401v2) |
| Citation | Dhouib et al. (2026), RAISED |
| Published / updated | 2026-10-05 / 2026-10-07 |
| Review scope | Sections 3.2 and 5.2, Appendix G; selected threat-model, objective and limitation passages. |
| Storage | Authored public-safe synthesis only; primary text remains an ignored local research cache. |

## Thesis

Clean-context teacher distributions supervise both clean and injected tool histories. Useful for explaining why authorized guidance from tools should remain usable while injected instructions lose influence.

## Mechanisms

Generate tool-use trajectories with useful legitimate guidance. Distill clean-context teacher token distributions onto a student under both clean and injected histories; the teacher target remains fixed when an injection is added.

The existing chapter owns the interface interpretation; the paper does not
implement the ASI Stack governance contract.

## Evidence

The selected threat model, objective and limitations explain the security–utility comparison and teacher-quality ceiling. They do not supply an independently reproduced attack rate or general alignment result. No study, code or proof was independently reproduced here.

## Failure Modes

Self-distillation preserves the clean teacher’s mistakes too. Security, benign task completion and general utility need separate measurements; this is no general alignment or arbitrary-adaptive-attack guarantee.

## Claims To Add Or Update

Add the bounded mechanism/comparator to the existing chapter. Core claims,
formal target definitions, experiment outcomes and support states stay unchanged.

## Open Questions

Which benefits survive a matched comparison in this consumer's intended
environment, including qualification, interference, false refusal, recovery
and total cost rather than the source's headline metric alone?

## Book Chapters Supported

- `adversarial-machine-learning-and-model-attack-surface`

## Chapter Decision

Update the existing owner under
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Selected passage review does not establish generality, novelty, safety,
semantic preservation, source-method correctness or architecture superiority.
