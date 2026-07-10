# Source Note: Safety Cases at AISI

| Field | Value |
|---|---|
| Source ID | `ext_aisi_safety_cases_2024` |
| Source title | Safety Cases at AISI |
| Ingestion date | 2026-07-10 |
| Source version / URL | AISI technical methodology page, 2024, https://www.aisi.gov.uk/blog/safety-cases-at-aisi |
| Citation label | AI Safety Institute (2024), Safety Cases at AISI |
| Published / updated | 2024 / 2024 |
| Ingestion basis | Official AISI page inspected for its description of safety-case structure, positive and negative evidence, countercases, uncertainty, scientific disagreement, and its warning that current safety-case sketches should not be high-confidence. No AISI process or result was reproduced in this repository. |

## Thesis

The page presents frontier-AI safety cases as structured arguments that make
uncertainty, evidence needs, and disagreement legible. It emphasizes that both
positive evidence and active searches for counterevidence matter, that the
reliability of red-team or evaluation evidence itself needs argument, and that
current AI safety-case sketches face open scientific and engineering questions.

## Mechanisms

- Make a context-specific safety argument inspectable rather than treating a
  collection of evaluations as self-interpreting.
- Include positive support and negative-evidence searches, with a record of why
  a countercase search is sufficiently capable, incentivized, and scoped.
- Preserve uncertainty about capabilities, oversight, verification, controls,
  and the appropriate degree of formal structure.
- Use the case to identify debate, assumptions, and research gaps rather than
  to conceal them behind a single confidence label.

## Evidence

- The official page describes AISI's methodological position on safety-case
  sketches, countercases, and frontier-AI uncertainty.
- It states that current sketches should not be expected to be high-confidence
  and that crucial details depend on contested scientific and experimental work.
- This repository has not constructed, independently reviewed, or validated a
  safety case. The source is a methodology and limitation comparator only.

## Failure Modes

- A positive-evidence dossier omits an active search for contradictory evidence
  or assumes the search process was adequate without support.
- A case is treated as high confidence despite unresolved theory, disagreement,
  weak evaluations, or unverified mitigations.
- Notation structure substitutes for substantive discussion of experiment
  quality, threat-model scope, or control effectiveness.
- A public case leaves no durable record of assumptions, uncertainty, dissent,
  or residual risk.

## Book Chapters Supported

- `safety-cases-and-structured-assurance` (Safety Cases and Structured Assurance)

## Claims To Add Or Update

- Use this note for countercase, negative-evidence, uncertainty, and review
  requirements in an assurance-case compilation record.
- Treat a compiled graph as a review surface that exposes dependencies, not as a
  conclusion that a system is safe.
- Do not claim high confidence, evaluation reliability, red-team adequacy,
  control efficacy, safety, readiness, or deployment authorization.

## Open Questions

- How can a book-level case make countercases and active defeaters visible
  without producing a misleading quantified risk estimate?
- Which independent review and adversarial-evaluation artifacts are minimally
  needed to judge a claim/evidence relationship?
- How should a generated case report distinguish an empty evidence field from a
  finding that directly undermines the case?
