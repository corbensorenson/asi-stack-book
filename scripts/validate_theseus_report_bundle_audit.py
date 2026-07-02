#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "experiments" / "theseus_report_bundle_audit" / "fixtures" / "valid"
INVALID_DIR = ROOT / "experiments" / "theseus_report_bundle_audit" / "fixtures" / "invalid"
VALID_FIXTURE = VALID_DIR / "report_bundle_public_audit.valid.json"
RESULT = ROOT / "experiments" / "theseus_report_bundle_audit" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "theseus_report_bundle_audit.md"

AUDIT_ID = "theseus-report-bundle-audit-2026-07-02-local"
COMMAND = "python3 scripts/validate_theseus_report_bundle_audit.py"
REQUIRED_COMPONENTS = {
    "goal_contract",
    "compiler_artifact",
    "work_board_item",
    "gate_record",
    "residual_record",
    "non_claim",
    "review_note",
    "publication_boundary",
}
ALLOWED_GATE_DECISIONS = {
    "residual_retention",
    "promotion_blocker_if_absent",
    "promotion_boundary",
    "block_promotion",
    "artifact_gap_blocks_support_movement",
}
REQUIRED_NON_CLAIMS = (
    "does not rerun Project Theseus",
    "does not import a clean live Theseus report bundle",
    "does not prove benchmark performance",
    "does not promote any chapter core claim above argument",
    "does not create a support-state transition",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus report-bundle audit validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def set_path(value: dict[str, Any], path: str, new_value: Any) -> None:
    cursor: Any = value
    parts = path.split(".")
    for part in parts[:-1]:
        if isinstance(cursor, dict):
            cursor = cursor[part]
        elif isinstance(cursor, list):
            cursor = cursor[int(part)]
        else:
            raise KeyError(path)
    last = parts[-1]
    if isinstance(cursor, dict):
        cursor[last] = new_value
    elif isinstance(cursor, list):
        cursor[int(last)] = new_value
    else:
        raise KeyError(path)


def require_string(owner: str, value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{owner} missing {field}.")


def validate_scalars(record: dict[str, Any], owner: str, errors: list[str]) -> None:
    expected = {
        "schema_version": "0.1",
        "audit_id": AUDIT_ID,
        "record_kind": "theseus_report_bundle_audit",
        "audit_scope": "public_safe_repository_fixture_only",
        "local_only": True,
        "live_theseus_replay": False,
        "imported_live_report_bundle": False,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
    }
    for key, expected_value in expected.items():
        if record.get(key) != expected_value:
            if key == "support_state_effect":
                errors.append(f"{owner}: support_state_effect must remain none.")
            else:
                errors.append(f"{owner}: {key} must be {expected_value!r}.")


def validate_components(record: dict[str, Any], owner: str, errors: list[str]) -> None:
    components = record.get("bundle_components")
    if not isinstance(components, list):
        errors.append(f"{owner}: bundle_components must be a list.")
        return
    by_name = {row.get("component"): row for row in components if isinstance(row, dict)}
    missing = REQUIRED_COMPONENTS - set(by_name)
    if missing:
        errors.append(f"{owner}: bundle_components missing {sorted(missing)}.")
    for component in sorted(REQUIRED_COMPONENTS):
        row = by_name.get(component)
        if not isinstance(row, dict):
            continue
        if row.get("present") is not True or row.get("public_safe") is not True:
            errors.append(f"{owner}: bundle component {component} must be present and public-safe.")
        require_string(owner, row.get("ref"), f"bundle component {component} ref", errors)


def validate_replay_rows(record: dict[str, Any], owner: str, errors: list[str]) -> tuple[int, int]:
    rows = record.get("replay_readiness_rows")
    if not isinstance(rows, list):
        errors.append(f"{owner}: replay_readiness_rows must be a list.")
        return 0, 0
    ready = 0
    blocked = 0
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f"{owner}: replay_readiness_rows contains a non-object row.")
            continue
        row_id = str(row.get("row_id", "<missing>"))
        if row.get("replay_ready") is True:
            ready += 1
            for field in (
                "command",
                "environment_notes",
                "input_boundary",
                "artifact_checksum",
                "expected_output_class",
                "failure_behavior",
            ):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    errors.append(f"{owner}: replay-ready row {row_id} missing {field}.")
        else:
            blocked += 1
            if not isinstance(row.get("blocked_reason"), str) or not row["blocked_reason"].strip():
                errors.append(f"{owner}: blocked replay row {row_id} must name blocked_reason.")
    if ready < 2:
        errors.append(f"{owner}: expected at least two replay-ready rows.")
    if blocked < 1:
        errors.append(f"{owner}: expected at least one blocked replay row.")
    return ready, blocked


def validate_crosswalk(record: dict[str, Any], owner: str, errors: list[str]) -> int:
    rows = record.get("crosswalk_rows")
    if not isinstance(rows, list):
        errors.append(f"{owner}: crosswalk_rows must be a list.")
        return 0
    required_layers = {
        "intent_and_goal_contract",
        "planning_and_semantic_ir",
        "operator_work_board",
        "architecture_gate",
        "generation_mode_gate",
        "residual_ledger",
        "self_evolution_ladder",
        "publication_boundary",
    }
    observed = {row.get("stack_layer") for row in rows if isinstance(row, dict)}
    missing = required_layers - observed
    if missing:
        errors.append(f"{owner}: crosswalk_rows missing layers {sorted(missing)}.")
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f"{owner}: crosswalk_rows contains a non-object row.")
            continue
        layer = row.get("stack_layer", "<missing>")
        for field in ("artifact_refs", "source_ids"):
            if not isinstance(row.get(field), list) or not row[field]:
                errors.append(f"{owner}: crosswalk row {layer} missing {field}.")
        require_string(owner, row.get("evidence_state"), f"crosswalk row {layer} evidence_state", errors)
        require_string(owner, row.get("public_claim_boundary"), f"crosswalk row {layer} public_claim_boundary", errors)
    return len(rows)


