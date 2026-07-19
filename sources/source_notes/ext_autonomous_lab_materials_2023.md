# Source Note: A-Lab Autonomous Materials Laboratory

| Field | Value |
|---|---|
| Source ID | `ext_autonomous_lab_materials_2023` |
| Source title | An autonomous laboratory for the accelerated synthesis of inorganic materials |
| Ingestion date | 2026-07-19 |
| Source version / URL | Corrected Nature article, https://www.nature.com/articles/s41586-023-06734-w; 2026 author correction, https://doi.org/10.1038/s41586-025-09992-y |
| Citation label | Szymanski et al. (2023), A-Lab |
| Published / updated | 2023-11-29 / 2026-01-19 |
| DOI | 10.1038/s41586-023-06734-w |
| Review state | Preliminary second-tranche audit note; the proposed chapter remains provisionally unadmitted. |
| Ingestion basis | Corrected official Nature abstract, selected article-page passages describing the closed loop and target scope, and the official 2026 author correction inspected. The supplementary files, code, data, diffraction patterns, instruments, robotics, and laboratory run were not ingested or reproduced locally. |

## Thesis

A-Lab is a bounded materials-domain example of a closed experimental loop that
combines computation, historical literature data, machine learning, active
learning, and robotics. The corrected article reports 36 realized compounds
from 57 targets over 17 days. This supports a preliminary application case for
the audit's general-control-plane test; it does not establish a domain-general
scientific-discovery architecture.

## Mechanisms

- Select air-stable target materials from computational screening inputs.
- Propose synthesis recipes using models trained on historical literature data.
- Execute solid-state powder synthesis with robotics.
- Characterize products using X-ray diffraction and machine-learning analysis.
- Use active learning to propose follow-up recipes after unsuccessful attempts.

## Evidence

The corrected official article reports 36 realized compounds among 57 targets.
The 2026 author correction states that manual re-analysis confirmed 36 of 40
originally reported successes while four were inconclusive, removed one target
mistakenly present in training data, and clarified that “new” meant new to the
prediction platform rather than necessarily new to science. No synthesis,
identification, success rate, autonomy, or transfer result has been reproduced
here.

## Failure Modes

- Treating one materials workflow as a domain-general experimental control plane.
- Treating an instrument or automated classifier return as scientific truth.
- Hiding inconclusive identifications, failed targets, contamination, or
  corrected denominators.
- Conflating novelty to a platform with novelty to science.
- Treating a corrected source-reported result as a local laboratory result.

## Book Chapters Supported

- Provisionally proposed: `scientific-discovery-and-experimental-governance`
- Existing boundary owners: `data-engines-continual-learning-and-unlearning`,
  `benchmark-ratchets-and-anti-goodhart-evidence`,
  `artifact-graphs-audit-logs-and-replay`, and
  `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

- Use A-Lab as a bounded, corrected materials-domain case study.
- Preserve target, attempt, failure, inconclusive, training-overlap, instrument,
  analysis, and correction denominators in any later packet.
- Require the audit's general-control-plane test before chapter admission; an
  application success does not by itself establish a reusable control plane.

## Open Questions

- Which artifacts and invariants generalize beyond materials synthesis?
- How should instrument uncertainty and inconclusive identification block a
  scientific claim?
- What independent replication and dual-use review are required before a
  result enters the evidence ledger?
