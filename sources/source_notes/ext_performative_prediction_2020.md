# Source Note: Performative Prediction

| Field | Value |
|---|---|
| Source ID | `ext_performative_prediction_2020` |
| Source title | Performative Prediction |
| Authors | Juan C. Perdomo, Tijana Zrnic, Celestine Mendler-Dunner, and Moritz Hardt |
| Venue / year | ICML, PMLR 119, 2020 |
| Source URL | https://proceedings.mlr.press/v119/perdomo20a.html |
| Ingestion date | 2026-08-14 |
| Ingestion basis | Official PMLR metadata, abstract, and primary paper reviewed; no result reproduced. |

## Thesis

When a prediction informs a decision, deployment can change the distribution on which the predictor is later evaluated. The paper formalizes that dependency with a model-indexed distribution map and distinguishes performative stability from ordinary risk minimization on a fixed distribution.

## Mechanisms

- Represent future data as a distribution that depends on the deployed model.
- Define a performatively stable point as a model that remains optimal for the distribution it induces.
- Analyze retraining as an equilibrating dynamic under explicit regularity conditions.
- Relate the framework to strategic classification, statistics, game theory, and causality.

## Evidence

- The primary paper states necessary and sufficient convergence conditions and reports bounded experiments under its formal setting.
- This repository did not reproduce the proofs, code, simulations, convergence conditions, or empirical results.
- Use the source to establish the closest formal predecessor for decision-dependent distributions, not to validate RMWS.

## Relation To The Book

`reflexive-model-world-systems` extends the ownership question from a parameter-indexed distribution to governed model lineages, eight distinct response channels, evidence ancestry, grounding reserves, institutional persistence, legitimacy, and multi-lineage interaction. Those extensions are an architectural synthesis and remain at `argument` support.

## Limits And Non-Claims

- Performative stability is not automatically beneficial, legitimate, globally stable, or safe.
- The source does not establish the completeness of the RMWS channel taxonomy.
- The source does not establish causal identification from one deployment history.
- No local support or release state changes through this citation.

## Book Chapters Supported

- `reflexive-model-world-systems`
- `governed-world-models-and-reality-grounding`
- `data-engines-continual-learning-and-unlearning`
