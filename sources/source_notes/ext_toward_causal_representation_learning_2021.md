# Source Note: Toward Causal Representation Learning

| Field | Value |
|---|---|
| Source ID | `ext_toward_causal_representation_learning_2021` |
| Source title | Toward Causal Representation Learning |
| Ingestion date | 2026-07-24 |
| Source version / URL | Proceedings of the IEEE 109(5), https://arxiv.org/abs/2102.11107 |
| Citation label | Schölkopf et al. (2021), Toward Causal Representation Learning |
| Published / updated | 2021-02-26 / 2021-05-01 |
| DOI | 10.1109/JPROC.2021.3058954 |
| Ingestion basis | Primary abstract, article metadata, and research agenda inspected; no representation, intervention, or transfer result reproduced. |

## Thesis

Machine learning usually assumes observed variables, while causal inference
usually assumes causal variables are already given. Discovering high-level
causal variables from low-level observations is therefore a central unresolved
bridge between representation learning and causal reasoning.

## Mechanisms

- Relate causal structure to transfer and generalization.
- Seek modular, sparse, autonomous mechanisms.
- Learn intervention-relevant variables from lower-level observations.

## Evidence

The article is a review and research agenda. It does not provide a general
solution to causal representation learning and supplies no local evidence.

## Failure Modes

- Predictive features mislabeled causal.
- Latent variables uninterpretable under intervention.
- Identifiability assumptions hidden.
- Correlation-based transfer mistaken for mechanism stability.

## Book Chapters Supported

- `governed-world-models-and-reality-grounding`

## Claims To Add Or Update

- World-model records should distinguish association, intervention, and
  counterfactual scope.
- A causal representation must state its identifiability and observation
  assumptions.

## Open Questions

- Which intervention-rich task can test causal variables against strong
  predictive representations?
- How should ontology change invalidate earlier causal claims?
