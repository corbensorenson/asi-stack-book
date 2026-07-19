# Source Note: Physical Risk Control in Foundation Model-enabled Robotics

| Field | Value |
|---|---|
| Source ID | `ext_foundation_robotics_physical_risk_2025` |
| Source title | A Comprehensive Survey on Physical Risk Control in the Era of Foundation Model-enabled Robotics |
| Ingestion date | 2026-07-19 |
| Source version / URL | arXiv:2505.12583v2, https://arxiv.org/abs/2505.12583 |
| Citation label | Kojima et al. (2025), Physical Risk Control in Foundation Model-enabled Robotics |
| Published / updated | 2025-05-19 / 2025-05-30 |
| DOI | 10.48550/arXiv.2505.12583 |
| Review state | Preliminary second-tranche audit note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official arXiv metadata and abstract inspected. The survey body, cited control literature, implementations, robots, and experiments were not ingested or reproduced locally. |

## Thesis

Foundation-model-enabled robots act in the physical world, so risk control must
cover a lifecycle broader than model-output review. The reviewed abstract
organizes this lifecycle into pre-deployment, pre-incident, and post-incident
phases and identifies open research gaps. It is a preliminary taxonomy, not a
validated controller or safety case.

## Mechanisms

- A pre-deployment phase for controls before a robot enters service.
- A pre-incident phase for controlling risk during operation before harm.
- A post-incident phase for response after an incident.
- A survey emphasis on gaps in pre-incident mitigation, physical human
  interaction, and foundation-model-specific issues.

## Evidence

The source is a survey accepted to the IJCAI 2025 Survey Track. The reviewed
basis reports its organization and conclusions but does not provide locally
checked evidence for any individual control. No physical system, controller,
interlock, fallback, runtime monitor, incident response, or safety result has
been tested in this repository.

## Failure Modes

- Treating survey coverage as proof that a control works.
- Reducing physical safety to pre-deployment model evaluation.
- Importing generic model-safety controls without checking dynamics, deadlines,
  contact, human proximity, or irreversible effects.
- Calling a simulated or source-reported outcome a local physical result.

## Book Chapters Supported

- Proposed: `embodied-agency-real-time-control-and-physical-safety`
- Existing boundary owners: `runtime-adapters-tool-permissions-and-human-approval`,
  `governed-world-models-and-reality-grounding`, and
  `governed-operations-incident-command-and-graceful-degradation`

## Claims To Add Or Update

- Use the three-phase lifecycle only as an initial literature-loading frame.
- Keep audit-specific control leases, interlocks, temporal envelopes, and
  physical-effect receipts labeled as design requirements until primary
  control literature is passage-reviewed and tests exist.
- Do not promote support or imply physical safety from this survey note.

## Open Questions

- Which primary sources validate pre-incident controls under human proximity?
- What independent stop and fallback paths remain available after sensing or
  compute loss?
- Which post-incident evidence is needed before physical operation resumes?
