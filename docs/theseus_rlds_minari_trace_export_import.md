# Theseus RLDS/Minari Trace Export Import

Validation command:

```bash
python3 scripts/validate_theseus_rlds_minari_trace_export_import.py
```

Result:

`experiments/theseus_rlds_minari_trace_export_import/results/2026-07-05-local.json`

Accepted bounded transition:

`evidence_transitions/v1_x_measured/theseus_rlds_minari_trace_export_import_prototype_backed.json`

## What Is Imported

This is a public-safe summary import of Project Theseus report
`reports/rlds_minari_trace_export.json` at source commit `1ad88a22`, with source
digest `989b413f887d76e29bb0b57f0656e670c2e6bb9657603aa7f5545b26f5936ccc` and
dirty-at-import-review boundary preserved. The source report records policy
`trainer_rlds_minari_trace_export_v0`, status `READY`, 1 READY export, 1
manifest, 3 declared formats, and 7 declared fields.

The imported manifest names the sanitized episode-source pointer
`reports/pressure_source_gym_pybullet_drones_seed1.json`, export id
`rlds_8e527a30014ee580`, formats `theseus_episode_jsonl`, `rlds_manifest`, and
`minari_manifest`, and fields `observation_ref`, `action`, `reward`, `done`,
`truncated`, `info`, and `seed`. It also preserves the requirements that
license metadata and replay smoke are required before downstream use.

## Evidence Boundary

The narrow support transition is for
`resource-economics.theseus_rlds_minari_trace_export_import`: the ASI Stack repo
can validate a sanitized Theseus RLDS/Minari trace-export readiness summary with
the exact source digest, expected formats, required fields, license metadata
gate, replay-smoke gate, public-safety boundary, and seven expected-invalid
controls. The claim moves only from `argument` to `prototype-backed`.

This does not prove RLDS dataset correctness, Minari dataset quality, simulator
adequacy, replay success, physical feasibility, benchmark transfer, model
quality, economic outcome, clean live Project Theseus replay, deployment
readiness, safety, alignment, transfer, ASI, or any chapter core claim.

## Public-Safety Boundary

- The raw Project Theseus report is not copied into this repository.
- Episode payloads, private traces, checkpoints, prompts, tests, solutions,
  score labels, and training rows are not copied into this repository.
- The source checkout was dirty at import review and is not described as a clean
  live replay.
- External inference calls remain `0`.

## Negative Controls

The validator rejects expected-invalid controls for source hash mismatch,
private payload copying, not-ready export status, missing license metadata,
missing replay-smoke requirement, support-promotion overclaim, and dataset-quality
overclaim.
