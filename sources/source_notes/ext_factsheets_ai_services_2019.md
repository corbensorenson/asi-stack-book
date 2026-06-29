# Source Note: FactSheets for AI Services

| Field | Value |
|---|---|
| Source ID | `ext_factsheets_ai_services_2019` |
| Source title | FactSheets: Increasing Trust in AI Services through Supplier's Declarations of Conformity |
| Ingestion date | 2026-06-29 |
| Source version / URL | arXiv:1808.07261, https://arxiv.org/abs/1808.07261 |
| Citation label | Arnold et al. (2019), FactSheets for AI Services |
| Published / updated | 2019-02-07 / 2019-02-07 |
| DOI | 10.48550/arXiv.1808.07261 |
| Ingestion basis | Public arXiv abstract and metadata inspected for the Project Theseus external-positioning queue; paper not vendored into this repository and no AI-service FactSheet implemented. |

## Thesis

AI service FactSheets are an external comparator for supplier declarations and trust-relevant service documentation. They help position Theseus report packets as explicit declarations about what a service, report, gate, or artifact claims, what it omits, and which evidence supports that declaration.

## Mechanisms

- Record supplier declarations about AI service properties and trust-relevant facts.
- Standardize documentation so service consumers can inspect and compare claims.
- Separate declared properties from unsupported assumptions.
- Encourage documentation practices that make governance and accountability review easier.

## Evidence

- The source proposes FactSheets as a structured reporting mechanism for AI services and supplier declarations of conformity.
- This repository has not created a Theseus FactSheet, audited an AI service, reproduced a compliance workflow, or validated a supplier declaration.
- Use this source as a service-reporting comparator, not as evidence that Theseus reports are complete or externally certified.

## Failure Modes

- Supplier declarations can overstate evidence if non-claims and missing artifacts are absent.
- Service-level documentation can hide lower-level data, model, workflow, operator, and replay boundaries.
- A FactSheet can become stale when the service changes.
- Conformity language can be mistaken for independent certification.

## Book Chapters Supported

- `project-theseus-as-report-first-implementation-reference` (Project Theseus as Report-First Implementation Reference)

## Claims To Add Or Update

- Use FactSheets to position Theseus report packets as supplier-style declarations with explicit non-claims and evidence references.
- Keep report-first Theseus claims narrower than service-level trust unless public-safe artifacts, replay commands, and review decisions exist.
- Do not claim AI-service conformity, certification, or deployment trust from this source.

## Open Questions

- Which Theseus packet fields should be phrased as supplier declarations rather than internal implementation notes?
- What review record would separate self-declared Theseus report facts from independent external review?
- How should stale declarations trigger downgrade, residual, or revalidation states?
