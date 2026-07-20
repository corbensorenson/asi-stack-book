# Source Note: Regulation (EU) 2016/679

| Field | Value |
|---|---|
| Source ID | `ext_eu_gdpr_2016` |
| Source title | Regulation (EU) 2016/679 (General Data Protection Regulation) |
| Ingestion date | 2026-07-19 |
| Source version / URL | Official EUR-Lex text, https://eur-lex.europa.eu/eli/reg/2016/679 |
| Citation label | European Parliament and Council (2016), Regulation (EU) 2016/679 |
| Published / updated | 2016-04-27 / text reviewed 2026-07-19 |
| DOI | none |
| Review state | Official legal text passage-reviewed; no legal interpretation or applicability decision. |
| Ingestion basis | Articles 5--7, 12--22, 25, 30, 35, and 89 plus Recitals 39, 50, and 58--68 were reviewed. |

## Thesis

Within its scope, the Regulation binds personal-data processing to principles,
a lawful basis, accountability, design obligations, and qualified rights. Its
exceptions and context make a universalized checklist unsafe.

## Mechanisms

- Purpose limitation, minimization, accuracy, storage limitation, and accountability.
- Consent conditions and other bases for processing.
- Access, rectification, erasure, restriction, portability, objection, design,
  records, impact assessment, notifications, and qualified exceptions.

## Evidence

EUR-Lex is the authoritative EU legal source. It defines requirements and
rights; it does not show that any ASI Stack system satisfies them.

## Failure Modes

- Treating consent as the only authority or as irrevocable.
- Omitting exceptions, jurisdiction, controller role, or compatibility tests.
- Claiming compliance from a schema, deletion action, or technical mechanism.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- Boundaries: `data-engines-continual-learning-and-unlearning`, `governance-rights-fork-exit-and-audit`

## Claims To Add Or Update

- Record claimed basis, jurisdiction, purpose, retention, recipients, rights,
  exceptions, and accountability explicitly.
- Never state compliance without competent jurisdiction-specific review.

## Open Questions

- Which jurisdictions and roles apply to each deployed flow?
- How should conflicting rights and cross-border duties be routed?
