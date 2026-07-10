# Source Note: Mathematical Discoveries from Program Search with Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_funsearch_2024` |
| Source title | Mathematical Discoveries from Program Search with Large Language Models |
| Ingestion date | 2026-07-10 |
| Source version / URL | Nature 625, 468-475 (2024), https://doi.org/10.1038/s41586-023-06924-6 |
| Citation label | Romera-Paredes et al. (2024), Mathematical Discoveries from Program Search with Large Language Models |
| Published / updated | 2024-01-17 / 2024-01-17 |
| DOI | 10.1038/s41586-023-06924-6 |
| Ingestion basis | Primary journal article inspected for its evaluate-function specification, fixed pretrained LLM, candidate-program generation, archive, scoring loop, and stated task scope. No model, evaluator, candidate program, or reported result was reproduced in this repository. |

## Thesis

FunSearch is a bounded program-search architecture: a pretrained language
model generates candidate functions, while a user-provided evaluation function
scores them and a database retains correct candidates. It is an example of a
generator-evaluator-archive loop, not evidence that a system has a general or
self-governing improvement engine.

## Mechanisms

- Start from a user-provided evaluation function and an initial program, which
  may include a skeleton that constrains the portion of the program to evolve.
- Sample programs from an archive, prompt a pretrained code model, and evaluate
  newly generated candidate functions against the supplied specification.
- Retain correctly evaluated candidates in a program database and expose the
  highest-scoring programs under that evaluator.
- Keep the generator fixed in the reported setup; the loop searches a bounded
  program space rather than changing the foundation model itself.

## Evidence

- The article reports program-search results in its selected mathematical and
  algorithmic tasks using its own evaluator and experimental setup.
- A candidate's status is bounded by the supplied evaluation function, program
  skeleton, model, sampling budget, and task domain. The evaluator is not a
  proof of safety, generality, or downstream usefulness outside that scope.
- This repository has not run FunSearch, copied its code, called its model,
  reproduced an evaluator, or verified a scientific or algorithmic result.
  The source supplies an external comparator for bounded generator-evaluator
  loops only.

## Failure Modes

- A malformed or incomplete evaluator can reward a proxy while accepting a
  candidate that fails the intended requirement.
- Archive selection can erase failed, unsafe, costly, or narrowly overfit
  candidates if their provenance and residuals are not retained.
- Treating search output as an approved artifact can bypass independent review,
  authority controls, deployment checks, and rollback.

## Book Chapters Supported

- `open-ended-improvement-engines` (Open-Ended Improvement Engines)

## Claims To Add Or Update

- Use FunSearch to ground the bounded generator-evaluator-archive pattern and
  the need to make evaluator scope explicit.
- Distinguish search validity under a supplied evaluator from an accepted
  capability, safety, deployment, or self-improvement conclusion.
- Do not claim local program-search reproduction, mathematical discovery,
  evaluator correctness, autonomous R&D, model improvement, or ASI.

## Open Questions

- What record connects an evaluator specification to a promotion decision
  without treating the evaluator as independent evidence by default?
- How should a governed archive retain failed candidates, evaluator versions,
  resource costs, and rejection reasons?
- Which tasks can expose a public-safe negative control where a high proxy
  score still fails an independent requirement?
