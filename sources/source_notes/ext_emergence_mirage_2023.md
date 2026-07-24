# Source Note: Are Emergent Abilities of Large Language Models a Mirage?

| Field | Value |
|---|---|
| Source ID | `ext_emergence_mirage_2023` |
| Source title | Are Emergent Abilities of Large Language Models a Mirage? |
| Ingestion date | 2026-07-24 |
| Source version / URL | NeurIPS 2023, https://proceedings.neurips.cc/paper_files/paper/2023/hash/adc98a266f45005c403b8311ca7e8bd7-Abstract-Conference.html |
| Citation label | Schaeffer, Miranda, and Koyejo (2023), Emergent Abilities Mirage |
| Published / updated | 2023-12-10 / 2023-12-10 |
| DOI | not assigned in the inspected record |
| Ingestion basis | Primary NeurIPS abstract, paper summary, and reported analyses inspected; no model output or meta-analysis reproduced. |

## Thesis

Nonlinear and discontinuous metrics can create apparently abrupt capability
transitions from smoothly changing model outputs. Emergence claims therefore
need metric sensitivity analysis.

## Mechanisms

- Model how metric choice produces apparent discontinuity.
- Re-score fixed model outputs with alternative metrics.
- Test predictions in language and vision settings.

## Evidence

The reported analyses are source evidence for the studied outputs and metrics.
They do not prove that all capability transitions are smooth or that genuinely
abrupt mechanisms cannot occur.

## Failure Modes

- One exact-match threshold used as the only signal.
- Smoothing used to erase a decision-relevant cliff.
- Metric sensitivity generalized beyond observed outputs.
- A measurement critique mistaken for a no-risk claim.

## Book Chapters Supported

- `the-efficient-asi-hypothesis`
- `capability-thresholds-and-deployment-commitments`
- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

- Capability forecasts must report continuous and operational metrics together.
- Threshold policy should remain conservative when measurement and mechanism
  explanations disagree.

## Open Questions

- Which metric families preserve operationally meaningful discontinuities?
- How should a run stop when a risk threshold is measurement-sensitive?
