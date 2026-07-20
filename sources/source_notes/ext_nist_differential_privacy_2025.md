# Source Note: NIST SP 800-226

| Field | Value |
|---|---|
| Source ID | `ext_nist_differential_privacy_2025` |
| Source title | Guidelines for Evaluating Differential Privacy Guarantees |
| Ingestion date | 2026-07-19 |
| Source version / URL | Final NIST SP 800-226, https://csrc.nist.gov/pubs/sp/800/226/final |
| Citation label | Near et al. (2025), NIST SP 800-226 |
| Published / updated | 2025-03-06 / 2025-03-06 |
| DOI | 10.6028/NIST.SP.800-226 |
| Review state | Final publication body reviewed for the admitted argument chapter. |
| Ingestion basis | Official final PDF reviewed at the Executive Summary; Sections 2--7 on privacy claims, the DP pyramid, mathematical, implementation, system, and operational hazards, and evaluation workflow; appendices and terminology. Supplemental notebooks and implementations were not run locally. |

## Thesis

Differential privacy is a mathematical framework for quantifying privacy loss
when an entity's data appears in a dataset, but evaluating a software claim
requires attention to implementation considerations and privacy hazards. The
reviewed NIST publication supplies an evaluation frame, not a local
privacy guarantee or a complete data-rights regime.

## Mechanisms

- Quantify privacy loss to entities represented in a dataset.
- Organize evaluation considerations through a differential-privacy pyramid.
- Identify hazards that can arise when the mathematical framework is realized
  in software.
- Provide practitioner-oriented guidance across backgrounds.

## Evidence

SP 800-226 is official NIST guidance. Its pyramid and hazard analysis distinguish
mathematical, implementation, system, and operational claims; it does not demonstrate that any local system
implements differential privacy correctly. No parameter selection, accountant,
attack evaluation, utility measurement, notebook, or compliance mapping was
performed here.

## Failure Modes

- Treating a mathematical label as evidence of a correct implementation.
- Hiding implementation hazards, assumptions, composition, or affected units.
- Treating differential privacy as equivalent to consent, purpose limitation,
  correction, export, deletion, or group privacy.
- Claiming legal compliance from technical guidance.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- Existing boundary owners: `security-kernel-and-digital-scifs`,
  `data-engines-continual-learning-and-unlearning`, and
  `context-transactions-snapshots-mounts-and-taint`

## Claims To Add Or Update

- Use SP 800-226 as a paper-body-reviewed differential-privacy evaluation source.
- Require the definition, privacy unit, adjacency, implementation, system,
  composition, parameters, and operational context to accompany a DP claim.
- Keep privacy engineering, legal rights, and compliance claims separate.

## Open Questions

- Which unit of privacy and neighboring relation matches each data flow?
- How should privacy loss compose across training, memory, audit, and sharing?
- Which tests distinguish a claimed guarantee from an implementation hazard?
