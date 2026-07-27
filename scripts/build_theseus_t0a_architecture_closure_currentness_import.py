#!/usr/bin/env python3
"""Build and validate the public-safe Theseus T0/T0A currentness handoff."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD = (
    ROOT
    / "experiments/theseus_t0a_architecture_closure_currentness_import"
    / "results/2026-07-27-local.json"
)
DOC = ROOT / "docs/theseus_t0a_architecture_closure_currentness_import.md"


def build() -> dict:
    return {
        "schema_version": "asi_stack.theseus_t0a_architecture_closure_currentness_import.v3",
        "import_id": "theseus-t0a-architecture-closure-currentness-2026-07-27-24955417",
        "observed_utc": "2026-07-27T12:22:52Z",
        "source_authority": {
            "project": "Project Theseus / Theseus-Hive",
            "owner": "Corben Sorenson",
            "source_kind": "local_author_owned_implementation_reference",
            "branch": "main",
            "commit": "24955417161e40587bb9eec7b091618d96e370ba",
            "worktree_clean": True,
            "ahead_of_origin_main_commit_count": 0,
            "published_on_origin_main": True,
            "source_project_mutations": 0,
            "network_calls": 0,
            "external_inference_calls": 0,
        },
        "frozen_source_files": [
            {
                "path": "configs/roadmap_implementation_matrix.json",
                "sha256": "3a3ee6037d915a50df9eeb1dfbdabdb512e943e404a4918095c071946cc32417",
                "bytes": 926634,
            },
            {
                "path": "configs/pretraining_architecture_freeze.json",
                "sha256": "27bc33c30cdce630912b53eb543160ac2bfc8636780aa6280b6166c8aa06e57e",
                "bytes": 26935,
            },
            {
                "path": "reports/pretraining_architecture_freeze_package.json",
                "sha256": "12217a2969e950622882f43d3a801a80e3d0c49da6250f520ca084ed7dfaa8c0",
                "bytes": 171879,
            },
            {
                "path": "reports/pretraining_factorized_bakeoff.json",
                "sha256": "cba6a1d09919eae9bd653a8619fdfce4a76c482762464193cb700779e74cb29d",
                "bytes": 5587,
            },
            {
                "path": "configs/pretraining_architecture_candidates.json",
                "sha256": "83701918935f22d9b9dd0d5e4fa8d7b5c4391eab047c83fffdad78fe6ba66c29",
                "bytes": 34861,
            },
            {
                "path": "configs/training_acceleration_final_selector.json",
                "sha256": "c0fdb87d5f777b98649403f7fb7eb7d5ede962f4a4487894461324ee35ffa593",
                "bytes": 2561,
            },
            {
                "path": "reports/training_acceleration_final_selector.json",
                "sha256": "3a347abe77866a8f9e9665bdb4b2fed26c34445561497102ea313145add1b1b2",
                "bytes": 8704,
            },
            {
                "path": "configs/project_manifest_registry.json",
                "sha256": "40853038521351fea6e1873a7fb5ea2732dea8148663ec720dd5cb69ff357f58",
                "bytes": 520627,
            },
            {
                "path": "reports/accelerator_replay/optimizer_matched_adequacy_guard.json",
                "sha256": "d3147b20511f2af530c609930ee5756c011e54b0bbcae894979c85bac799859a",
                "bytes": 27715,
            },
            {
                "path": "reports/replay_safety/00.json",
                "sha256": "72c6322c053e089adcd5539e59ba534ada252d6a3e1d4188386c23a6886eb961",
                "bytes": 33180,
            },
            {
                "path": "reports/replay_safety/01.json",
                "sha256": "e925d575268116d82bf16571a769cc1ffbf09f86a9cb7252308a6c1ed8ca2027",
                "bytes": 30271,
            },
            {
                "path": "reports/replay_safety/02.json",
                "sha256": "71b30334b96101570ae3f8eaf015fd7079b94839a22fab0ea7027e2645cc0678",
                "bytes": 7270,
            },
            {
                "path": "reports/replay_safety/03.json",
                "sha256": "3cb8e95609914d2f40db6c74628844914392c046e935c8ec46319aaf8bd0453d",
                "bytes": 3595,
            },
            {
                "path": "reports/replay_safety/04.json",
                "sha256": "2a786cc7a93b2c5137dd809913eadb8e95e4d30cae168697f7068717c73d2467",
                "bytes": 2833,
            },
            {
                "path": "reports/replay_safety/05.json",
                "sha256": "ba65d9dd096157e28f31edd2ec941e1e9fc2c2fc7ba0599e3ebfdeddae98514a",
                "bytes": 2889,
            },
            {
                "path": "reports/replay_safety/06.json",
                "sha256": "888f10e5f626ac68c4d2f478c7b049974e4cf1d274ee90fc066964a53fddc021",
                "bytes": 31140,
            },
            {
                "path": "roadmap.md",
                "sha256": "6fdaa33f1e63551f376917c867ed63efb434caf1a211da624a1fb9d181d11425",
                "bytes": 243460,
            },
        ],
        "historical_t0_package": {
            "created_utc": "2026-07-26T14:17:19.993860Z",
            "package_identity": "sha256:9d7dc30b378067c0a254fdca21ef54e3c5469af63c748d3cc49e1f427b251cce",
            "trigger_state": "GREEN",
            "disposition": "architecture_frozen_training_not_started",
            "artifact_count": 123,
            "unchanged_artifact_count": 102,
            "changed_artifact_count": 21,
            "missing_artifact_count": 0,
            "current_for_source_commit": False,
            "role": "immutable_historical_control_only",
        },
        "current_t0a_state": {
            "t0_state": "complete",
            "t0a_state": "active",
            "t1_state": "blocked_by_T0A",
            "strict_architecture_first_enforcement": True,
            "training_authority_state": "denied_until_finite_docket_and_freeze_package_are_green",
            "finite_docket_closed_to_untriggered_new_architecture_families": True,
            "factorized_bakeoff_trigger_state": "GREEN",
            "factorized_bakeoff_disposition": "factorized_architecture_selected_training_not_started",
            "acceleration_selector_trigger_state": "GREEN",
            "project_registry_trigger_state": "GREEN",
            "project_registry_blocker_count": 0,
            "cpu_governance_replay_requested_count": 7,
            "cpu_governance_replay_passed_count": 7,
            "cpu_governance_replay_complete": True,
            "accelerator_replay_requested_count": 14,
            "accelerator_replay_valid_count": 13,
            "accelerator_replay_invalid_count": 1,
            "invalid_accelerator_shard_id": "optimizer_matched_adequacy",
            "invalid_accelerator_child_started": True,
            "invalid_accelerator_fault": "host_memory_reserve_breached",
            "invalid_accelerator_initial_reclaimable_available_mib": 5216.328,
            "invalid_accelerator_minimum_reclaimable_available_mib": 3686.562,
            "invalid_accelerator_fault_reclaimable_available_mib": 3708.391,
            "invalid_accelerator_live_reserve_mib": 4096.0,
            "invalid_accelerator_maximum_inferred_unified_memory_mib": 1529.766,
            "invalid_accelerator_maximum_process_rss_mib": 231.75,
            "invalid_accelerator_maximum_swapout_growth_mib": 0.0,
            "architecture_package_current": False,
            "remaining_blockers": [
                "run the unchanged guarded optimizer-matched accelerator replay in a quiescent host window that preserves both the 5120 MiB launch reserve and the 4096 MiB live reserve",
                "publish a replacement content-addressed architecture-freeze package binding the current artifacts",
            ],
            "post_t0a_pretraining_prerequisite": "rerun the broader pre-training readiness gate against the current 84-chapter ASI Stack after the replacement package exists",
        },
        "observation_receipts": [
            {
                "command": "python3 scripts/pretraining_architecture_freeze.py --execute-replays",
                "exit_code": 1,
                "result": "seven_cpu_governance_replays_passed_then_freeze_refused_for_one_invalid_accelerator_receipt",
                "interpretation": "partial replay custody only; the replacement package was not written",
            },
            {
                "command": "python3 scripts/pretraining_architecture_freeze.py --run-accelerator-shards --accelerator-shard optimizer_matched_adequacy",
                "exit_code": 2,
                "result": "child_started_then_host_memory_live_reserve_breached",
                "interpretation": "the 5120 MiB launch reserve passed, but the external guard stopped the child after reclaimable memory fell below the 4096 MiB live reserve; maximum inferred unified memory was 1529.766 MiB, maximum process RSS was 231.75 MiB, and swapout growth was zero",
            },
            {
                "command": "python3 scripts/theseus_project_registry.py --gate",
                "exit_code": 0,
                "result": "GREEN_zero_blockers",
                "interpretation": "the exact replacement binding repair restored registry and cleanup-queue custody without adding a waiver",
            },
        ],
        "book_disposition": {
            "prior_state": "T0A_active_before_guarded_replay_attempt",
            "new_state": "T0A_active_with_7_of_7_cpu_replays_green_13_of_14_accelerator_receipts_valid_latest_shard_stopped_by_live_memory_guard_and_replacement_freeze_unpublished",
            "next_legal_action": "run only the unchanged guarded optimizer-matched shard in a quiescent host window that preserves its launch and live reserves, then publish the replacement package",
            "protected_outcomes_opened": 0,
            "support_state_effect": "none",
            "release_effect": "none",
        },
        "public_safety": {
            "raw_gate_copied": False,
            "raw_crosswalk_copied": False,
            "private_payloads_copied": 0,
            "training_rows_copied": 0,
            "prompts_copied": 0,
            "solutions_copied": 0,
            "checkpoints_copied": 0,
            "held_out_outcomes_copied": 0,
            "restricted_paths_copied": 0,
        },
        "negative_controls": [
            "source_commit_substitution",
            "dirty_worktree_erasure",
            "remote_divergence_erasure",
            "origin_main_publication_erasure",
            "changed_artifact_denominator_shrink",
            "stale_package_marked_current",
            "T0A_marked_complete",
            "T1_unblocked",
            "cpu_replay_failure_invention",
            "accelerator_denominator_shrink",
            "invalid_accelerator_receipt_erasure",
            "accelerator_child_start_erasure",
            "protected_outcome_invention",
            "private_payload_copy",
            "support_promotion",
            "release_promotion",
        ],
        "non_claims": [
            "This is a public-safe implementation-reference currentness handoff, not a training or capability result.",
            "A GREEN historical package and GREEN factorized bakeoff do not make the changed current source tree training-ready.",
            "The import does not establish model quality, useful behavior, training success, optimizer superiority, safety, deployment, transfer, AGI, ASI, or SOTA.",
            "The runtime memory-reserve stop is not negative evidence about the optimizer or architecture.",
            "Seven CPU/governance passes and thirteen valid accelerator receipts do not make a fourteen-receipt freeze complete.",
            "No chapter-core or non-core support state changes.",
        ],
    }


def validate(actual: dict, expected: dict) -> list[str]:
    errors: list[str] = []
    if actual != expected:
        errors.append("T0A currentness import differs from the exact sanitized observation")
    authority = actual.get("source_authority", {})
    if (
        authority.get("branch") != "main"
        or authority.get("worktree_clean") is not True
        or authority.get("ahead_of_origin_main_commit_count") != 0
        or authority.get("published_on_origin_main") is not True
        or authority.get("source_project_mutations") != 0
    ):
        errors.append("source authority or remote-divergence custody drifted")
    old = actual.get("historical_t0_package", {})
    if (
        old.get("artifact_count") != 123
        or old.get("unchanged_artifact_count") != 102
        or old.get("changed_artifact_count") != 21
        or old.get("missing_artifact_count") != 0
        or old.get("current_for_source_commit") is not False
        or old.get("role") != "immutable_historical_control_only"
    ):
        errors.append("historical package currentness boundary drifted")
    current = actual.get("current_t0a_state", {})
    if (
        current.get("t0_state") != "complete"
        or current.get("t0a_state") != "active"
        or current.get("t1_state") != "blocked_by_T0A"
        or current.get("project_registry_trigger_state") != "GREEN"
        or current.get("project_registry_blocker_count") != 0
        or current.get("cpu_governance_replay_requested_count") != 7
        or current.get("cpu_governance_replay_passed_count") != 7
        or current.get("cpu_governance_replay_complete") is not True
        or current.get("accelerator_replay_requested_count") != 14
        or current.get("accelerator_replay_valid_count") != 13
        or current.get("accelerator_replay_invalid_count") != 1
        or current.get("invalid_accelerator_shard_id") != "optimizer_matched_adequacy"
        or current.get("invalid_accelerator_child_started") is not True
        or current.get("invalid_accelerator_fault") != "host_memory_reserve_breached"
        or current.get("invalid_accelerator_live_reserve_mib") != 4096.0
        or current.get("invalid_accelerator_maximum_swapout_growth_mib") != 0.0
        or current.get("architecture_package_current") is not False
        or len(current.get("remaining_blockers", [])) != 2
    ):
        errors.append("T0/T0A/T1 dependency state drifted")
    receipts = actual.get("observation_receipts", [])
    if (
        len(receipts) != 3
        or receipts[0].get("result")
        != "seven_cpu_governance_replays_passed_then_freeze_refused_for_one_invalid_accelerator_receipt"
        or receipts[1].get("result") != "child_started_then_host_memory_live_reserve_breached"
        or receipts[2].get("result") != "GREEN_zero_blockers"
        or [row.get("exit_code") for row in receipts] != [1, 2, 0]
    ):
        errors.append("fail-closed observation receipts drifted")
    disposition = actual.get("book_disposition", {})
    if (
        disposition.get("protected_outcomes_opened") != 0
        or disposition.get("support_state_effect") != "none"
        or disposition.get("release_effect") != "none"
    ):
        errors.append("book disposition launders outcomes, support, or release")
    safety = actual.get("public_safety", {})
    if any(safety.get(key) for key in safety):
        errors.append("public-safety boundary failed")
    if len(actual.get("negative_controls", [])) != 16:
        errors.append("negative-control denominator drifted")
    return errors


def render(record: dict) -> str:
    authority = record["source_authority"]
    old = record["historical_t0_package"]
    current = record["current_t0a_state"]
    return f"""# Project Theseus T0A architecture-closure currentness import

