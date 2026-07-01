# Theseus Support Replay Probe

Date: 2026-07-01

This record documents a local replay probe for the two selected Project
Theseus support lanes in the v1.x active evidence cycle. It runs the two
public-safe Project Theseus validators, records command exit codes, elapsed
milliseconds, output digests, and tracked artifact hashes, then checks that the
result remains a replay artifact rather than a claim promotion.

This is not a clean live Theseus replay, public task-bundle run, current
dashboard record, production workload trace, model-quality measurement,
generation-speed result, useful-solution-per-second result, deployment
readiness result, safety result, alignment result, external review, or ASI
evidence. It is a reproducibility and accounting increment over the static
public-safe imports already recorded in the repository.

## Command

```bash
python3 scripts/run_theseus_support_replay_probe.py --write-result
python3 scripts/validate_theseus_support_replay_probe.py
```

The first command writes the local replay result record. The second command
replays the same validator set, checks command-output digests, verifies tracked
artifact hashes, and enforces the non-claim boundary.

## Result Record

Result record:
`experiments/theseus_support_replay_probe/results/2026-07-01-local.json`

| Field | Value |
|---|---|
| Probe ID | `theseus-support-replay-probe-2026-07-01-local` |
| Replay commands | 2 |
| Tracked artifacts | 10 |
| Support-state effect | `none` |
| Chapter-core support effect | `none` |
| Evidence transition created | `false` |

## Replay Surface

The probe runs and records these local commands:

| Command | Evidence surface |
|---|---|
| `python3 scripts/validate_theseus_report.py` | Public-safe static Project Theseus architecture-gate import. |
| `python3 scripts/validate_theseus_generation_mode_import.py` | Public-safe static Project Theseus generation-mode import plus Fast Generation Lean bridge. |

## Boundary

The probe proves only that the current repository can replay the named public-
safe static import validators and that the tracked Theseus support artifacts
match the recorded hashes at the time of validation. It does not replace the
larger blockers for this lane: clean live Theseus replay, archived public
release fixture, public task bundle, quality/residual review, exact execution
commands, external review, or an accepted support-state transition.

## Non-Claims

- This Theseus support replay probe does not promote any chapter core claim
  above `argument`.
- This Theseus support replay probe does not create a support-state transition.
- This Theseus support replay probe does not rerun Project Theseus, prove
  deployed Theseus runtime behavior, prove generation speed, prove
  useful-solution-per-second improvement, prove model quality, prove routing
  quality, prove benchmark quality, prove safety, prove alignment, prove
  transfer, or prove ASI.
- This Theseus support replay probe records repository command execution over
  public-safe static imports only; it is not a clean live Theseus replay,
  public task-bundle run, production dashboard record, or external review.
