# Source Note: Model Cards for Model Reporting

| Field | Value |
|---|---|
| Source ID | `ext_model_cards_2019` |
| Source title | Model Cards for Model Reporting |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:1810.03993, https://arxiv.org/abs/1810.03993 |
| Citation label | Mitchell et al. (2019), Model Cards |
| Published / updated | 2019-01-14 / 2019-01-14 |
| DOI | 10.48550/arXiv.1810.03993 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the Project Theseus external-positioning queue; paper not vendored into this repository and no model-card workflow implemented. |

## Thesis

Model cards are an external comparator for structured model reporting. They help position the Theseus report-first lane against a known documentation pattern: a system report should name intended use, evaluated behavior, limitations, and trust-relevant context before a model or service is treated as ready for use.

## Mechanisms

- Record model identity, intended uses, factors, metrics, evaluation data, and ethical considerations.
- Make model behavior and limitations visible to downstream users.
- Separate reporting about a system from proof that the system is safe, fair, or fit for every deployment.
- Encourage standardized disclosure so reports can be compared and audited.

## Evidence

- The source proposes model cards as a reporting framework and illustrates how structured model documentation can expose intended use, performance, and limitation boundaries.
- This repository has not implemented a model-card generator, reviewed a Theseus model card, reproduced any model-card evaluation, or validated a deployed model.
- Use this source as a reporting comparator for Theseus report packets, not as a support-state promotion.

## Failure Modes

- A report can become marketing if limitations, disallowed uses, and evaluation gaps are omitted.
- Model-level reporting can hide workflow, operator, gate, residual, or replay records that matter in a governed stack.
- Standardized documentation can be mistaken for evidence that the underlying system is safe.
- A stale card can misrepresent current system behavior.

## Book Chapters Supported

- `project-theseus-as-report-first-implementation-reference` (Project Theseus as Report-First Implementation Reference)

## Claims To Add Or Update

- Use model cards to position Theseus report packets as part of a broader reporting family.
- Keep Theseus report packets broader than model cards by including gates, residuals, work-board items, replay state, publication boundaries, and non-claims.
- Do not claim that Theseus has produced or validated model cards until a public-safe artifact exists.

## Open Questions

- Should future Theseus report packets include a model-card-compatible section when a model artifact is involved?
- Which fields belong in the ASI Stack report packet but not in a conventional model card?
- What validator would reject stale or marketing-only model-card language?