def validate_gate_mappings(record: dict[str, Any], owner: str, errors: list[str]) -> int:
    rows = record.get("architecture_gate_mappings")
    if not isinstance(rows, list):
        errors.append(f"{owner}: architecture_gate_mappings must be a list.")
        return 0
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f"{owner}: architecture_gate_mappings contains a non-object row.")
            continue
        gate = str(row.get("gate", "<missing>"))
        decision = row.get("maps_to_decision")
        if decision not in ALLOWED_GATE_DECISIONS:
            errors.append(f"{owner}: gate mapping {gate} has invalid decision {decision}.")
        require_string(owner, row.get("artifact_ref"), f"gate mapping {gate} artifact_ref", errors)
    if len(rows) < 5:
        errors.append(f"{owner}: expected at least five architecture/gate mappings.")
    return len(rows)


def validate_work_board(record: dict[str, Any], owner: str, errors: list[str]) -> None:
    contract = record.get("work_board_improvement_contract")
    if not isinstance(contract, dict):
        errors.append(f"{owner}: work_board_improvement_contract must be an object.")
        return
    for field in ("objective", "gate", "evidence_artifact", "residual", "owner", "completion_criterion"):
        require_string(owner, contract.get(field), f"work_board_improvement_contract {field}", errors)


def validate_artifact_gaps(record: dict[str, Any], owner: str, errors: list[str]) -> int:
    gaps = record.get("artifact_gaps")
    if not isinstance(gaps, list):
        errors.append(f"{owner}: artifact_gaps must be a list.")
        return 0
    for row in gaps:
        if not isinstance(row, dict):
            errors.append(f"{owner}: artifact_gaps contains a non-object row.")
            continue
        gap = str(row.get("gap", "<missing>"))
        if row.get("visible") is not True or row.get("blocks_support_movement") is not True:
            errors.append(f"{owner}: artifact gap {gap} must stay visible and block support movement.")
    if len(gaps) < 6:
        errors.append(f"{owner}: expected at least six visible artifact gaps.")
    return len(gaps)


