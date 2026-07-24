# Source Note: ImageBind

| Field | Value |
|---|---|
| Source ID | `ext_imagebind_2023` |
| Source title | ImageBind: One Embedding Space To Bind Them All |
| Ingestion date | 2026-07-24 |
| Source version / URL | CVPR 2023 open-access record, https://openaccess.thecvf.com/content/CVPR2023/html/Girdhar_ImageBind_One_Embedding_Space_To_Bind_Them_All_CVPR_2023_paper |
| Citation label | Girdhar et al. (2023), ImageBind |
| Published / updated | 2023-06-18 / 2023-06-18 |
| DOI | not assigned in the inspected record |
| Ingestion basis | Primary CVF abstract, metadata, and paper excerpt inspected; no weights, dataset, embedding, retrieval, or recognition result reproduced. |

## Thesis

A shared representation can connect image, text, audio, depth, thermal, and IMU
modalities without observing every modality pair. That is a useful substrate
comparator, not proof that the shared space is calibrated to the world.

## Mechanisms

- Use image-paired data as a hub for six modalities.
- Align modality encoders into a shared embedding space.
- Evaluate cross-modal retrieval, recognition, composition, and transfer.

## Evidence

The reported zero- and few-shot results are source evidence within ImageBind's
models, data, tasks, and metrics. They do not establish sensor identity,
calibration, synchronization, causal grounding, uncertainty, or safety.

## Failure Modes

- Hub-modality bias and inherited image-model errors.
- Semantically close embeddings mistaken for physical equivalence.
- Missing, stale, or desynchronized sensor channels hidden by a plausible
  shared representation.
- Capability metrics substituted for observation reliability.

## Book Chapters Supported

- `perception-sensor-fusion-and-observation-trust`
- `replaceable-cognitive-substrates-beyond-transformer-monoculture`

## Claims To Add Or Update

- Shared embeddings are candidate representations behind the observation
  contract, never the authority boundary itself.
- Cross-modal agreement must not suppress provenance, timing, or disagreement.

## Open Questions

- Which representation tests distinguish semantic alignment from task-relevant
  physical state?
- How should an observation receipt expose a hub modality's correlated error?
