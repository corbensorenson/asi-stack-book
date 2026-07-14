#!/usr/bin/env python3
"""Build the sanitized fresh Project Theseus readiness-currentness import."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments/theseus_pretraining_readiness_currentness_import"
RECORD = BASE / "results/2026-07-14-local.json"
DOC = ROOT / "docs/theseus_pretraining_readiness_currentness_import.md"


def build() -> dict:
    return {
        "schema_version": "asi_stack.theseus_pretraining_readiness_currentness_import.v0",
        "import_id": "theseus-pretraining-readiness-currentness-2026-07-14-d2343540",
        "observed_utc": "2026-07-14T08:30:37.235577+00:00",
        "source_authority": {
            "project": "Project Theseus / Theseus-Hive",
            "owner": "Corben Sorenson",
            "source_kind": "local_author_owned_implementation_reference",
            "commit": "d2343540a17ea3e12760983f653529621fa445f1",
            "head_before": "d2343540a17ea3e12760983f653529621fa445f1",
            "head_after": "d2343540a17ea3e12760983f653529621fa445f1",
            "clean_before": True,
            "clean_after": True,
            "network_calls": 0,
            "external_inference_calls": 0,
        },
        "frozen_source_files": [
            {"path": "scripts/roadmap_implementation_gate.py", "sha256": "8a40511d9f9e4c3a284735586a7a1cd2b4edc553db8f81e3e4486c54af328178", "bytes": 103652},
            {"path": "configs/roadmap_implementation_matrix.json", "sha256": "6ca1a43fd29fba1c721aaefa800a7c68127d2a00d3e256dbed0c24b0e13c7b47", "bytes": 556313},
            {"path": "configs/project_manifest_registry.json", "sha256": "78f22273dac9c9b44d7a5b54513b49a74f514091851924a5bcd6962cac776e1b", "bytes": 465434},
        ],
        "replay": {
            "command": "python3 $THESEUS_ROOT/scripts/roadmap_implementation_gate.py --gate --require-pre-training-ready --out $TMPDIR/gate.json --markdown-out $TMPDIR/gate.md --crosswalk-out $TMPDIR/crosswalk.json --ai-book-root $AI_BOOK_ROOT",
            "exit_code": 0,
            "environment": "local macOS arm64; Python 3; isolated temporary outputs; no source-project write",
            "expected_outputs": ["gate.json", "gate.md", "crosswalk.json", "stdout.txt"],
            "outputs": [
                {"name": "gate.json", "sha256": "dfa888a352f9aaaf81b8f166657a52fb1a35972bb700862e0ec56757c7681587", "bytes": 48298},
                {"name": "gate.md", "sha256": "5c88d672c22343c472d78d64c4c7ce3c80fc01b8af99593aa8239990c5041b6d", "bytes": 6084},
                {"name": "crosswalk.json", "sha256": "b1bf7615a802ef83011ae937790b7a0d35376d464b93e435a33aabe4001d76bf", "bytes": 1481519},
                {"name": "stdout.txt", "sha256": "dcaa9b9767892375871630113473066ca0dab75c0feb40d5d5054a5aaf90ad89", "bytes": 4126},
            ],
            "artifact_truth_checks": {
                "same_commit_before_after": True,
                "clean_checkout_before_after": True,
                "require_pre_training_ready_exit_zero": True,
                "temporary_output_only": True,
                "source_project_mutations": 0,
            },
        },
        "sanitized_summary": {
            "trigger_state": "YELLOW",
            "phase_count": 20,
            "required_phase_count": 20,
            "phase_status_counts": {"wired": 12, "implemented": 2, "partial": 5, "frozen": 1},
            "implemented_or_wired_count": 14,
            "missing_count": 0,
            "hard_gap_count": 0,
            "warning_count": 1,
            "pre_training_architecture_ready": True,
            "pre_training_architecture_blocker_count": 0,
            "pre_training_architecture_warning_count": 0,
            "externally_frozen_phase_count": 1,
            "externally_frozen_phase": {"phase": 9, "title": "Hive Policy-First Distributed Operation", "reason_class": "trusted_peers_and_eligible_remote_device_unreachable"},
            "deferred_training_or_behavior_phases": [5, 7, 10, 13, 16],
            "book_manifest_chapter_count": 54,
            "book_manifest_commit": "32635eb94ded42a5f54e528302685cab343993b7",
            "book_manifest_digest_match": True,
            "book_manifest_order_match": True,
            "live_book_manifest_differs_from_pin": True,
            "book_active_flagship_lane_id": "C1_correctness_rl_and_generator_survival_lane",
            "book_active_core_slice_count": 1,
            "book_to_theseus_crosswalk_item_count": 20,
            "theseus_to_book_evidence_count": 73,
            "book_to_theseus_source_sync_smoke_passed": True,
            "public_safe_evidence_smoke_passed": True,
        },
        "currentness_residual": {
            "id": "THESEUS-CURRENTNESS-PRETRAINING-READINESS",
            "prior_state": "fresh post-accelerator-parity implementation currentness lane absent",
            "new_state": "closed_for_exact_d2343540_readiness_gate_observation_only",
            "remaining": ["The imported book pin is 32635eb94 and intentionally predates current ASI Stack source work.", "Five training/behavior phases remain partial and phase 9 remains externally frozen.", "YELLOW readiness is not deployment readiness, model quality, benchmark performance, or clean open-world replay.", "Future Theseus commits supersede currentness but do not falsify this exact historical observation."],
        },
        "public_safety": {
            "raw_gate_copied": False,
            "raw_crosswalk_copied": False,
            "private_payloads_copied": 0,
            "training_rows_copied": 0,
            "prompts_copied": 0,
            "solutions_copied": 0,
            "checkpoints_copied": 0,
            "restricted_paths_copied": 0,
            "allowed_fields": "aggregate phase/status counts, exact public-safe digests, commit identity, command receipt, bounded residuals, and non-claims",
        },
        "negative_controls": [
            "source_commit_mismatch",
            "dirty_checkout_hidden",
            "gate_exit_failure_hidden",
            "output_digest_mismatch",
            "missing_partial_or_frozen_phase",
            "private_payload_copied",
            "deployment_readiness_overclaim",
            "chapter_core_promotion_overclaim",
        ],
        "support_state_effect": "none",
        "release_effect": "none",
        "non_claims": [
            "This is implementation-reference currentness evidence only.",
            "The import does not prove learned model quality, benchmark superiority, training success, useful throughput, production routing, distributed operation, deployment readiness, safety, alignment, transfer, AGI, or ASI.",
            "The import does not prove current behavior after source commit d2343540a17ea3e12760983f653529621fa445f1.",
            "The readiness gate's own YELLOW/ready distinction and partial/frozen phases remain visible.",
            "No chapter-core or non-core support state is promoted.",
        ],
    }


def validate(actual: dict, expected: dict) -> list[str]:
    errors = []
    if actual != expected: errors.append("currentness import differs from exact sanitized observation")
    authority = actual.get("source_authority", {})
    if authority.get("head_before") != authority.get("head_after") or authority.get("clean_before") is not True or authority.get("clean_after") is not True: errors.append("clean same-commit authority missing")
    replay = actual.get("replay", {})
    checks = replay.get("artifact_truth_checks", {})
    if (
        replay.get("exit_code") != 0
        or len(replay.get("outputs", [])) != 4
        or any(checks.get(key) is not True for key in ["same_commit_before_after", "clean_checkout_before_after", "require_pre_training_ready_exit_zero", "temporary_output_only"])
        or checks.get("source_project_mutations") != 0
    ):
        errors.append("replay or artifact truth checks failed")
    summary = actual.get("sanitized_summary", {})
    if summary.get("trigger_state") != "YELLOW" or summary.get("pre_training_architecture_ready") is not True or summary.get("phase_status_counts") != {"wired": 12, "implemented": 2, "partial": 5, "frozen": 1}: errors.append("readiness boundary drifted")
    safety = actual.get("public_safety", {})
    if any(safety.get(key) for key in ["raw_gate_copied", "raw_crosswalk_copied", "private_payloads_copied", "training_rows_copied", "prompts_copied", "solutions_copied", "checkpoints_copied", "restricted_paths_copied"]): errors.append("public-safety boundary failed")
    if actual.get("support_state_effect") != "none" or actual.get("release_effect") != "none": errors.append("import launders support or release")
    return errors


def render(record: dict) -> str:
    s = record["sanitized_summary"]; r = record["replay"]; c = record["currentness_residual"]
    return f"""# Project Theseus pre-training readiness currentness import

