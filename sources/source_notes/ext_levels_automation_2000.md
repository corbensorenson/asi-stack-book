# Source Note: A Model for Types and Levels of Human Interaction with Automation

| Field | Value |
|---|---|
| Source ID | `ext_levels_automation_2000` |
| Source title | A Model for Types and Levels of Human Interaction with Automation |
| Ingestion date | 2026-07-03 |
| Source version / URL | https://dl.acm.org/doi/10.1109/3468.844354 |
| Citation label | Parasuraman, Sheridan, and Wickens (2000), Types and Levels of Automation |
| Published / updated | 2000 |
| DOI | 10.1109/3468.844354 |
| Ingestion basis | Primary metadata/abstract record inspected; paper not vendored or reproduced. |

## Thesis

Human oversight degradation should be modeled at the right level of automation.
Parasuraman, Sheridan, and Wickens separate automation across information
acquisition, information analysis, decision/action selection, and action
implementation. For the ASI Stack, that means a runtime adapter cannot ask for
"human approval" generically. It should name which level the human is approving:
evidence intake, interpretation, decision choice, or external effect.

## Mechanisms

- Decompose approval by automation function rather than treating the human as a
  single end-stage check.
- Preserve different evidence requirements for analysis approval, action
  selection approval, and execution approval.
- Use the decomposition to detect automation bias: a reviewer who only sees the
  system's recommendation may not be independently checking the evidence.

## Evidence

This source provides external taxonomy and comparator grounding. The book does
not reproduce the paper's model empirically or claim that its own adapter
service implements every level.

## Failure Modes

- Collapsing information, decision, and action approval into one approval
  click.
- Treating a user confirmation of intent as approval of downstream execution.
- Losing the ability to audit which level of automation the human actually
  reviewed.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`
- `human-intent-as-a-formal-input`

## Claims To Add Or Update

- Distinguish intent approval, evidence approval, action-selection approval,
  and effect approval in runtime-adapter prose and future fixtures.

## Open Questions

- Which adapter schemas should carry an explicit automation-level field?
- How should reader-facing prose explain automation level without turning the
  chapter into a human-factors survey?
