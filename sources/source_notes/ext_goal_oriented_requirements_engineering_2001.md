# Source Note: Goal-Oriented Requirements Engineering: A Guided Tour

| Field | Value |
|---|---|
| Source ID | `ext_goal_oriented_requirements_engineering_2001` |
| Source title | Goal-Oriented Requirements Engineering: A Guided Tour |
| Ingestion date | 2026-06-29 |
| Source version / URL | DOI: 10.1109/ISRE.2001.948567, https://doi.org/10.1109/ISRE.2001.948567 |
| Citation label | van Lamsweerde (2001), Goal-Oriented Requirements Engineering |
| Published / updated | 2001 / 2001 |
| DOI | 10.1109/ISRE.2001.948567 |
| Ingestion basis | Crossref metadata inspected for the human-intent external-positioning queue; paper not vendored into this repository and no requirements-engineering tool or method reproduced. |

## Thesis

Goal-oriented requirements engineering is a direct external comparator for turning stakeholder goals, constraints, refinements, and responsibilities into explicit system requirements. It helps position the ASI Stack's intent contract as an AI-governance intake artifact rather than an isolated prompt-engineering invention.

## Mechanisms

- Treat goals as first-class requirements-engineering objects.
- Refine goals into more operational requirements and assignments.
- Use obstacles, responsibilities, alternatives, and conflicts to expose incomplete or unsafe requirements.
- Separate the requirements model from downstream implementation.

## Evidence

- The source is established requirements-engineering literature; this repository has not reproduced a requirements-engineering method, tool, case study, or formal analysis from it.
- Use it as a comparator for goal formalization and refinement, not as evidence that ASI Stack intent parsing or contract lowering works.

## Failure Modes

- Requirements models can be mistaken for actual user understanding.
- Goal refinement can hide stakeholder conflict or authority gaps.
- A formal-looking requirement can still omit stop conditions, permissions, evidence duties, or approval boundaries.
- Requirements capture does not prove downstream execution respects the captured intent.

## Book Chapters Supported

- `human-intent-as-a-formal-input` (Human Intent as a Formal Input)

## Claims To Add Or Update

- Use this source to position intent contracts beside goal-oriented requirements engineering.
- Emphasize that ASI Stack intent contracts add authority ceilings, stop conditions, evidence requirements, and re-contract triggers for AI execution.
- Do not claim source-derived support, tool reproduction, or deployed requirements validation.

## Open Questions

- Which requirements-engineering concepts should become explicit fields in the intent-contract schema?
- Should obstacles and goal conflicts become first-class residuals in the intent-intake state machine?
- What test fixture would distinguish goal refinement from unauthorized scope expansion?