Recorded from one clean, same-commit, temporary-output replay at `{record['source_authority']['commit']}` on 2026-07-14. This is the fresh post-accelerator-parity currentness lane required by the active roadmap.

## Exact observation

| Field | Observation |
|---|---|
| Gate route | `--gate --require-pre-training-ready`; exit {r['exit_code']} |
| Trigger state | `{s['trigger_state']}` |
| Architecture-ready boundary | `{str(s['pre_training_architecture_ready']).lower()}` for training/public-calibration focus, not deployment |
| Phase states | 12 wired; 2 implemented; 5 partial; 1 externally frozen; 0 missing |
| Hard gaps | {s['hard_gap_count']} |
| External frozen phase | 9 — Hive Policy-First Distributed Operation; trusted peers/eligible remote device unavailable |
| Book pin used by Theseus | `{s['book_manifest_commit']}`; 54 chapters; digest/order match; live book differs from pin |
| Crosswalk/evidence summary | {s['book_to_theseus_crosswalk_item_count']} crosswalk items; {s['theseus_to_book_evidence_count']} evidence items; source-sync and public-safe smoke pass |

The exact temporary outputs were hashed but not copied. The import retains aggregate public-safe facts, the command receipt, source/output digests, partial/frozen phases, and non-claims. It contains no raw gate, raw crosswalk, private payload, training row, prompt, solution, checkpoint, or restricted path.

