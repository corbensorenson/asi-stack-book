# Source Note: Benchmarking Robustness of 3D Object Detection to Common Corruptions

| Field | Value |
|---|---|
| Source ID | `ext_3d_detection_corruptions_2023` |
| Source title | Benchmarking Robustness of 3D Object Detection to Common Corruptions |
| Ingestion date | 2026-07-19 |
| Source version / URL | Official CVPR 2023 open-access record, https://openaccess.thecvf.com/content/CVPR2023/html/Dong_Benchmarking_Robustness_of_3D_Object_Detection_to_Common_Corruptions_CVPR_2023_paper.html |
| Citation label | Dong et al. (2023), Benchmarking Robustness of 3D Object Detection to Common Corruptions |
| Published / updated | 2023-06 / not recorded |
| DOI | not recorded |
| Review state | Preliminary second-tranche audit note; the proposed chapter remains unadmitted. |
| Ingestion basis | Official CVF bibliographic record and abstract inspected. The accepted-paper body, supplement, released code, corrupted datasets, and detector evaluations were not ingested or run locally. |

## Thesis

The official abstract reports that common real-world corruptions can materially
degrade 3D object detection and introduces a controlled benchmark family for
LiDAR, camera, and fusion systems. This is a preliminary comparator for
observation trust under corruption, not evidence that any ASI Stack perception
route is robust or physically safe.

## Mechanisms

- Twenty-seven reported corruption types spanning LiDAR and camera inputs.
- Synthetic application of corruptions to KITTI, nuScenes, and Waymo data to
  form KITTI-C, nuScenes-C, and Waymo-C.
- Evaluation of 24 source-selected 3D object detectors.
- Source-reported comparisons among LiDAR-only, camera-only, and fusion routes.

## Evidence

The abstract reports that motion-level corruptions caused the largest drops in
the evaluated models, fusion models were more robust in the reported envelope,
and camera-only models were especially vulnerable to image corruptions. These
are source-reported benchmark findings. No dataset, model, corruption, metric,
or downstream driving effect has been reproduced here.

## Failure Modes

- Treating synthetic corruption coverage as exhaustive real-world coverage.
- Generalizing aggregate detector findings to every sensor, fusion topology,
  task, environment, or severity.
- Treating improved detection robustness as calibrated observation trust or
  end-to-end physical safety.
- Hiding clean-performance, modality, corruption, and severity denominators.

## Book Chapters Supported

- Proposed: `perception-sensor-fusion-and-observation-trust`
- Existing boundary owners: `governed-world-models-and-reality-grounding`,
  `security-kernel-and-digital-scifs`, and
  `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

- Use the source as a preliminary corruption-benchmark comparator only.
- Require separate modality, corruption, severity, calibration, abstention,
  task-loss, and downstream-harm denominators in any later campaign.
- Keep synthetic-to-real transfer and physical safety explicitly unresolved.

## Open Questions

- Which corruptions transfer from synthetic benchmarks to held-out field data?
- How should correlated sensor failures affect fusion confidence?
- What downstream error threshold forces abstention or active observation?
