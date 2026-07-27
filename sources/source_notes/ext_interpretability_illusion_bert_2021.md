# Source Note: An Interpretability Illusion for BERT

| Field | Value |
|---|---|
| Source ID | `ext_interpretability_illusion_bert_2021` |
| Source title | An Interpretability Illusion for BERT |
| Ingestion date | 2026-07-26 |
| Source version / URL | arXiv:2104.07143v1, https://arxiv.org/abs/2104.07143 |
| Citation label | Bolukbasi et al. (2021), An Interpretability Illusion for BERT |
| Published / updated | 2021-04-14 / 2021-04-14 |
| DOI | 10.48550/arXiv.2104.07143 |
| Ingestion basis | Primary paper inspected at Sections 1, 3–5, the dataset and annotation methods, results tables, concept-direction taxonomy, and methodological conclusion. No experiment was reproduced locally. |

## Thesis

Coherent top-activating examples from one corpus can create a simple semantic
story for a neuron or direction that changes when the same model and direction
are inspected on another corpus. Dataset geometry and local semantic coherence
can therefore create an **interpretability illusion**. A credible construct
claim needs cross-dataset challenge and must distinguish global, dataset-level,
and local structure.

## Mechanisms

- Hold the BERT model and activation direction fixed while changing among four
  corpora.
- Compare top-activating sentences with random directions and random sentence
  groups under annotation.
- Test whether the datasets occupy separable regions of embedding space.
- Distinguish global concept directions from directions meaningful only in one
  dataset region and from locally coherent clusters with no global direction.

## Evidence

Sections 3–5 report that many neurons and random directions produced
apparently meaningful top-activating examples within a dataset, but those
patterns often differed across QQP, QNLI, Wikipedia, and BookCorpus. The paper
attributes the effect to dataset idiosyncrasy, representation geometry, and
annotation error. This is a BERT sentence-embedding case, not a universal
finding about every representation or method.

## Failure Modes

- Selected exemplars can make a local or dataset-level pattern look global.
- Annotators can impose a simple concept on heterogeneous examples.
- A held-out split from the same corpus may preserve the same geometric
  shortcut.
- Cross-dataset instability does not by itself distinguish feature failure,
  construct misspecification, or a legitimately context-dependent mechanism.

## Book Chapters Supported

- Primary: `white-box-evidence-interpretability-and-activation-governance`
- Handoff: `governed-world-models-and-reality-grounding`

## Claims To Add Or Update

- Test a semantic interpretation on materially different corpora and relevant
  deployment shifts, not only a random same-corpus split.
- Preserve global, dataset-level, and local interpretations as competing
  hypotheses until the evidence distinguishes them.
- Treat stable-looking exemplars as hypothesis generation rather than semantic
  construct validation.

## Open Questions

- Which distribution shifts are sufficient to challenge a construct without
  changing the construct itself?
- How should cross-dataset instability interact with causal interventions?
- Can automated explanation systems detect their own dataset-conditioned
  stories without an independently designed challenge set?
