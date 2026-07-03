# Source Note: Towards Monosemanticity: Decomposing Language Models With Dictionary Learning

| Field | Value |
|---|---|
| Source ID | `ext_monosemanticity_2023` |
| Source title | Towards Monosemanticity: Decomposing Language Models With Dictionary Learning |
| Ingestion date | 2026-07-03 |
| Source version / URL | Transformer Circuits article, https://transformer-circuits.pub/2023/monosemantic-features |
| Citation label | Bricken et al. (2023), Towards Monosemanticity |
| Published / updated | 2023-10-05 / 2023-10-05 |
| DOI | not recorded |
| Ingestion basis | Public Transformer Circuits and Anthropic research pages inspected for source metadata and high-level claim boundary; article not vendored into this repository and no sparse-autoencoder run reproduced. |

## Thesis

Towards Monosemanticity is an external mechanistic-interpretability comparator for feature-level evidence. It helps the Evidence States chapter state that a discovered feature can be useful evidence only within a declared model, layer, decomposition method, feature-selection procedure, and behavioral scope.

## Mechanisms

- Use dictionary learning / sparse autoencoder methods to decompose activations into learned features.
- Treat features as candidate units of analysis that can be more informative than individual neurons in some settings.
- Connect feature discovery to examples and activation patterns rather than treating feature names as self-validating.
- Preserve the distinction between a feature-level artifact and a whole-system safety or capability claim.

## Evidence

- The source contributes a concrete family of mechanistic-interpretability artifacts: learned features from model activations.
- This repository has not trained sparse autoencoders, decomposed activations, evaluated feature monosemanticity, reproduced the paper's examples, or connected feature evidence to any ASI Stack model.
- Use this source to position feature-level interpretability as an evidence role with scope and limitations, not as a support-state promotion.

## Failure Modes

- Feature labels can become folk explanations if examples, activation contexts, and negative cases are not preserved.
- A feature decomposition can be treated as a general model explanation even when it covers one model/layer/run.
- A sparse-autoencoder artifact can be mistaken for behavioral validation.
- Feature evidence can be over-counted if the evidence ledger does not require artifact refs, analysis scope, and non-claims.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)

## Claims To Add Or Update

- Add feature-level interpretability as a possible evidence role only with artifact refs, model/layer scope, method limits, examples or interventions, negative cases, and explicit non-claims.
- Keep feature evidence from automatically becoming safety, deployment-readiness, or model-quality evidence.
- Route any future ASI Stack interpretability result through an evidence transition before moving support state.

## Open Questions

- What minimum negative controls should a feature-level evidence packet include?
- Should interpretability evidence have its own support state or stay an evidence role inside existing support states?
- How should feature-level evidence interact with proof-carrying claims and benchmark ratchets?
