# Theseus Book Crosswalk Import

Import ID: `theseus-book-crosswalk-import-2026-07-05`

This document records a sanitized public-safe Project Theseus book-to-Theseus crosswalk import. It is a pointer-only implementation-reference evidence slice, not a clean live Theseus replay and not a chapter-core support-state promotion.

## Summary

| Field | Value |
|---|---:|
| Trigger state | `GREEN` |
| AI-book source files in source manifest | 1,474 |
| Public-safe pointer rows | 53 |
| Book-to-Theseus backlog cards | 20 |
| Source-sync review decisions | 134 |
| Changed AI-book source files | 9 |
| Removed AI-book source files | 0 |
| Stale phases | 0 |
| Missing source-basis rows | 0 |
| Done phases missing evidence | 0 |

The import preserves 53 public-safe pointer rows and 20 backlog cards while keeping every imported support row at pointer-only support.

## Validation

- Command: `python3 scripts/validate_theseus_book_crosswalk_import.py`
- Result: `experiments/theseus_book_crosswalk_import/results/2026-07-05-local.json`
- Decision: `evidence_transitions/v1_x_measured/theseus_book_crosswalk_import_no_change.json`
- Lean bridge: `lean:theseus.reference.book_crosswalk.pointer_boundary`
- Expected-invalid controls: 10.

| Control | Rejected |
|---|---:|
| `chapter_core_promotion.invalid.json` | true |
| `clean_live_replay_overclaim.invalid.json` | true |
| `missing_source_basis.invalid.json` | true |
| `private_payload_copied.invalid.json` | true |
| `public_safe_evidence_smoke_failure.invalid.json` | true |
| `public_training_rows.invalid.json` | true |
| `raw_report_copied.invalid.json` | true |
| `source_hash_mismatch.invalid.json` | true |
| `source_sync_smoke_failure.invalid.json` | true |
| `support_promotion_overclaim.invalid.json` | true |

## Non-Claims

- Project Theseus book-to-book crosswalk import is pointer-only implementation-reference evidence.
- This import does not copy the raw Project Theseus crosswalk report, private paths, private payloads, prompts, tests, solutions, candidate code, traces, checkpoints, dogfood records, or training rows into this public repository.
- This import does not prove clean live Project Theseus replay, model quality, deployed Theseus behavior, benchmark performance, generation speed, safety, alignment, transfer, deployment readiness, self-evolution safety, or ASI.
- This import does not create an upward support-state transition.
- This import does not promote any chapter core claim above argument.
