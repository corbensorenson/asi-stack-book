# Source Note: A Mathematical Framework for Transformer Circuits

| Field | Value |
|---|---|
| Source ID | `ext_transformer_circuits_2021` |
| Source title | A Mathematical Framework for Transformer Circuits |
| Ingestion date | 2026-07-03 |
| Source version / URL | Transformer Circuits article, https://transformer-circuits.pub/2021/framework/index.html |
| Citation label | Elhage et al. (2021), Transformer Circuits |
| Published / updated | 2021-12-22 / 2021-12-22 |
| DOI | not recorded |
| Ingestion basis | Public Transformer Circuits and Anthropic research pages inspected for source metadata and high-level claim boundary; article not vendored into this repository and no circuit analysis reproduced. |

## Thesis

Transformer Circuits is an external mechanistic-interpretability comparator for treating internal model analysis as a possible evidence class. It helps the Evidence States chapter distinguish behavioral evidence from white-box evidence: a circuit analysis can support a scoped claim about a particular model, layer, behavior, or mechanism only when the inspected artifact and analysis boundary are explicit.

## Mechanisms

- Reverse-engineer model internals rather than only measuring input/output behavior.
- Work on deliberately scoped transformer settings before extrapolating to larger systems.
- Use mathematical and mechanistic descriptions to make internal computation inspectable.
- Keep the model family, scale, component, behavior, and analysis method visible.

## Evidence

- The source contributes mechanistic-interpretability vocabulary for white-box evidence and circuit-level claims.
- This repository has not reproduced a Transformer Circuits analysis, run causal interventions, inspected ASI Stack model internals, or validated any deployed model mechanism.
- Use this source to position interpretability as a possible evidence role, not as support that the ASI Stack is interpretable or safe.

## Failure Modes

- A narrow circuit analysis can be over-read as a whole-model guarantee.
- A description of a mechanism can be mistaken for evidence that the mechanism governs deployed behavior.
- A result from a small or simplified model can be laundered into claims about larger or different systems.
- White-box evidence can crowd out negative behavioral results if the evidence ledger does not keep roles separate.

## Book Chapters Supported

- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `white-box-evidence-interpretability-and-activation-governance`

## Claims To Add Or Update

- Add interpretability as a possible evidence role only when the artifact, model/layer/behavior scope, method, intervention or analysis boundary, and limitations are recorded.
- Keep interpretability evidence separate from source-derived, proof-backed, synthetic-test-backed, and empirical behavioral evidence.
- Do not treat a cited interpretability paper as evidence that this stack has white-box transparency.

## Open Questions

- What record fields should a future interpretability evidence packet require before it can move a claim?
- Which ASI Stack claims would actually benefit from mechanistic evidence rather than behavioral, proof, or replay evidence?
- What negative controls should reject overbroad interpretability claims?