def validate_ladder(record: dict[str, Any], owner: str, errors: list[str]) -> int:
    ladder = record.get("intervention_ladder")
    if not isinstance(ladder, list):
        errors.append(f"{owner}: intervention_ladder must be a list.")
        return 0
    levels = [row.get("level") for row in ladder if isinstance(row, dict)]
    if levels != list(range(len(ladder))):
        errors.append(f"{owner}: intervention ladder levels must be contiguous from 0.")
    for row in ladder:
        if not isinstance(row, dict):
            errors.append(f"{owner}: intervention_ladder contains a non-object row.")
            continue
        require_string(owner, row.get("name"), f"intervention_ladder level {row.get('level')} name", errors)
        if row.get("level") != 0 and row.get("requires_review") is not True:
            errors.append(f"{owner}: intervention ladder level {row.get('level')} must require review.")
    if len(ladder) < 6:
        errors.append(f"{owner}: expected at least six intervention ladder levels.")
    return len(ladder)


def validate_non_claims(record: dict[str, Any], owner: str, errors: list[str]) -> None:
    non_claims = record.get("non_claims")
    if not isinstance(non_claims, list) or not non_claims:
        errors.append(f"{owner}: non_claims must be a non-empty list.")
        return
    blob = text_blob(non_claims)
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in blob:
            errors.append(f"{owner}: non_claims missing {phrase!r}.")


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    validate_scalars(record, owner, errors)
    validate_components(record, owner, errors)
    ready, blocked = validate_replay_rows(record, owner, errors)
    crosswalk_count = validate_crosswalk(record, owner, errors)
    gate_count = validate_gate_mappings(record, owner, errors)
    validate_work_board(record, owner, errors)
    gap_count = validate_artifact_gaps(record, owner, errors)
    ladder_count = validate_ladder(record, owner, errors)
    validate_non_claims(record, owner, errors)
    metrics = {
        "replay_ready_row_count": ready,
        "blocked_replay_row_count": blocked,
        "crosswalk_layer_count": crosswalk_count,
        "mapped_gate_decision_count": gate_count,
        "visible_artifact_gap_count": gap_count,
        "intervention_ladder_level_count": ladder_count,
    }
    return errors, metrics


def validate_invalid_fixture(path: Path, base_record: dict[str, Any], errors: list[str]) -> None:
    spec = load_json(path)
    owner = rel(path)
    if not isinstance(spec, dict):
        errors.append(f"{owner}: expected object.")
        return
    for key in ("case_id", "base_report", "mutation", "expected_error_fragment"):
        if key not in spec:
            errors.append(f"{owner}: missing {key}.")
            return
    if spec["base_report"] != rel(VALID_FIXTURE):
        errors.append(f"{owner}: base_report must be {rel(VALID_FIXTURE)}.")
    mutation = spec.get("mutation")
    if not isinstance(mutation, dict) or not isinstance(mutation.get("path"), str) or "value" not in mutation:
        errors.append(f"{owner}: mutation must contain path and value.")
        return
    mutated = copy.deepcopy(base_record)
    try:
        set_path(mutated, mutation["path"], mutation["value"])
    except (KeyError, IndexError, ValueError):
        errors.append(f"{owner}: mutation path {mutation['path']!r} does not exist.")
        return
    observed, _metrics = validate_record(mutated, owner)
    if not observed:
        errors.append(f"{owner}: expected invalid mutation passed validation.")
        return
    expected_fragment = str(spec["expected_error_fragment"])
    if expected_fragment not in "\n".join(observed):
        errors.append(f"{owner}: expected error fragment {expected_fragment!r}; got {observed}.")


