# Theseus/Fast Support Lane Run

This record documents the selected v1.x support-lane aggregate for Project
Theseus and Fast Generation. It composes existing public-safe evidence surfaces
instead of creating a new support-state transition.

Command:

```bash
python3 scripts/run_theseus_fast_support_lane.py --write-result
```

Tracked result:

`experiments/theseus_fast_support_lane/results/2026-07-03-local.json`

Validation command:

```bash
python3 scripts/validate_theseus_fast_support_lane.py
```

Lane id: `theseus-fast-support-lane-2026-07-03-local`

## Scope

- Selected support lanes: `project-theseus-as-report-first-implementation-reference`; `fast-generation-architectures`
- Support-state effect: `none`
- Chapter-core support effect: `none`
- Evidence transition created by this run: `false`
- Command replays: 4
- Tracked artifact digests: 16
- Public task records carried by the aggregate: 68 public task records
- Expected-invalid or rejected controls: 14 expected-invalid or rejected controls
- Accepted no-promotion decisions carried: 2

## Aggregate Lean Alignment

The result carries an aggregate Python/Lean support-lane invariant. The Python
validator recomputes the aggregate from the current Theseus generation-mode
import, Theseus support replay probe, Theseus public task-bundle import, Fast
Generation task bundle, tracked artifacts, and accepted no-promotion decisions.
The Lean fixture `theseusFastSupportAggregateFixture` mirrors the same finite
counts and no-promotion boundaries.

The checked Lean theorems are
`theseus_fast_support_aggregate_fixture_valid`,
`theseus_fast_support_aggregate_preserves_no_promotion`,
`theseus_fast_support_aggregate_carries_task_and_control_counts`, and
`theseus_fast_support_aggregate_clean_replay_overclaim_rejected`.

This aggregate bridge does not prove clean live Project Theseus replay, does
not prove model quality, benchmark superiority, generation speed,
useful-solution-per-second improvement, routing quality, safety, alignment,
transfer, or ASI, and does not promote any chapter core claim above
`argument`.

## Composed Surfaces

| Surface | Role | Boundary |
|---|---|---|
| `python3 scripts/validate_theseus_generation_mode_import.py` | Static public-safe generation-mode import with Fast Generation Lean bridge | no live replay, no generation-speed claim |
| `python3 scripts/validate_theseus_support_replay_probe.py` | Local replay of the two ASI-side Theseus static-import validators | no clean live Theseus replay |
| `python3 scripts/validate_theseus_public_task_bundle_import.py` | Bounded public task-bundle summary import with no-promotion decision | no model-quality or benchmark-superiority claim |
| `python3 scripts/validate_fast_generation_task_bundle.py` | Local public-safe Fast Generation task-bundle accounting slice | no model-speed, deployment, or useful-solution-per-second model claim |

