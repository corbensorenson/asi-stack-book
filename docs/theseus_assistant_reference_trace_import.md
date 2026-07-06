# Theseus Assistant Reference-Trace Import

Import ID: `theseus-assistant-reference-trace-import-2026-07-06`

Claim ID: `project-theseus-as-report-first-implementation-reference.assistant_reference_trace_import`

This document records a sanitized public-safe Project Theseus assistant runtime reference-trace import. It packages the existing Theseus assistant runtime report as a bounded implementation-reference trace object: intent, command contract, context, planning, runtime adapter, procedural route, authority, resource, generation, failure, artifact, claim, evidence, residual, and policy-optimization records are all present as record-type metadata. It is not a clean live Theseus replay, not current runtime state, not model-quality evidence, and not a chapter-core promotion.

## Summary

| Field | Value |
|---|---:|
| Source commit | `1ad88a22` |
| Source checkout boundary | `dirty_at_import_review` |
| Source report created | `2026-06-29T23:55:08.805277+00:00` |
| Runtime trigger state | `GREEN` |
| Required reference-trace record types | 19 |
| Gates passed / total | 27 / 27 |
| Hard / warning gates | 23 / 4 |
| VIEA view records | 2,203 |
| Route required groups | 4 |
| VCM selected pages | 12 |
| Latest public diagnostic score | 45 / 64 |
| Public training rows | 0 |
| External inference calls | 0 |
| Expected-invalid controls | 11 |

The imported trace records 19 required reference-trace record types without copying the raw Project Theseus report, raw VIEA trace, raw assistant text, raw prompts, private paths, checkpoints, candidate code, score labels, or training rows into this repository.

The validation summary is intentionally compact: 27 / 27 gates pass, and the import carries 11 expected-invalid controls.

## Trace Records

| Record family | Imported boundary |
|---|---|
| Intent and command | `intent_contract`, `command_contract` |
| Context and adequacy | `context_abi_record`, `context_transaction`, `context_adequacy` |
| Planning and work | `typed_job`, `planforge_dag`, `runtime_adapter_invocation`, `procedural_tool_record` |
| Authority and resources | `authority_transition`, `authority_use_receipt`, `resource_budget` |
| Generation and failure | `generation_mode`, `failure_boundary` |
| Evidence and residuals | `artifact_graph_record`, `claim_record`, `evidence_transition_record`, `residual_record` |
| Improvement policy | `policy_optimization_record` |

The route validator receipt records 2,203 VIEA view records, 117 governance records, 196 authority records, 161 resource-route records, 140 failure-boundary records, 158 evidence-transition records, 180 artifact records, 185 claim-ledger entries, 227 context records, 92 runtime-adapter records, 139 semantic-IR records, and 49 simulation-fidelity records. These counts show a report-shaped runtime trace boundary; they do not prove quality of the underlying route, verifier, model, benchmark, or runtime.

## Validation

- Command: `python3 scripts/validate_theseus_assistant_reference_trace_import.py`
- Result: `experiments/theseus_assistant_reference_trace_import/results/2026-07-06-local.json`
- Transition: `evidence_transitions/v1_x_measured/theseus_assistant_reference_trace_import_prototype_backed.json`
- Lean bridge: `lean:theseus.reference.assistant_reference_trace_import.fixture_bridge`
- Expected-invalid controls: 11.

| Control | Rejected |
|---|---:|
| `benchmark_headline_overclaim.invalid.json` | true |
| `chapter_core_promotion.invalid.json` | true |
| `clean_live_replay_overclaim.invalid.json` | true |
| `external_inference_calls.invalid.json` | true |
| `gate_failure_hidden.invalid.json` | true |
| `missing_required_trace_record.invalid.json` | true |
| `model_quality_overclaim.invalid.json` | true |
| `private_payload_copied.invalid.json` | true |
| `public_training_rows.invalid.json` | true |
| `raw_assistant_text_copied.invalid.json` | true |
| `source_hash_mismatch.invalid.json` | true |

## Non-Claims

- Project Theseus assistant reference-trace import evidence is a sanitized digest-and-count implementation-reference boundary.
- It does not copy the raw Project Theseus report, raw VIEA trace, raw assistant text, raw prompts, private payloads, private paths, checkpoints, tests, solutions, score labels, candidate code, or training rows into this public repository.
- It does not prove clean live Project Theseus replay, current runtime state, deployed Theseus behavior, route quality, private verifier quality, model quality, benchmark superiority, useful-solution-per-second improvement, learned generation, safety, alignment, transfer, or ASI.
- It does not promote any chapter core claim above `argument`.