def build_result(record: dict[str, Any], metrics: dict[str, int], invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "0.1",
        "result_id": "2026-07-02-theseus-report-bundle-audit",
        "audit_id": AUDIT_ID,
        "validation_result": "pass",
        "valid_fixture_count": 1,
        "expected_invalid_count": invalid_count,
        "valid_fixture_sha256": stable_hash(record),
        "bundle_component_count": len(record.get("bundle_components", [])),
        **metrics,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "ci_verification_command": COMMAND,
        "artifact_refs": [
            rel(VALID_FIXTURE),
            rel(DOC),
            rel(RESULT),
            "docs/theseus_report_import_slice.md",
            "docs/theseus_generation_mode_import_slice.md",
            "docs/theseus_support_replay_probe.md",
            "lean/AsiStackProofs/TheseusReference.lean"
        ],
        "lean_bridge": {
            "lean_module": "lean/AsiStackProofs/TheseusReference.lean",
            "checked_theorem_names": [
                "complete_theseus_report_bundle_audit_accepts",
                "accepted_theseus_report_bundle_audit_preserves_public_boundaries",
                "complete_theseus_report_bundle_audit_satisfies_public_bundle_review"
            ]
        },
        "non_claims": record["non_claims"],
    }


def validate_result(expected_result: dict[str, Any], errors: list[str]) -> None:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}. Run `{COMMAND} --write-result`.")
        return
    observed = load_json(RESULT)
    if observed != expected_result:
        errors.append(f"{rel(RESULT)} is out of date. Run `{COMMAND} --write-result`.")


def validate_doc(expected_result: dict[str, Any], errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"Missing {rel(DOC)}.")
        return
    text = DOC.read_text(encoding="utf-8")
    required = (
        "Project Theseus Report Bundle Audit",
        AUDIT_ID,
        rel(VALID_FIXTURE),
        rel(RESULT),
        COMMAND,
        "Expected-invalid controls | 7",
        "Replay-ready rows | 2",
        "Blocked replay rows | 1",
        "Crosswalk rows | 8",
        "Architecture/gate mapping rows | 5",
        "Visible artifact gaps | 6",
        "Intervention ladder levels | 6",
        "Support-state effect | `none`",
        "does not rerun Project Theseus",
        "does not promote any chapter core claim above `argument`",
        "does not create a support-state transition",
    )
    for fragment in required:
        if fragment not in text:
            errors.append(f"{rel(DOC)} missing required fragment: {fragment}")
    if str(expected_result["valid_fixture_sha256"]) not in text and "Valid fixtures | 1" not in text:
        errors.append(f"{rel(DOC)} must expose either the valid fixture digest or the fixture count.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="Write the deterministic result record.")
    args = parser.parse_args()

    errors: list[str] = []
    if not VALID_FIXTURE.exists():
        fail([f"Missing {rel(VALID_FIXTURE)}."])
    record = load_json(VALID_FIXTURE)
    if not isinstance(record, dict):
        fail([f"{rel(VALID_FIXTURE)} must contain a JSON object."])

    record_errors, metrics = validate_record(record, rel(VALID_FIXTURE))
    errors.extend(record_errors)

    invalid_fixtures = sorted(INVALID_DIR.glob("*.invalid.json"))
    if len(invalid_fixtures) != 7:
        errors.append(f"{rel(INVALID_DIR)} must contain exactly 7 expected-invalid fixtures.")
    for path in invalid_fixtures:
        validate_invalid_fixture(path, record, errors)

    expected_result = build_result(record, metrics, len(invalid_fixtures))
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(expected_result, indent=2) + "\n", encoding="utf-8")
    else:
        validate_result(expected_result, errors)
    validate_doc(expected_result, errors)

    if errors:
        fail(errors)

    print(
        "Theseus report-bundle audit validation passed: "
        f"1 valid fixture, {len(invalid_fixtures)} expected-invalid controls, "
        f"{metrics['crosswalk_layer_count']} crosswalk rows, "
        f"{metrics['visible_artifact_gap_count']} visible artifact gaps, support-state effect none."
    )


if __name__ == "__main__":
    main()
