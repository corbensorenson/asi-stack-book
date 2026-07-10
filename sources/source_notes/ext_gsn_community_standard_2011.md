# Source Note: GSN Community Standard Version 1

| Field | Value |
|---|---|
| Source ID | `ext_gsn_community_standard_2011` |
| Source title | GSN Community Standard Version 1 |
| Ingestion date | 2026-07-10 |
| Source version / URL | Version 1, 2011-11-16, https://www.faa.gov/about/office_org/headquarters_offices/ang/redac/redac-sas-201503-gsn-community-standard-v1.pdf |
| Citation label | Assurance Case Working Group (2011), GSN Community Standard v1 |
| Published / updated | 2011-11-16 / 2011-11-16 |
| Ingestion basis | Primary GSN standard PDF inspected for its definitions of goals, strategies, solutions, context, assumptions, justifications, support relations, and its explicit limitation that notation documents an asserted argument rather than establishing its truth. No GSN tool, model, or assurance case was executed in this repository. |

## Thesis

Goal Structuring Notation is a graphical notation for making the structure of an
argument and its relationship to evidence explicit. It represents claims as
goals, evidence references as solutions, and the interpretive conditions of
the argument through strategies, context, assumptions, and justifications. The
standard is clear that this structure records an asserted argument; use of GSN
does not make the argument true.

## Mechanisms

- Decompose a top-level goal into scoped sub-goals through declared argument
  strategies rather than leaving inferential steps implicit.
- Attach solutions as evidence references and retain the context needed to
  interpret a goal, strategy, or evidential relationship.
- Make assumptions and justifications explicit objects that reviewers can
  inspect, challenge, or replace.
- Use support and contextual relations to expose which evidence and reasoning
  the argument depends on.

## Evidence

- The standard defines the notation and the intended relationship among goals,
  strategies, solutions, context, assumptions, and justifications.
- It states that a goal structure documents an asserted chain of reasoning and
  that the notation itself does not establish an argument's truth.
- This repository has not built or assessed a complete GSN case, verified an
  argument, or used a notation diagram as safety, readiness, or deployment
  evidence. The source is an argument-structure comparator only.

## Failure Modes

- Treating a complete-looking graph or notation-conformant document as proof
  that its top claim is true.
- Omitting assumptions, context, or defeaters so evidence is presented as more
  general than the argument permits.
- Attaching evidence without declaring the strategy or claim property that the
  evidence is supposed to support.
- Mistaking a relationship's visual clarity for independent review, valid
  threat modeling, sufficient evidence, or authorization to operate.

## Book Chapters Supported

- `safety-cases-and-structured-assurance` (Safety Cases and Structured Assurance)

## Claims To Add Or Update

- Use this note for the structure of explicit claims, argument strategies,
  evidence references, context, assumptions, and justifications in a generated
  assurance graph.
- Keep graph completeness separate from truth, evidence adequacy, safety,
  readiness, and deployment authority.
- Do not claim that an ASI Stack graph is a certified GSN case or that the
  notation validates safety, correctness, or release decisions.

## Open Questions

- Which book ledgers can compile into a public-safe assurance graph without
  duplicating the evidence or authority they already own?
- How should a structured graph represent active defeaters, residuals, and
  conflicting evidence rather than only positive support?
- What independent review, threat-model, evaluation, and control evidence would
  be required before a compiled case could support a narrowed operational claim?