Observed on 2026-07-27 from clean Project Theseus `main` at
`{authority['commit']}`. The local branch was {authority['ahead_of_origin_main_commit_count']}
commits ahead of `origin/main`, and the observed commit is published on
`origin/main`. This import records that exact clean author-owned implementation
state.

## Dependency correction

| Gate | Exact state | Meaning |
|---|---|---|
| `T0` | `{current['t0_state']}` | The prior 57M architecture package remains an immutable historical control. |
| `T0A` | `{current['t0a_state']}` | The successor finite architecture docket is selected, but its replacement freeze is not current. |
| `T1` | `{current['t1_state']}` | Long training may not inherit authority from the stale `T0` package. |

The 2026-07-26 package recorded `{old['artifact_count']}` artifacts. Direct
digest comparison against the observed source tree found
`{old['unchanged_artifact_count']}` unchanged, `{old['changed_artifact_count']}`
changed, and `{old['missing_artifact_count']}` missing. Its GREEN state and
identity `{old['package_identity']}` therefore remain historical facts, not
current training authority.

## What is already organized

The finite docket is closed to untriggered architecture expansion. The matched
factorized bakeoff is GREEN with disposition
`{current['factorized_bakeoff_disposition']}`, and the acceleration selector is
GREEN. The exact replacement binding repair leaves the project registry GREEN
with zero blockers. All `{current['cpu_governance_replay_requested_count']}`
CPU/governance replays are current and green. Of
`{current['accelerator_replay_requested_count']}` selected accelerator receipts,
`{current['accelerator_replay_valid_count']}` validate. Those records organize
the selected route and scoped exclusions; they do not substitute for the
current content-addressed package.

