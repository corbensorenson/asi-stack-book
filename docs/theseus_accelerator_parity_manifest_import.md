# Theseus Accelerator Parity Manifest Import

Import ID: `theseus-accelerator-parity-manifest-import-2026-07-06`

This document records a sanitized public-safe Project Theseus accelerator parity manifest import. It is a bounded implementation-reference evidence slice, not full CUDA/MLX/Metal parity, not production scheduler routing, not model promotion, and not a chapter-core support-state promotion.

## Summary

| Field | Value |
|---|---:|
| Trigger state | `GREEN` |
| Surfaces OK | 7 / 7 |
| MLX report summaries | 7 / 7 |
| Metal report summaries | 4 / 4 |
| Artifact manifests | 4 |
| Scheduler canary surfaces | 4 |
| Hard failures | 0 |
| Explicit guardrail gaps | 0 |
| Public training rows | 0 |
| External inference calls | 0 |
| Teacher-use count | 0 |
| Model-promotion allowed count | 0 |
| Production-routing enabled count | 0 |

The import records 7 of 7 surfaces, 4 Metal report summaries, 4 scheduler-canary surfaces, and nine expected-invalid controls.

## Guardrails

| Guardrail | Value |
|---|---:|
| `public_calibration_run` | `False` |
| `public_training_rows` | `0` |
| `external_inference_calls` | `0` |
| `teacher_used` | `False` |
| `model_promotion_allowed` | `False` |
| `production_scheduler_routing_enabled` | `False` |
| `full_parity_claim_allowed` | `False` |

## Surface Rows

| Surface | Class | CUDA-equivalent command | MLX | Metal | Artifact manifest |
|---|---|---|---:|---:|---:|
| `eval_chunk` | `hive_worker_chunk` | `` | true | false | false |
| `training_chunk` | `hive_worker_chunk` | `` | true | false | false |
| `rollout_chunk` | `hive_worker_chunk` | `` | true | false | false |
| `standalone_readout_cli` | `rust_cli_bridge_plus_native_metal` | `train-standalone-cuda` | true | true | true |
| `rollout_cli` | `rust_cli_bridge_plus_native_metal` | `train-rollout-cuda` | true | true | true |
| `rollout_sweep_cli` | `rust_cli_bridge_plus_native_metal` | `train-rollout-cuda-sweep` | true | true | true |
| `token_superposition_cli` | `rust_cli_bridge_plus_native_metal` | `train-token-superposition-cuda` | true | true | true |

## Validation

- Command: `python3 scripts/validate_theseus_accelerator_parity_manifest_import.py`
- Result: `experiments/theseus_accelerator_parity_manifest_import/results/2026-07-06-local.json`
- Transition: `evidence_transitions/v1_x_measured/theseus_accelerator_parity_manifest_import_prototype_backed.json`
- Lean bridge: `lean:theseus.reference.accelerator_parity_manifest_import.fixture_bridge`
- Expected-invalid controls: 9.

| Control | Rejected |
|---|---:|
| `chapter_core_promotion.invalid.json` | true |
| `full_parity_overclaim.invalid.json` | true |
| `hard_failure_hidden.invalid.json` | true |
| `model_promotion_overclaim.invalid.json` | true |
| `production_routing_overclaim.invalid.json` | true |
| `raw_report_copied.invalid.json` | true |
| `source_hash_mismatch.invalid.json` | true |
| `source_trigger_not_green.invalid.json` | true |
| `surface_count_mismatch.invalid.json` | true |

## Non-Claims

- does not copy the raw Project Theseus accelerator parity report, private paths, private payloads, checkpoints, prompts, tests, solutions, score labels, candidate code, metrics payloads, or training rows into this public repository
- does not prove full CUDA, MLX, or Metal parity; production scheduler routing; model promotion; benchmark performance; model quality; deployment readiness; safety; alignment; transfer; clean live Project Theseus replay; or ASI
- does not promote any chapter core claim above argument
