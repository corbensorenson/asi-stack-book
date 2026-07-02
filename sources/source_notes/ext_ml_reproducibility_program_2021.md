# Source Note: Improving Reproducibility in Machine Learning Research

| Field | Value |
|---|---|
| Source ID | `ext_ml_reproducibility_program_2021` |
| Source title | Improving Reproducibility in Machine Learning Research |
| Ingestion date | 2026-06-29 |
| Source version / URL | Journal of Machine Learning Research, https://jmlr.org/papers/v22/20-303.html |
| Citation label | Pineau et al. (2021), Improving Reproducibility in Machine Learning Research |
| Published / updated | 2021 / 2021 |
| Ingestion basis | Public JMLR article page inspected for the Project Theseus external-positioning queue; article not vendored into this repository and no NeurIPS reproducibility checklist or code-review process reproduced. |

## Thesis

The NeurIPS reproducibility program is an external comparator for research reporting, code submission, checklist discipline, and reproducibility review. It helps position Theseus report-first evidence around commands, artifacts, environment notes, failure cases, and reviewer-readable claims.

## Mechanisms

- Use reproducibility checklists to make experimental claims more inspectable.
- Encourage code submission and review of artifacts that support reported results.
- Record reviewer-facing information needed to reproduce or evaluate a machine-learning claim.
- Treat reproducibility as a community process, not only an author's statement of intent.

## Evidence

- The source reports on reproducibility initiatives and lessons from NeurIPS reproducibility work.
- This repository has not run a NeurIPS-style reproducibility checklist for Theseus, submitted code for external reproducibility review, or reproduced a Theseus experiment under an external program.
- Use this source as a reproducibility and artifact-review comparator, not as evidence that Theseus has been reproduced.

## Failure Modes

- Checklists can become compliance theater if commands, artifacts, and negative cases are absent.
- Code availability does not by itself prove correctness, safety, or adequacy of a result.
- Reproducibility review can miss private data, hidden environment assumptions, or stale dependencies.
- A reproducibility program can validate a paper's artifact path without validating a broader architecture claim.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `project-theseus-as-report-first-implementation-reference` (Project Theseus as Report-First Implementation Reference)

## Claims To Add Or Update

- Use the reproducibility program to ground Theseus replay-readiness fields: command, environment, artifact checksum, expected output class, negative controls, and review decision.
- Use the reproducibility program to position support-state transitions against artifact review and checklist discipline while preserving that this repository has not undergone external reproducibility review.
- Keep Theseus report imports below support-state promotion until the relevant artifact path is public-safe and replayed or digest-verified under an accepted evidence-transition record.
- Do not claim external reproducibility review, code review, or experiment reproduction.

## Open Questions

- Which Theseus report packet fields should be required before a report can be called replay-ready?
- What negative controls should accompany the first public-safe Theseus replay lane?
- Could an external reviewer use the report packet without private project access?
