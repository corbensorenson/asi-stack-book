# Conformal Fusion Under Missing Modalities

| Field | Value |
|---|---|
| Source ID | `ext_conformal_missing_modalities_2026` |
| Publication | Alireza Moayedikia (2026). [Primary publication](https://arxiv.org/html/2608.07183v1). |

## Thesis

Check prediction-set coverage and set size separately for each observed combination of input streams.

## Mechanisms

Calibrate prediction sets separately within groups defined by the observed input mask.

## Evidence

The method calibrates a threshold for each modality-presence pattern on the studied classification tasks.

## Failure Modes

The guarantee assumes exchangeability within the pattern. The study did not measure deployment acquisition drift.

## Book Chapters Supported

- `perception-sensor-fusion-and-observation-trust`

## Claims To Add Or Update

The chapter uses the paper as an external comparison in “How often is the true state inside the prediction set?” and retains its existing core support state.

## Open Questions

How does coverage change on the difficult episodes in which a specific sensor drops out?
