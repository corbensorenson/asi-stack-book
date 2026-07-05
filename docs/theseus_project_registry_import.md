# Theseus Project Registry Import

Import ID: `theseus-project-registry-import-2026-07-05`

This document records a sanitized public-safe Project Theseus project-registry import. It is a bounded implementation-reference evidence slice, not a clean live Theseus replay and not a chapter-core support-state promotion.

## Summary

| Field | Value |
|---|---:|
| Trigger state | `GREEN` |
| Registered paths | 5,662 / 5,662 |
| Owned lifecycle surfaces | 24 surfaces |
| Coverage ratio | 1.0 |
| Unregistered active sources | 0 |
| Unclassified duplicate families | 0 |
| Stale report outputs | 0 |
| Missing report outputs | 0 |
| Generated source artifacts | 0 |
| Registry-governance violations | 0 |
| Hard governance violations | 0 |
| External inference calls | 0 |

The import records 5,662 registered paths across 24 surfaces and nine expected-invalid controls.

## Validation

- Command: `python3 scripts/validate_theseus_project_registry_import.py`
- Result: `experiments/theseus_project_registry_import/results/2026-07-05-local.json`
- Transition: `evidence_transitions/v1_x_measured/theseus_project_registry_import_prototype_backed.json`
- Lean bridge: `lean:theseus.reference.project_registry_import.fixture_bridge`
- Expected-invalid controls: 9.

| Control | Rejected |
|---|---:|
| `chapter_core_promotion.invalid.json` | true |
| `clean_live_replay_overclaim.invalid.json` | true |
| `coverage_gap.invalid.json` | true |
| `generated_source_artifact.invalid.json` | true |
| `governance_violation.invalid.json` | true |
| `private_payload_copied.invalid.json` | true |
| `source_hash_mismatch.invalid.json` | true |
| `unclassified_duplicates.invalid.json` | true |
| `unregistered_active_sources.invalid.json` | true |

## Non-Claims

- Project Theseus project-registry health is repository-organization evidence only.
- This import does not copy the raw Project Theseus registry report, private paths, private payloads, prompts, tests, solutions, candidate code, traces, checkpoints, or training rows into this public repository.
- This import does not prove clean live Project Theseus replay, model quality, deployed Theseus behavior, benchmark performance, generation speed, safety, alignment, transfer, deployment readiness, self-evolution safety, or ASI.
- This import does not promote any chapter core claim above argument.
