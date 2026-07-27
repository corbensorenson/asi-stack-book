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
        "schema_version": "asi_stack.theseus_t0a_architecture_closure_currentness_import.v1",
        "import_id": "theseus-t0a-architecture-closure-currentness-2026-07-27-d5b99128",
        "observed_utc": "2026-07-27T10:08:45Z",
        "source_authority": {
            "project": "Project Theseus / Theseus-Hive",
            "owner": "Corben Sorenson",
            "source_kind": "local_author_owned_implementation_reference",
            "branch": "main",
            "commit": "d5b99128395f6af5a34b731ba024305d2e44433c",
            "worktree_clean": True,
            "ahead_of_origin_main_commit_count": 53,
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
                "sha256": "b7c84562337cbea6641dcef82ec71c3ef384adf740c7a80873907080c5d0f4e6",
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
        ],
        "historical_t0_package": {
            "created_utc": "2026-07-26T14:17:19.993860Z",
            "package_identity": "sha256:9d7dc30b378067c0a254fdca21ef54e3c5469af63c748d3cc49e1f427b251cce",
            "trigger_state": "GREEN",
            "disposition": "architecture_frozen_training_not_started",
            "artifact_count": 123,
            "unchanged_artifact_count": 104,
            "changed_artifact_count": 19,
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
            "architecture_package_current": False,
            "remaining_blockers": [
                "run the guarded replacement independent replay against the current source tree",
                "publish a replacement content-addressed architecture-freeze package binding the current artifacts",
                "rerun the broader pre-training readiness gate against the current 84-chapter ASI Stack after the replacement package exists",
            ],
        },
        "observation_receipts": [
            {
                "command": "python3 $THESEUS_ROOT/scripts/pretraining_architecture_freeze.py --out $TMPDIR/theseus_pretraining_architecture_freeze_2026_07_27.json",
                "exit_code": 1,
                "result": "independent_replay_required",
                "interpretation": "expected fail-closed dry-run result; no replay or source mutation occurred",
            },
            {
                "command": "python3 $THESEUS_ROOT/scripts/roadmap_implementation_gate.py --gate --out $TMPDIR/gate.json --markdown-out $TMPDIR/gate.md --crosswalk-out $TMPDIR/crosswalk.json --ai-book-root $AI_BOOK_ROOT",
                "exit_code": 1,
                "result": "source_side_report_write_forbidden_by_ai_book_workspace_boundary",
                "interpretation": "environmental observation only; not a Theseus architecture or behavior result",
            },
        ],
        "book_disposition": {
            "prior_state": "single_T0_in_progress_row_conflated_historical_and_successor_freezes",
            "new_state": "historical_T0_complete_successor_T0A_active_T1_blocked_by_T0A",
            "next_legal_action": "guarded replacement replay and current content-addressed package publication in Theseus",
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
            "changed_artifact_denominator_shrink",
            "stale_package_marked_current",
            "T0A_marked_complete",
            "T1_unblocked",
            "independent_replay_failure_erasure",
            "protected_outcome_invention",
            "private_payload_copy",
            "support_promotion",
            "release_promotion",
        ],
        "non_claims": [
            "This is a public-safe implementation-reference currentness handoff, not a training or capability result.",
            "A GREEN historical package and GREEN factorized bakeoff do not make the changed current source tree training-ready.",
            "The import does not establish model quality, useful behavior, training success, optimizer superiority, safety, deployment, transfer, AGI, ASI, or SOTA.",
            "The failed dry-run and workspace-boundary observations are not negative evidence about the architecture.",
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
        or authority.get("ahead_of_origin_main_commit_count") != 53
        or authority.get("source_project_mutations") != 0
    ):
        errors.append("source authority or remote-divergence custody drifted")
    old = actual.get("historical_t0_package", {})
    if (
        old.get("artifact_count") != 123
        or old.get("unchanged_artifact_count") != 104
        or old.get("changed_artifact_count") != 19
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
        or current.get("architecture_package_current") is not False
        or len(current.get("remaining_blockers", [])) != 3
    ):
        errors.append("T0/T0A/T1 dependency state drifted")
    receipts = actual.get("observation_receipts", [])
    if (
        len(receipts) != 2
        or receipts[0].get("result") != "independent_replay_required"
        or any(row.get("exit_code") != 1 for row in receipts)
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
    if len(actual.get("negative_controls", [])) != 12:
        errors.append("negative-control denominator drifted")
    return errors


def render(record: dict) -> str:
    authority = record["source_authority"]
    old = record["historical_t0_package"]
    current = record["current_t0a_state"]
    return f"""# Project Theseus T0A architecture-closure currentness import

Observed on 2026-07-27 from clean Project Theseus `main` at
`{authority['commit']}`. The local branch was {authority['ahead_of_origin_main_commit_count']}
commits ahead of `origin/main`; this import records the exact local
author-owned implementation state and does not imply that the source repository
has published those commits.

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
GREEN. Those records organize the selected route and scoped exclusions; they
do not substitute for the current content-addressed package.

## Remaining T0A work

1. Run the guarded replacement independent replay against the current tree.
2. Publish the replacement content-addressed architecture-freeze package.
3. Re-run the broader readiness gate against the current 84-chapter ASI Stack.

A dry-run without `--execute-replays` failed closed with
`independent_replay_required`, as designed. The attempted roadmap-gate
observation also stopped at the AI-book workspace boundary because the Theseus
gate refreshes source-side reports. Neither result is architecture
counterevidence.

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
        ("remote divergence", lambda x: x["source_authority"].__setitem__("ahead_of_origin_main_commit_count", 0)),
        ("artifact denominator", lambda x: x["historical_t0_package"].__setitem__("changed_artifact_count", 0)),
        ("stale package current", lambda x: x["historical_t0_package"].__setitem__("current_for_source_commit", True)),
        ("T0A complete", lambda x: x["current_t0a_state"].__setitem__("t0a_state", "complete")),
        ("T1 unblocked", lambda x: x["current_t0a_state"].__setitem__("t1_state", "ready")),
        ("replay erasure", lambda x: x["observation_receipts"][0].__setitem__("result", "passed")),
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
        "T1 blocked; 104/123 frozen artifacts unchanged, 19 changed, "
        "zero outcomes/support/release movement, 12 rejecting controls."
    )


if __name__ == "__main__":
    main()
