# Source Note: Gemini Robotics

| Field | Value |
|---|---|
| Source ID | `ext_gemini_robotics_2025` |
| Source title | Gemini Robotics: Bringing AI into the Physical World |
| Ingestion date | 2026-07-24 |
| Source version / URL | arXiv:2503.20020, https://arxiv.org/abs/2503.20020 |
| Citation label | Gemini Robotics Team et al. (2025), Gemini Robotics |
| Published / updated | 2025-03-25 / 2025-03-25 |
| DOI | 10.48550/arXiv.2503.20020 |
| Ingestion basis | Primary technical-report abstract and metadata inspected; no model, robot, demonstration, or safety evaluation reproduced. |

## Thesis

Vision-language-action and embodied-reasoning models show how a general model
can connect perception, spatial reasoning, instruction following, and direct
robot control. That integration raises rather than removes the need for typed
perception, control, and safety boundaries.

## Mechanisms

- Extend a multimodal foundation model into action generation.
- Use embodied reasoning for detection, pointing, trajectories, grasps, and
  multi-view correspondence.
- Fine-tune for new tasks and robot embodiments.

## Evidence

All capability and safety results are source-reported. The paper is a capability
and integration comparator, not independent assurance or local embodiment
evidence.

## Failure Modes

- Open-vocabulary competence generalized beyond tested embodiments.
- Semantic instruction success hiding timing, force, or contact hazards.
- Safety evaluation coupled to the same development organization or models.
- Adaptation invalidating prior control envelopes.

## Book Chapters Supported

- `embodied-agency-real-time-control-and-physical-safety`
- `perception-sensor-fusion-and-observation-trust`

## Claims To Add Or Update

- Generalist robotics models belong behind explicit observation and control
  contracts.
- Embodiment transfer must expire prior safety evidence unless equivalence is
  demonstrated.

## Open Questions

- Which report dimensions can be independently reproduced on low-energy
  hardware?
- How should open-vocabulary commands be narrowed into force/space/time leases?
