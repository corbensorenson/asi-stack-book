# Source Note: Human oversight of agentic systems in practice

| Field | Value |
|---|---|
| Source ID | `ext_agentic_oversight_practice_2026` |
| Source title | Human oversight of agentic systems in practice: Examining the oversight work, challenges, and heuristics of developers using software agents |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2606.05391, https://arxiv.org/abs/2606.05391 |
| Citation label | Dhanorkar, Passi, and Vorvoreanu (2026), Human oversight of agentic systems in practice |
| Published / updated | 2026-06-03 / 2026-06-03 |
| DOI | 10.48550/arXiv.2606.05391 |
| Ingestion basis | Primary arXiv abstract, methods overview, findings, and stated limitations inspected; interview data were not reanalyzed. |

## Thesis

Experienced developers oversee software agents through a mix of a priori
control, co-planning, live monitoring, and post hoc review. Their situated
heuristics and review difficulties provide a current empirical anchor for why
oversight quality must be measured across a workflow, not inferred from a final
approval event.

## Mechanisms

- Preventive scope and environment control before execution.
- Joint planning and intervention during work.
- Real-time monitoring of agent activity.
- Post hoc inspection of outputs, diffs, and test evidence.

## Evidence

The study is exploratory and based on interviews with 17 experienced
developers. It supports hypothesis formation and instrument design, not a
population-wide causal claim or proof of any oversight protocol.

## Failure Modes

- Review becomes infeasible as output volume and complexity rise.
- Test results are mistaken for complete correctness guarantees.
- Oversight effort is hidden when productivity is measured.
- Heuristics can fail under unfamiliar tasks, time pressure, or automation bias.

## Book Chapters Supported

- Proposed: `human-factors-and-meaningful-control-in-oversight`
- Existing boundary owners: `runtime-adapters-tool-permissions-and-human-approval`,
  `labor-os-and-typed-jobs`

## Claims To Add Or Update

- Model oversight as work with measurable time, coverage, intervention, and cost.
- Separate preventive, concurrent, and retrospective control.
- Include false-confidence controls where tests or model explanations appear
  reassuring but omit consequential defects.

## Open Questions

- Which observed behaviors predict effective intervention rather than ceremony?
- How does oversight quality change with task duration and agent autonomy?
- What independent outcome measure avoids relying on reviewer confidence?
