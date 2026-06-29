# Project Theseus Report Import Slice

Date: 2026-06-29

This record documents the first public-safe Project Theseus report import lane
inside **The ASI Stack** repository. It imports a sanitized architecture-gate
summary as a static fixture, verifies the pinned source-artifact digest, and
checks three expected-invalid mutation controls. It does not rerun Project
Theseus from this repository.

Accepted imported report:
`theseus.architecture_gate.20260618T192303Z.public_static_import`

Tracked fixture:
`experiments/theseus_import/fixtures/valid/architecture_gate_public_report.valid.json`

Tracked result:
`experiments/theseus_import/results/2026-06-29-local.json`

Validator:

```bash
python3 scripts/validate_theseus_report.py
```

## Source Provenance

Source project: Project Theseus / SymLiquid RMI

Repository: `https://github.com/corbensorenson/symliquid-rmi`

Local checkout reviewed: `/Users/corbensorenson/Documents/Theseus-Hive`

Source commit recorded by the local checkout: `1ad88a22`

Worktree state at import review: `dirty_at_import_review`

Source artifact path:
`checkpoints/20260618T192303Z_sparkstream_smoke/artifacts/reports/architecture_gate_report.json`

Source artifact SHA-256:
`7994e2909029644d6073289d8c9c59f774473f366a1c8cbda5943326f28518b2`

The same source artifact digest was observed in the
`20260607T085402Z_sparkstream_smoke` and
`20260618T192303Z_sparkstream_smoke` checkpoint snapshots. The ASI Stack import
does not copy the raw checkpoint tree; it records the public-safe gate summary
and verifies the digest that identifies the checkpointed architecture-gate
report.

Public report fixture SHA-256:
`c33ea5d8d466e394ac556eebd623fb0eb43f601d79ea5f66021ec57762751923`

## Imported Gate Summary

The static report records a Project Theseus architecture-gate status of
`ready_for_heavy_training` with `14/14` gates passed and
`external_inference_calls` equal to `0`.

The imported gate names are:

- `rgs_complete`
- `rmi_complete`
- `ora_complete`
- `rule_router_eval_passed`
- `learned_router_head_promoted`
- `safety_ledger_passed`
- `regression_suite_present`
- `public_calibration_present`
- `residual_escrow_present`
- `bridge_benchmark_present`
- `procedural_tools_registered`
- `routing_memory_present`
- `arm_lifecycle_governed`
- `external_inference_zero`

## Negative Controls

The validator applies three expected-invalid mutation fixtures:

- `digest_mismatch.invalid.json` changes the expected source digest and must be
  rejected.
- `private_payload_copied.invalid.json` marks a private payload as copied and
  must be rejected.
- `support_promotion_overclaim.invalid.json` changes the support-state effect
  away from `no_chapter_core_claim_promotion` and must be rejected.

## Blocked Fresh Replay

The import records the failed-attempt marker
`live_theseus_rerun_blocked_dirty_checkout`. The local Project Theseus checkout
contained modified and untracked files, including private-data surfaces, so this
increment does not claim a fresh live rerun. A future stronger transition needs
a clean checkout, a public release or archived fixture, exact commands, negative
controls, and an accepted evidence-transition record.

## How This Can Be Used

This fixture can be cited as implementation-reference evidence that a Project
Theseus checkpointed report recorded a 14/14 architecture-gate pass with zero
external inference calls. It is useful context for the governed
self-improvement, readiness-gate, Project Theseus implementation-reference, and
integrated architecture chapters.

It remains a non-core import lane. No chapter core claim support state moves
above `argument`.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove deployed Theseus runtime behavior, model quality, routing
  quality, benchmark quality, safety, alignment, transfer, or ASI.
- Does not authorize heavy training inside The ASI Stack book or reproduce the
  Project Theseus training pipeline.
- Does not copy private training rows, checkpoints, dogfood traces, candidate
  payloads, prompts, or benchmark data into this public repository.
- Does not replace future clean Project Theseus replay, external review, or
  chapter-core evidence-transition review.
