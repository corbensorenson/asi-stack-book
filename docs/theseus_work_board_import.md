# Theseus Work Board Import

Import ID: `theseus-work-board-import-2026-07-06`

This document records a sanitized public-safe Project Theseus work-board metadata import. It is a stale snapshot boundary for the durable work-board substrate, not a clean live Theseus replay, not a current-dashboard proof, and not a support-state promotion.

## Summary

| Field | Value |
|---|---:|
| Source status age at review | 6 days |
| Durable task rows | 130 |
| Event rows | 412 |
| Evidence rows | 133 |
| SQLite tables | 5 |
| Executor ready / active / blocked / done | 36 / 22 / 8 / 64 |
| Execution-ledger rows | 1 |
| Unattended-improvement rows | 4 |
| Feedback rows | 72 |
| Public training rows | 0 |
| External inference calls | 0 |

The imported snapshot records 130 durable task rows, 412 event rows, and 133 evidence rows while keeping raw SQLite rows and task payloads out of the public repository. It is a stale snapshot: the import explicitly blocks fresh-currentness claims.

## Validation

- Command: `python3 scripts/validate_theseus_work_board_import.py`
- Result: `experiments/theseus_work_board_import/results/2026-07-06-local.json`
- Transition: `evidence_transitions/v1_x_measured/theseus_work_board_import_no_change.json`
- Lean bridge: `lean:theseus.reference.work_board_import.metadata_boundary`
- Expected-invalid controls: 10.

| Control | Rejected |
|---|---:|
| `chapter_core_promotion.invalid.json` | true |
| `clean_live_replay_overclaim.invalid.json` | true |
| `external_inference_calls.invalid.json` | true |
| `fresh_currentness_overclaim.invalid.json` | true |
| `private_payload_copied.invalid.json` | true |
| `public_training_rows.invalid.json` | true |
| `source_hash_mismatch.invalid.json` | true |
| `sqlite_evidence_count_mismatch.invalid.json` | true |
| `task_count_mismatch.invalid.json` | true |
| `task_payloads_copied.invalid.json` | true |

## Non-Claims

- Project Theseus work-board import evidence is a metadata-only, stale-snapshot implementation-reference boundary.
- It does not copy raw reports, raw SQLite rows, task payloads, private paths, prompts, tests, solutions, score labels, candidate code, checkpoints, dogfood traces, or training rows into this public repository.
- It does not prove clean live Project Theseus replay, current dashboard state, current board state, deployed Theseus behavior, model quality, benchmark superiority, generation speed, useful-solution-per-second improvement, unattended safety, self-evolution safety, support-state movement, ASI, or any chapter core claim.
- It does not create an upward support-state transition and does not promote any chapter core claim above argument.
