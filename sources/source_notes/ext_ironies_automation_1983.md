# Source Note: Ironies of Automation

| Field | Value |
|---|---|
| Source ID | `ext_ironies_automation_1983` |
| Source title | Ironies of Automation |
| Ingestion date | 2026-07-03 |
| Source version / URL | https://www.sciencedirect.com/science/article/pii/0005109883900468 |
| Citation label | Bainbridge (1983), Ironies of Automation |
| Published / updated | 1983 |
| DOI | 10.1016/0005-1098(83)90046-8 |
| Ingestion basis | Primary metadata/abstract record inspected; paper not vendored or reproduced. |

## Thesis

Human oversight degradation fits the classic automation irony: automation can
move the human from ordinary operation into a harder supervisory or abnormal
condition role. In the ASI Stack, a human approval gate is therefore not a
simple safety add-on. It is a component whose job can become harder exactly
because the automation handles the easy cases.

## Mechanisms

- Automation can leave humans responsible for rare, high-stakes, or abnormal
  interventions.
- Supervisory control can degrade if the human loses context before being
  asked to intervene.
- Approval gates need review context, escalation paths, and residual ownership
  rather than only an approve/reject button.

## Evidence

This source is used as external conceptual grounding for automation-supervision
failure modes. No local operator study, deployed approval service, or live
human-factors result is claimed.

## Failure Modes

- Assuming automation removes the need for skilled human judgment.
- Asking a fatigued reviewer to catch rare failures after context has been
  stripped away.
- Treating after-the-fact human approval as proof of real-time control.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`
- `evidence-states-and-claim-discipline`
- `human-factors-and-meaningful-control-in-oversight`

## Claims To Add Or Update

- Add the automation-irony objection to human approval: the gate may become
  weakest when the system is most automated and context has already been
  compressed away.

## Open Questions

- Which adapter classes should require human review before execution rather
  than post-hoc review?
- How should the stack preserve enough context for a reviewer without creating
  long-context theater?
