# Source Note: Liquid Time-constant Networks

| Field | Value |
|---|---|
| Source ID | `ext_liquid_time_constant_networks_2021` |
| Source title | Liquid Time-constant Networks |
| Ingestion date | 2026-07-15 |
| Source version / URL | AAAI 2021, https://doi.org/10.1609/aaai.v35i9.16936 |
| Ingestion basis | Primary paper abstract and model/evaluation sections reviewed; no reproduction. |

## Thesis

Liquid Time-constant Networks use input-dependent continuous-time dynamics to
create compact recurrent models for time-varying signals.

## Mechanisms

- Continuous-time hidden-state dynamics.
- Input-dependent time constants and bounded dynamics analysis.
- Numerical integration for irregular or continuous observations.

## Evidence

The source reports time-series and control-related comparisons. No local liquid
network or continuous-time benchmark exists.

## Failure Modes

- Solver cost and numerical error can dominate compact parameter counts.
- Continuous-time inductive bias may not transfer to language or exact tasks.
- Stability results can be mistaken for semantic or safety guarantees.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Include continuous-time dynamics where irregular-time workloads justify them.
- Account for solver tolerances, steps, latency, and error in total cost.

## Open Questions

- Which real control or sensor tasks justify a continuous-time kernel?
- How should checkpoint and replay handle solver and floating-point state?
