# Source Note: Multimodal Machine Learning

| Field | Value |
|---|---|
| Source ID | `ext_multimodal_machine_learning_taxonomy_2019` |
| Source title | Multimodal Machine Learning: A Survey and Taxonomy |
| Ingestion date | 2026-07-24 |
| Source version / URL | IEEE TPAMI 41(2), https://arxiv.org/abs/1705.09406 |
| Citation label | Baltrušaitis, Ahuja, and Morency (2019), Multimodal Machine Learning |
| Published / updated | 2019-02-01 / 2019-02-01 |
| DOI | 10.1109/TPAMI.2018.2798607 |
| Ingestion basis | Primary abstract, journal metadata, and taxonomy inspected; no surveyed result reproduced. |

## Thesis

Multimodal learning is not one fusion operation. Representation, translation,
alignment, fusion, and co-learning create different interfaces and failure
surfaces.

## Mechanisms

- Organize multimodal systems by representation, translation, alignment,
  fusion, and co-learning.
- Compare early/late and model-level integration within a broader taxonomy.
- Surface missing-pair, alignment, and cross-modal transfer questions.

## Evidence

This is a peer-reviewed survey and taxonomy. It is strong field orientation but
does not validate a particular architecture or the ASI Stack observation
contract.

## Failure Modes

- Treating multimodality as concatenation.
- Losing temporal or semantic alignment.
- Inferring redundancy from correlated but non-independent modalities.
- Co-learning transferring error or bias from a resource-rich modality.

## Book Chapters Supported

- `perception-sensor-fusion-and-observation-trust`

## Claims To Add Or Update

- Perception records should identify which multimodal operation occurred.
- Alignment and fusion adequacy require distinct tests.

## Open Questions

- Which taxonomy fields must be mandatory in the minimal observation contract?
- How should missing modalities and translation uncertainty propagate to
  planning?
