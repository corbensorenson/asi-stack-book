# Project Theseus Generation Mode Import Slice

Date: 2026-07-01

This record documents the second public-safe Project Theseus report import lane
inside **The ASI Stack** repository. It imports a sanitized generation-mode gate
summary as a static fixture, verifies pinned source-artifact digests, and checks
four expected-invalid mutation controls. It does not rerun Project Theseus from
this repository.

Accepted imported report:
`theseus.generation_mode_gate.20260701.public_static_import`

Tracked fixture:
`experiments/theseus_generation_mode_import/fixtures/valid/generation_mode_gate_public_summary.valid.json`

Tracked result:
`experiments/theseus_generation_mode_import/results/2026-07-01-local.json`

Validator:

```bash
python3 scripts/validate_theseus_generation_mode_import.py
```

## Source Provenance

Source project: Project Theseus / SymLiquid RMI

Repository: `https://github.com/corbensorenson/symliquid-rmi`

Local checkout reviewed: `/Users/corbensorenson/Documents/Theseus-Hive`

Source commit recorded by the local checkout: `1ad88a22`

Worktree state at import review: `dirty_at_import_review`

Source report path:
`reports/generation_mode_registry.json`

Source report SHA-256:
`a711d0dbca9779f26d4b0a63db18ce1fc574ade47a262f5140a9a7b6d325e90b`

Source config SHA-256:
`eebf96a7cf0a6c30c9203d2f11377c953973694a34dec8f095c8b76e378114c7`

Source tool SHA-256:
`e99477a1b9546c14c60dc8e2b442f1437274d7ba367e717c23b608fb41fd290b`

Public report fixture SHA-256:
`0a101d427d51029ba7a0aaaaf4329cb47e96400cd21fc284123e366fb309d709`

## Imported Gate Summary

The static report records a Project Theseus generation-mode gate status of
`YELLOW` with `18 modes`, `13 comparisons`, zero hard gaps, five hard boundary
gates passing, and zero promotable comparisons. Five comparison warnings record
accepted-span speed lift, but every candidate task-pass count remains zero and
mean useful solution per second remains zero.

The imported hard boundary gates are:

- `public_benchmark_training_forbidden`
- `runtime_external_inference_forbidden`
- `fallback_template_router_tool_credit_forbidden`
- `raw_throughput_only_promotion_forbidden`
- `mixed_metric_overclaim_forbidden`

This is negative evidence against raw-throughput promotion. It shows the report
discipline detecting that faster accepted-span accounting is insufficient when
verified task success stays at zero.

## Negative Controls

The validator applies four expected-invalid mutation fixtures:

- `private_payload_copied.invalid.json` marks a private payload as copied and
  must be rejected.
- `support_promotion_overclaim.invalid.json` changes the support-state effect
  away from `no_chapter_core_claim_promotion` and must be rejected.
- `raw_speed_promotion.invalid.json` marks a raw-speed comparison promotable and
  must be rejected.
- `useful_speed_overclaim.invalid.json` invents nonzero useful solution per
  second and must be rejected.

## Blocked Fresh Replay

The import records the failed-attempt marker
`live_theseus_generation_mode_rerun_blocked_dirty_checkout`. The local Project
Theseus checkout contained modified and untracked files, including private-data
surfaces, so this increment does not claim a fresh live rerun. A future stronger
transition needs a clean checkout, a public task bundle or archived fixture,
exact commands, negative controls, quality/residual review, and an accepted
evidence-transition record.

## How This Can Be Used

This fixture can be cited as implementation-reference evidence that a Project
Theseus checkpointed generation-mode gate enforced accepted-output and
useful-solution accounting, rejected raw-throughput-only promotion, and recorded
zero promotable comparisons. It is useful context for the Fast Generation,
Resource Economics, Benchmark Ratchets, and Project Theseus
implementation-reference chapters.

It remains a non-core import lane. No chapter core claim support state moves
above `argument`.

## Non-Claims

- Does not promote any chapter core claim above `argument`.
- Does not prove generation speed, useful-solution-per-second improvement, model
  quality, routing quality, benchmark quality, safety, alignment, transfer, or
  ASI.
- Does not authorize heavy training inside The ASI Stack book or reproduce the
  Project Theseus generation-mode pipeline.
- Does not copy private task rows, prompts, candidate outputs, training rows,
  checkpoints, traces, or benchmark payloads into this public repository.
- Does not replace future clean Project Theseus replay, public task bundle,
  external review, or chapter-core evidence-transition review.