## Remaining T0A work

1. Run the unchanged guarded optimizer-matched accelerator shard in a quiescent
   host window that preserves both its 5,120 MiB launch reserve and 4,096 MiB
   live reserve.
2. Publish the replacement content-addressed architecture-freeze package.

The latest remaining-shard attempt passed its 5,120 MiB launch reserve and
started. The external guard stopped it after reclaimable memory fell to
3,708.391 MiB, below the declared 4,096 MiB live reserve. Maximum inferred
unified memory was 1,529.766 MiB, maximum process RSS was 231.75 MiB, and
swapout growth was zero. This preserves host safety and is not optimizer or
architecture counterevidence, but it also does not complete the replay. After
`T0A`, the broader readiness gate must be rerun against the current 84-chapter
ASI Stack before `T1`.

## Boundary

No training, held-out task, model output, private payload, checkpoint, support
transition, or release transition was opened. This packet establishes
dependency and artifact currentness only; it does not establish model quality,
useful behavior, safety, deployment, transfer, AGI, ASI, or SOTA.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    expected = build()
    markdown = render(expected)
    if args.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(
            json.dumps(expected, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        DOC.write_text(markdown, encoding="utf-8")
    if not RECORD.exists() or not DOC.exists():
        raise SystemExit("T0A currentness import missing; run with --write")
    actual = json.loads(RECORD.read_text(encoding="utf-8"))
    errors = validate(actual, expected)
    if DOC.read_text(encoding="utf-8") != markdown:
        errors.append("T0A human report drifted")
    mutations = [
        ("commit", lambda x: x["source_authority"].__setitem__("commit", "0" * 40)),
        ("dirty", lambda x: x["source_authority"].__setitem__("worktree_clean", False)),
        ("remote divergence", lambda x: x["source_authority"].__setitem__("ahead_of_origin_main_commit_count", 1)),
        ("origin publication", lambda x: x["source_authority"].__setitem__("published_on_origin_main", False)),
        ("artifact denominator", lambda x: x["historical_t0_package"].__setitem__("changed_artifact_count", 0)),
        ("stale package current", lambda x: x["historical_t0_package"].__setitem__("current_for_source_commit", True)),
        ("T0A complete", lambda x: x["current_t0a_state"].__setitem__("t0a_state", "complete")),
        ("T1 unblocked", lambda x: x["current_t0a_state"].__setitem__("t1_state", "ready")),
        ("cpu replay failure", lambda x: x["current_t0a_state"].__setitem__("cpu_governance_replay_passed_count", 6)),
        ("accelerator denominator", lambda x: x["current_t0a_state"].__setitem__("accelerator_replay_requested_count", 13)),
        ("invalid accelerator erasure", lambda x: x["current_t0a_state"].__setitem__("accelerator_replay_invalid_count", 0)),
        ("child start erasure", lambda x: x["current_t0a_state"].__setitem__("invalid_accelerator_child_started", False)),
        ("outcome invention", lambda x: x["book_disposition"].__setitem__("protected_outcomes_opened", 1)),
        ("private copy", lambda x: x["public_safety"].__setitem__("private_payloads_copied", 1)),
        ("support promotion", lambda x: x["book_disposition"].__setitem__("support_state_effect", "prototype-backed")),
        ("release promotion", lambda x: x["book_disposition"].__setitem__("release_effect", "published")),
    ]
    for label, mutate in mutations:
        candidate = copy.deepcopy(actual)
        mutate(candidate)
        if not validate(candidate, expected):
            errors.append(f"negative mutation accepted: {label}")
    if errors:
        raise SystemExit("Theseus T0A currentness import failed:\n - " + "\n - ".join(errors))
    print(
        "Theseus T0A currentness import passed: T0 complete, T0A active, "
        "T1 blocked; 102/123 frozen artifacts unchanged, 21 changed; "
        "7/7 CPU replays green, 13/14 accelerator receipts valid, "
        "zero outcomes/support/release movement, 16 rejecting controls."
    )


if __name__ == "__main__":
    main()
