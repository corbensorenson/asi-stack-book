# Source Note: Extracting Training Data from Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_carlini_training_data_extraction_2021` |
| Source title | Extracting Training Data from Large Language Models |
| Ingestion date | 2026-07-19 |
| Source version / URL | USENIX Security 2021, https://www.usenix.org/conference/usenixsecurity21/presentation/carlini-extracting |
| Citation label | Carlini et al. (2021), Extracting Training Data from Large Language Models |
| Published / updated | 2021-08 / 2021-08 |
| DOI | none |
| Review state | Paper-body and official proceedings page reviewed. |
| Ingestion basis | Threat model, generation/ranking attack, GPT-2 experiments, memorization analysis, ethics, and limitations. Code was not run. |

## Thesis

Black-box generation and ranking can recover memorized training sequences,
including rare and personally identifying content, so raw-data access control
is insufficient.

## Mechanisms

- Generate candidates, rank with likelihood/reference/compression signals, and
  validate likely memorized content.

## Evidence

The authors report hundreds of verbatim GPT-2 sequences, including some present
in one training document. This is not proof that every model or the local stack leaks.

## Failure Modes

- Rare-sequence extraction, weak attack evaluation, censored attack attempts,
  and public-data-is-harmless assumptions.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`
- `data-engines-continual-learning-and-unlearning`

## Claims To Add Or Update

- Use strong extraction attacks and canary positive controls while preserving
  configuration-specific ceilings.

## Open Questions

- Which current attacks provide a competent lower bound on leakage?
- What defenses reduce leakage without unacceptable utility loss?