## Residual disposition

`{c['id']}` is closed only for the exact `d2343540` observation. Five training/behavior phases remain partial, phase 9 remains externally frozen, and the gate is YELLOW. Later Project Theseus commits supersede currentness; they do not turn this record into a claim about their behavior.

## Boundary

Implementation-reference currentness only. No support state or release changes. The replay does not establish learned model quality, benchmark superiority, training success, useful throughput, production routing, distributed operation, deployment readiness, safety, alignment, transfer, AGI, or ASI.
"""


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    expected = build(); md = render(expected)
    if args.write:
        RECORD.parent.mkdir(parents=True, exist_ok=True); RECORD.write_text(json.dumps(expected, indent=2) + "\n"); DOC.write_text(md)
    if not RECORD.exists() or not DOC.exists(): raise SystemExit("Theseus currentness import missing; run --write")
    actual = json.loads(RECORD.read_text()); errors = validate(actual, expected)
    if DOC.read_text() != md: errors.append("currentness report drifted")
    for label, mutate in [("commit", lambda x: x["source_authority"].__setitem__("head_after", "0" * 40)), ("dirty", lambda x: x["source_authority"].__setitem__("clean_after", False)), ("digest", lambda x: x["replay"]["outputs"][0].__setitem__("sha256", "0" * 64)), ("partial erasure", lambda x: x["sanitized_summary"]["phase_status_counts"].__setitem__("partial", 0)), ("private copy", lambda x: x["public_safety"].__setitem__("private_payloads_copied", 1)), ("release overclaim", lambda x: x.__setitem__("release_effect", "published")), ("support overclaim", lambda x: x.__setitem__("support_state_effect", "prototype-backed")), ("yellow erasure", lambda x: x["sanitized_summary"].__setitem__("trigger_state", "GREEN"))]:
        candidate = copy.deepcopy(actual); mutate(candidate)
        if not validate(candidate, expected): errors.append(f"negative mutation accepted: {label}")
    if errors: raise SystemExit("Theseus currentness import failed:\n - " + "\n - ".join(errors))
    print("Theseus currentness import passed: clean same-commit d2343540 replay, 20 phases (12 wired/2 implemented/5 partial/1 frozen), YELLOW readiness boundary, 4 output digests, no private payload, no support effect, and 8 rejecting controls.")


if __name__ == "__main__": main()
