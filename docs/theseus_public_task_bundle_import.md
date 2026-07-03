# Project Theseus Public Task-Bundle Import

Import id: `theseus_public_task_bundle_import_2026_07_03_local`

Validator: `python3 scripts/validate_theseus_public_task_bundle_import.py`

Result: `experiments/theseus_public_task_bundle_import/results/2026-07-03-local.json`

## What It Imports

This is a public-safe summary import from pinned Project Theseus reports at
commit `1ad88a22b28e9228a67a4779176aeef5c41d2544`. The local Theseus checkout
was dirty at import time, so clean live Theseus replay remains unclaimed. The
fixture imports report hashes, counts, gate outcomes, residual counts, public
boundary flags, and artifact gaps only.

The import does not prove model quality, benchmark superiority, generation
speed, useful-solution-per-second improvement, or clean live Theseus replay.

Accepted no-promotion decision:
`evidence_transitions/v1_x_measured/theseus_public_task_bundle_import_no_change.json`.
The decision keeps the import at `argument` support and blocks clean-live-replay,
model-quality, benchmark-superiority, generation-speed,
useful-solution-per-second, support-state, deployment, self-evolution, and
chapter-core promotion claims until a clean public-safe replay or archived
public fixture, environment notes, missing-artifact and publication-permission
closure, verifier-quality review, and independent review exist.

The imported source surface records 64 public BigCodeBench metadata-only tasks,
0 public training rows, 0 external inference calls, 12 of 12 operator gates
passed, 18 of 18 benchmark gates passed, 19 residuals exported, 512 student
candidates recorded in the summary, 45 quality-passing candidates under the
source quality gate, 0 task-level regressions, and a reported public
calibration pass rate of 0.703125 for the imported result.

## Public Boundary

The task manifest is treated as metadata-only. The fixture records that prompts,
tests, solutions, traces, score labels, and candidate code are not copied into
this repository. The result is an implementation-reference import and
calibration-boundary record, not a public benchmark claim.

## Visible Gaps

- The source checkout was dirty at import time.
- Clean live Theseus replay remains unclaimed.
- A transfer artifact path reported by the source result was not present in the
  local checkout.
- A student candidate manifest path reported by the operator summary was not
  present in the local checkout.
- No archived public Theseus release fixture is bundled in this repository.

## Negative Controls

The validator rejects seven expected-invalid mutations: clean-live-replay
overclaim, public training rows, public prompt export, support-state promotion,
hidden task regression, hidden artifact gap, and benchmark gate failure.

## Non-Claims

- Does not prove clean live Project Theseus replay.
- Does not prove model quality, benchmark superiority, generation speed, or
  useful-solution-per-second improvement.
- Does not copy public prompts, tests, solutions, traces, scores, or candidate
  code into this repository.
- Does not promote any chapter core claim above `argument`.
- The import result itself records support-state effect `none`; the separate
  accepted no-promotion decision blocks broader promotion and does not create
  an upward support-state transition.
