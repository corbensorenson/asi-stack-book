# Source Note: Meaningful human control: actionable properties

| Field | Value |
|---|---|
| Source ID | `ext_meaningful_human_control_actionable_2022` |
| Source title | Meaningful human control: actionable properties for AI system development |
| Ingestion date | 2026-07-19 |
| Source version / URL | AI and Ethics, https://link.springer.com/article/10.1007/s43681-022-00167-3 |
| Citation label | Siebert et al. (2022), Meaningful human control: actionable properties |
| Published / updated | 2022-05-19 / 2022-05-19 |
| DOI | 10.1007/s43681-022-00167-3 |
| Ingestion basis | Primary article abstract, four properties, methods, and limitations inspected; no local human-subjects study performed. |

## Thesis

Meaningful human control is a socio-technical property, not the presence of an
approval button. The paper operationalizes it through an explicit operating
domain, mutually compatible representations, responsibility commensurate with
authority and ability, and traceable links to responsible human action.

## Mechanisms

- Define morally loaded operating situations and their boundaries.
- Preserve compatible human and machine representations.
- Match assigned responsibility to actual authority and ability.
- Trace system actions to humans who understand their responsibility.

## Evidence

The paper provides an interdisciplinary design framework and case-based
application. It does not prove that a specific oversight design works, and this
repository has not run a human-factors evaluation.

## Failure Modes

- Nominal authority without time, information, skill, or usable controls.
- Responsibility assigned to a person who cannot affect the outcome.
- Machine representations that reviewers cannot understand or challenge.
- Oversight that exists procedurally but disappears under workload or urgency.

## Book Chapters Supported

- Proposed: `human-factors-and-meaningful-control-in-oversight`
- Existing boundary owners: `human-intent-as-a-formal-input`,
  `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

- Treat meaningful control as a measured capacity envelope.
- Record reviewer information, time, competence, authority, load, and alternatives.
- Reject approval receipts as evidence of comprehension or meaningful control.

## Open Questions

- Which workload and time-pressure thresholds invalidate an approval path?
- How can compatible representations be tested without self-report alone?
- What fallback preserves control when qualified human capacity is exhausted?
