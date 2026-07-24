# Source Note: Adversarial Robustness of Deep Sensor Fusion Models

| Field | Value |
|---|---|
| Source ID | `ext_adversarial_sensor_fusion_2022` |
| Source title | Adversarial Robustness of Deep Sensor Fusion Models |
| Ingestion date | 2026-07-24 |
| Source version / URL | WACV 2022 open-access record, https://openaccess.thecvf.com/content/WACV2022/html/Wang_Adversarial_Robustness_of_Deep_Sensor_Fusion_Models_WACV_2022_paper.html |
| Citation label | Wang et al. (2022), Adversarial Robustness of Deep Sensor Fusion Models |
| Published / updated | 2022-01-04 / 2022-01-04 |
| DOI | not assigned in the inspected record |
| Ingestion basis | Primary CVF abstract and paper metadata inspected; no model, dataset, perturbation, training run, or evaluation reproduced. |

## Thesis

Sensor fusion can improve capability and some single-channel robustness while
also creating cross-channel externalities. A fused confidence is therefore not
an observation-trust certificate.

## Mechanisms

- Compare early and late camera-LiDAR fusion.
- Attack one or both channels under explicit threat models.
- Contrast single-channel and joint-channel adversarial training.
- Surface cases where hardening one modality harms robustness to another.

## Evidence

The authors report results for camera-LiDAR 2D object detection in their studied
architectures. The ASI Stack has not reproduced any result. The paper supports
a failure model and comparator design, not a general claim that fusion helps or
hurts.

## Failure Modes

- Correlated or jointly attacked modalities.
- Cross-channel externalities from a narrow defense.
- Clean accuracy or single-source robustness laundered into joint robustness.
- An attack model that omits physically or operationally relevant faults.

## Book Chapters Supported

- `perception-sensor-fusion-and-observation-trust`

## Claims To Add Or Update

- Fusion admission must preserve per-modality evidence and disagreement.
- A defense must be tested across joint and cross-channel conditions.
- No source result becomes local robustness evidence.

## Open Questions

- Which natural multimodal workload can exercise time sync, missingness, drift,
  spoofing, and correlated failure together?
- What independent truth source can score downstream harm without sharing the
  fused model's blind spots?
