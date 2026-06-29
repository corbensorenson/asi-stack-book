# Source Note: Robust Layered Control System

| Field | Value |
|---|---|
| Source ID | `ext_subsumption_architecture_1986` |
| Source title | A Robust Layered Control System for a Mobile Robot |
| Ingestion date | 2026-06-29 |
| Source version / URL | MIT AI Memo PDF, https://people.csail.mit.edu/brooks/papers/AIM-864.pdf |
| Citation label | Brooks (1986), Robust Layered Control System |
| Published / updated | 1986 / 1986 |
| DOI | 10.1109/JRA.1986.1087032 |
| Ingestion basis | Public MIT-hosted paper PDF metadata and bibliographic DOI inspected for the opener external-positioning queue; paper not vendored into this repository and no robot-control architecture reproduced. |

## Thesis

Brooks' layered robot-control architecture is an external comparator for decomposing intelligent behavior into interacting layers rather than centralizing behavior in one monolithic controller. It helps position the ASI Stack's stack frame as part of a broader systems-architecture lineage.

## Mechanisms

- Decompose robot behavior into layered control systems.
- Let layers interact so lower-level behavior can support higher-level behavior.
- Emphasize robust situated behavior through architectural decomposition.
- Avoid a single central representation or monolithic controller as the only unit of analysis.

## Evidence

- The source reports a layered control architecture for mobile robots under its own robotics context.
- This repository has not reproduced the robot system, implemented subsumption control, or shown ASI Stack behavior in robotics.
- Use this source as layered-control architecture lineage, not as evidence for ASI Stack capability or safety.

## Failure Modes

- Layered control lineage can be overgeneralized from robotics to ASI without new evidence.
- Behavior-layer success does not imply evidence ledgers, authority controls, or governed self-improvement.
- Layer interactions can still create hidden authority or debugging problems if records are missing.
- Historical architecture analogies can obscure the need for current tests and proofs.

## Book Chapters Supported

- `asi-is-a-stack-not-a-model` (ASI Is a Stack, Not a Model)

## Claims To Add Or Update

- Use Brooks' layered-control work to show that decomposition into interacting layers is established systems architecture vocabulary.
- Keep the ASI Stack claim narrower: governed AI layers need explicit authority, evidence, rollback, and support-state controls beyond layered behavior.
- Do not claim robotics reproduction or subsumption implementation.

## Open Questions

- Which ASI Stack layer-boundary fields are absent from classical layered-control architectures?
- Would a future robotics or embodied-agent slice expose useful handoff and authority failures?
- How should low-level behavior layers inherit or refuse higher-level authority?
