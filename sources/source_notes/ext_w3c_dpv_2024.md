# Source Note: W3C Data Privacy Vocabulary v2

| Field | Value |
|---|---|
| Source ID | `ext_w3c_dpv_2024` |
| Source title | Data Privacy Vocabulary (DPV), Version 2 |
| Ingestion date | 2026-07-19 |
| Source version / URL | Community Final Specification 2024-08-01, https://www.w3.org/community/reports/dpvcg/CG-FINAL-dpv-20240801/ |
| Citation label | W3C Data Privacy Vocabularies and Controls CG (2024), DPV v2 |
| Published / updated | 2024-08-01 / 2024-08-01 |
| DOI | none |
| Review state | Specification-body reviewed. |
| Ingestion basis | Status/scope and sections on data, purpose, processing, entities, legal basis, consent, rights, risks, measures, and context were reviewed. |

## Thesis

A machine-readable vocabulary can represent what data is processed, how, why,
where, by whom, under which basis, with which rights, risks, measures, and
consent state. Representation does not establish validity or enforcement.

## Mechanisms

- Typed concepts and relations for purpose, processing, actors, rights, risk,
  measures, legal basis, recipients, and consent.
- Specific-purpose guidance and extensible identifiers.

## Evidence

This is a W3C Community Group Final Specification, not a W3C Recommendation,
law, implementation proof, or local interoperability result.

## Failure Modes

- Vocabulary theater and overbroad purposes.
- Treating a legal-basis term as a legal determination.
- Losing extensions or meanings at boundaries.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Make purpose, processing, actors, rights, risk, and measures interoperable
  transaction fields while preserving the enforcement ceiling.

## Open Questions

- Which DPV terms map losslessly to ASI Stack records?
- Which runtime evidence shows represented constraints were obeyed?
