# Source Note: Label-Only Membership Inference Attacks

| Field | Value |
|---|---|
| Source ID | `ext_choquette_choo_label_only_mia_2021` |
| Source title | Label-Only Membership Inference Attacks |
| Ingestion date | 2026-07-19 |
| Source version / URL | ICML 2021, https://proceedings.mlr.press/v139/choquette-choo21a.html |
| Citation label | Choquette-Choo et al. (2021), Label-Only Membership Inference Attacks |
| Published / updated | 2021-07 / 2021-07 |
| DOI | none |
| Review state | Paper-body and official proceedings page reviewed. |
| Ingestion basis | Attack construction, robustness/augmentation variants, experiments, confidence masking, defense evaluation, and limitations. Code was not run. |

## Thesis

Membership can be inferred from hard labels through prediction robustness, so
hiding confidence scores is not a sufficient defense.

## Mechanisms

- Query label robustness under perturbations and calibrate boundary-distance or
  augmentation behavior for membership scoring.

## Evidence

The source reports label-only attacks competitive with confidence-based attacks
and insufficient confidence masking in studied settings. Results are not reproduced.

## Failure Modes

- Evaluating only confidence-output attacks, ignoring low-FPR performance, or
  tuning a defense against the final attack.

## Book Chapters Supported

- `privacy-data-rights-and-information-flow-governance`

## Claims To Add Or Update

- Require label-only and confidence-aware probes with an independent held-out evaluator.

## Open Questions

- Which attacks remain competent for generative and agentic interfaces?
- How should rare and affected subgroups be evaluated?
