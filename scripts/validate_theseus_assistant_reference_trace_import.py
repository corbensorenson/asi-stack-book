#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "theseus_assistant_reference_trace_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "assistant_reference_trace_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-06-local.json"
DOC = ROOT / "docs" / "theseus_assistant_reference_trace_import.md"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "theseus_assistant_reference_trace_import_prototype_backed.json"
)
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
PROJECT_LEDGER = ROOT / "docs" / "project_theseus_static_import_status_ledger.md"
OUTLINE = ROOT / "docs" / "book_outline.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
PROOF_MANIFEST = ROOT / "proofs" / "proof_manifest.json"
PROOF_TRIAGE = ROOT / "proofs" / "proof_triage.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"

COMMAND = "python3 scripts/validate_theseus_assistant_reference_trace_import.py"
IMPORT_ID = "theseus-assistant-reference-trace-import-2026-07-06"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.assistant_reference_trace_import"
PROOF_TAG = "lean:theseus.reference.assistant_reference_trace_import.fixture_bridge"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_CREATED = "2026-06-29T23:55:08.805277+00:00"
EXPECTED_REVIEWED = "2026-07-06T03:09:41Z"
EXPECTED_POLICY = "project_theseus_assistant_runtime_v0"
EXPECTED_REPORTS = {
    "assistant_runtime_report": {
        "path": "reports/theseus_assistant_runtime.json",
        "sha256": "ce7c9fec7c4fe44edbf252fc33e9923a43406546acde7b1db22a91acdb0895d4",
        "size_bytes": 135420,
    },
    "assistant_viea_trace": {
        "path": "reports/theseus_assistant_viea_trace.jsonl",
        "sha256": "f72742461c1c22ab05dc170d7a6d98cdcee7773d3ba02e08430dbba0c3a58427",
        "size_bytes": 2532244,
    },
    "assistant_runtime_markdown": {
        "path": "reports/theseus_assistant_runtime.md",
        "sha256": "96f030ee16583a4f73cc8abe456141ba2ba71c9932a24b1e77647b409dda43d3",
        "size_bytes": 4576,
    },
    "assistant_trace_schema": {
        "path": "configs/assistant_trace_schema.json",
        "sha256": "7f16d13d71f5ebe1df2d2bd4e2765e4b632329aa89998746415589fd4cf6cef2",
        "size_bytes": 2372,
    },
    "benchmark_measurement": {
        "path": "reports/theseus_benchmark_measurement.json",
        "sha256": "edfc4dc58b132f0e8e1cd423aa8d061dc8d3204fb6e5cd0bb10056905d766a85",
        "size_bytes": 13303,
    },
    "runtime_script": {
        "path": "scripts/theseus_assistant_runtime.py",
        "sha256": "6cf19c67232516840120d42efbaa42086844857c464fe5663ec169f4ebe1e0d0",
        "size_bytes": 126886,
    },
}
EXPECTED_RECORD_TYPES = [
    "intent_contract",
    "command_contract",
    "context_abi_record",
    "context_transaction",
    "context_adequacy",
    "typed_job",
    "planforge_dag",
    "runtime_adapter_invocation",
    "procedural_tool_record",
    "authority_transition",
    "authority_use_receipt",
    "resource_budget",
    "generation_mode",
    "failure_boundary",
    "artifact_graph_record",
    "claim_record",
    "evidence_transition_record",
    "residual_record",
    "policy_optimization_record",
]
EXPECTED_SUMMARY = {
    "trigger_state": "GREEN",
    "assistant_lane": "planning_assistant",
    "intent": "planning",
    "session_id": "registry_default_assistant_runtime_refresh",
    "runtime_ms": 4282,
    "assistant_trace_schema_ready": True,
    "assistant_trace_allowed_outcome_count": 5,
    "assistant_viea_trace_required": True,
    "assistant_viea_trace_complete": True,
    "assistant_viea_trace_record_count": 19,
    "gate_count": 27,
    "passed_gate_count": 27,
    "hard_gate_count": 23,
    "warning_gate_count": 4,
    "context_refresh_command_count": 5,
    "vcm_context_ready": True,
    "vcm_selected_page_count": 12,
    "vcm_page_count": 8,
    "vcm_blocker_count": 0,
    "vcm_task_family": "autonomy_governance",
    "vcm_label": "Autonomy Loop And Governance",
    "public_training_rows_written": 0,
    "external_inference_calls": 0,
    "fallback_return_count": 0,
    "expected_invalid_control_count": 11,
}
EXPECTED_ROUTE = {
    "ready": True,
    "record_count": 2203,
    "required_group_count": 4,
    "missing_required_group_count": 0,
    "governance_record_count": 117,
    "authority_record_count": 196,
    "resource_route_record_count": 161,
    "failure_boundary_count": 140,
    "evidence_transition_count": 158,
    "artifact_record_count": 180,
    "claim_ledger_entry_count": 185,
    "context_record_count": 227,
    "runtime_adapter_record_count": 92,
    "semantic_ir_record_count": 139,
    "simulation_fidelity_record_count": 49,
    "no_cheat_fault_count": 0,
    "view_trigger_state": "GREEN",
}
EXPECTED_PROCEDURAL = {
    "present": True,
    "ready": True,
    "active": True,
    "selection_matched": True,
    "selected_route_id": "default.local_planning_assistant_metadata_only_v1",
    "selected_route_scope": "assistant_intent_lane_metadata_route",
    "default_route_adopted_count": 1,
    "default_route_guarded_count": 1,
    "hard_gap_count": 0,
    "warning_count": 0,
    "matched_event_count": 55,
    "emitted_route_packet_count": 1,
    "before_metadata_verification_obligations": 220,
    "after_replay_fixture_check_count": 14,
    "metadata_obligations_per_trace": 4,
    "metadata_verification_cost_delta": -206,
    "learned_generation_claim_allowed": False,
}
EXPECTED_BENCHMARK = {
    "active": True,
    "measurement_kind": "partial_card_diagnostic",
    "latest_public_run_id": "public_transfer_measurement_partial_diagnostic_seed9_1x64",
    "latest_public_passed": 45,
    "latest_public_task_count": 64,
    "latest_public_pass_rate": 0.703125,
    "effective_card_count": 1,
    "headline_claim_allowed": False,
}
EXPECTED_THEOREMS = (
    "theseus_assistant_reference_trace_import_fixture_valid",
    "theseus_assistant_reference_trace_import_requires_all_hops",
    "theseus_assistant_reference_trace_import_private_payload_rejected",
    "theseus_assistant_reference_trace_import_core_promotion_rejected",
    "theseus_assistant_reference_trace_import_model_quality_overclaim_rejected",
    "theseus_assistant_reference_trace_import_clean_replay_overclaim_rejected",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "data/training_data/high_transfer/private_train",
    "private_train",
    "runtime/dogfood",
    "checkpoints/",
    ".npz",
    "candidate_body",
    "solution_body",
)
REQUIRED_NON_CLAIMS = (
    "does not copy the raw Project Theseus report, raw VIEA trace, raw assistant text, raw prompts",
    "does not prove clean live Project Theseus replay, current runtime state",
    "does not promote any chapter core claim above argument",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus assistant reference-trace import validation failed:")
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
        cursor = cursor[int(part)] if isinstance(cursor, list) else cursor[part]
    last = parts[-1]
    if isinstance(cursor, list):
        cursor[int(last)] = new_value
    else:
        cursor[last] = new_value


def validate_record(record: dict[str, Any], owner: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if record.get("schema_version") != "asi_stack.theseus_assistant_reference_trace_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("review_created_utc") != EXPECTED_REVIEWED:
        errors.append(f"{owner}: review_created_utc mismatch.")
    if record.get("source_created_utc") != EXPECTED_CREATED:
        errors.append(f"{owner}: source_created_utc mismatch.")
    if record.get("source_policy") != EXPECTED_POLICY:
        errors.append(f"{owner}: source_policy mismatch.")

    reports = record.get("source_reports")
    if not isinstance(reports, dict):
        errors.append(f"{owner}: source_reports must be an object.")
        reports = {}
    for key, expected in EXPECTED_REPORTS.items():
        value = reports.get(key)
        if not isinstance(value, dict):
            errors.append(f"{owner}: source_reports.{key} missing.")
            continue
        for field, expected_value in expected.items():
            if value.get(field) != expected_value:
                errors.append(f"{owner}: source_reports.{key}.{field} must be {expected_value!r}.")
        digest = value.get("sha256")
        if not isinstance(digest, str) or not SHA_RE.match(digest):
            errors.append(f"{owner}: source_reports.{key}.sha256 must be a SHA-256 digest.")

    for field in (
        "sanitized_for_public_repo",
        "private_path_fields_redacted",
    ):
        if record.get(field) is not True:
            errors.append(f"{owner}: {field} must remain true.")
    for field in (
        "raw_report_copied",
        "raw_viea_trace_copied",
        "raw_assistant_text_copied",
        "raw_prompt_copied",
        "private_payload_copied",
    ):
        if record.get(field) is not False:
            errors.append(f"{owner}: {field} must remain false.")

    public_text = text_blob(record)
    for forbidden in FORBIDDEN_PUBLIC_TEXT:
        if forbidden in public_text:
            errors.append(f"{owner}: sanitized fixture leaks forbidden private fragment {forbidden!r}.")

    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{owner}: summary must be an object.")
        summary = {}
    for field, expected in EXPECTED_SUMMARY.items():
        if summary.get(field) != expected:
            errors.append(f"{owner}: summary.{field} must be {expected!r}.")

    trace = record.get("reference_trace")
    if not isinstance(trace, dict):
        errors.append(f"{owner}: reference_trace must be an object.")
        trace = {}
    if trace.get("record_types") != EXPECTED_RECORD_TYPES:
        errors.append(f"{owner}: reference_trace.record_types must preserve the 19 required hop records.")
    if trace.get("required_record_type_count") != len(EXPECTED_RECORD_TYPES):
        errors.append(f"{owner}: reference_trace.required_record_type_count mismatch.")
    if trace.get("required_hops_present") is not True:
        errors.append(f"{owner}: reference_trace.required_hops_present must remain true.")
    for field in ("raw_trace_copied", "raw_prompt_stored"):
        if trace.get(field) is not False:
            errors.append(f"{owner}: reference_trace.{field} must remain false.")
    if trace.get("prompt_hash_only") is not True:
        errors.append(f"{owner}: reference_trace.prompt_hash_only must remain true.")

    route = record.get("route_validator_receipt")
    if not isinstance(route, dict):
        errors.append(f"{owner}: route_validator_receipt must be an object.")
        route = {}
    for field, expected in EXPECTED_ROUTE.items():
        if route.get(field) != expected:
            errors.append(f"{owner}: route_validator_receipt.{field} must be {expected!r}.")
    if "not learned-generation capability evidence" not in str(route.get("non_claim", "")):
        errors.append(f"{owner}: route validator non-claim must remain explicit.")

    procedural = record.get("procedural_route_boundary")
    if not isinstance(procedural, dict):
        errors.append(f"{owner}: procedural_route_boundary must be an object.")
        procedural = {}
    for field, expected in EXPECTED_PROCEDURAL.items():
        if procedural.get(field) != expected:
            errors.append(f"{owner}: procedural_route_boundary.{field} must be {expected!r}.")
    if "not wall-clock throughput evidence" not in str(procedural.get("metric_semantics", "")):
        errors.append(f"{owner}: procedural metric semantics must block throughput overclaim.")

    benchmark = record.get("benchmark_boundary")
    if not isinstance(benchmark, dict):
        errors.append(f"{owner}: benchmark_boundary must be an object.")
        benchmark = {}
    for field, expected in EXPECTED_BENCHMARK.items():
        if benchmark.get(field) != expected:
            errors.append(f"{owner}: benchmark_boundary.{field} must be {expected!r}.")
    blockers = benchmark.get("blockers")
    if not isinstance(blockers, list) or len(blockers) != 5:
        errors.append(f"{owner}: benchmark_boundary.blockers must list five blockers.")
    elif "latest_public_measurement_is_diagnostic_not_headline" not in blockers:
        errors.append(f"{owner}: benchmark_boundary must keep diagnostic-not-headline blocker.")

    safety = record.get("public_safety_boundary")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety_boundary must be an object.")
        safety = {}
    for field in ("public_training_rows_written", "external_inference_calls", "fallback_return_count"):
        if safety.get(field) != 0:
            errors.append(f"{owner}: public_safety_boundary.{field} must be 0.")
    for field in (
        "raw_report_copied",
        "raw_viea_trace_copied",
        "raw_assistant_text_copied",
        "raw_prompt_copied",
        "private_payload_copied",
    ):
        if safety.get(field) is not False:
            errors.append(f"{owner}: public_safety_boundary.{field} must remain false.")
    if safety.get("private_path_fields_redacted") is not True:
        errors.append(f"{owner}: public_safety_boundary.private_path_fields_redacted must remain true.")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    for field in (
        "chapter_core_promotion_claimed",
        "clean_live_theseus_replay_claimed",
        "current_runtime_state_claimed",
        "deployment_claimed",
        "model_quality_claimed",
        "benchmark_headline_claimed",
        "useful_solution_per_second_claimed",
        "route_quality_claimed",
        "private_verifier_quality_claimed",
        "learned_generation_claimed",
        "safety_claimed",
        "asi_claimed",
    ):
        if boundary.get(field) is not False:
            errors.append(f"{owner}: claim_boundary.{field} must remain false.")

    if record.get("support_state_effect") != "bounded_non_core_transition_only":
        errors.append(f"{owner}: support_state_effect mismatch.")
    if record.get("new_support_state") != "prototype-backed":
        errors.append(f"{owner}: new_support_state must remain prototype-backed.")
    if record.get("chapter_core_support_effect") != "none":
        errors.append(f"{owner}: chapter_core_support_effect must remain none.")

    non_claims = record.get("non_claims")
    if not isinstance(non_claims, list):
        errors.append(f"{owner}: non_claims must be a list.")
        non_claims = []
    non_claim_text = "\n".join(str(item) for item in non_claims)
    for required in REQUIRED_NON_CLAIMS:
        if required not in non_claim_text:
            errors.append(f"{owner}: non_claims missing {required!r}.")

    metrics = {
        "fixture_hash": stable_hash(record),
        "trace_record_type_count": len(trace.get("record_types", [])) if isinstance(trace.get("record_types"), list) else 0,
        "gate_count": summary.get("gate_count"),
        "passed_gate_count": summary.get("passed_gate_count"),
        "hard_gate_count": summary.get("hard_gate_count"),
        "warning_gate_count": summary.get("warning_gate_count"),
        "route_validator_record_count": route.get("record_count"),
        "route_validator_required_group_count": route.get("required_group_count"),
        "vcm_selected_page_count": summary.get("vcm_selected_page_count"),
        "latest_public_passed": benchmark.get("latest_public_passed"),
        "latest_public_task_count": benchmark.get("latest_public_task_count"),
        "expected_invalid_control_count": summary.get("expected_invalid_control_count"),
    }
    return errors, metrics


def validate_invalid_controls(valid: dict[str, Any]) -> tuple[list[str], dict[str, bool]]:
    errors: list[str] = []
    controls: dict[str, bool] = {}
    paths = sorted(INVALID_DIR.glob("*.invalid.json"))
    if len(paths) != EXPECTED_SUMMARY["expected_invalid_control_count"]:
        errors.append(
            f"expected {EXPECTED_SUMMARY['expected_invalid_control_count']} invalid controls; found {len(paths)}"
        )
    for path in paths:
        control = load_json(path)
        invalid_id = control.get("invalid_id")
        if not isinstance(invalid_id, str) or not invalid_id:
            errors.append(f"{rel(path)}: missing invalid_id.")
            continue
        mutated = copy.deepcopy(valid)
        mutations = control.get("mutations")
        if not isinstance(mutations, list) or not mutations:
            errors.append(f"{rel(path)}: mutations must be a non-empty list.")
            continue
        for mutation in mutations:
            if not isinstance(mutation, dict):
                errors.append(f"{rel(path)}: mutation must be an object.")
                continue
            set_path(mutated, str(mutation.get("path")), mutation.get("value"))
        invalid_errors, _ = validate_record(mutated, rel(path))
        expected_error = str(control.get("expected_error", ""))
        if not invalid_errors:
            errors.append(f"{rel(path)}: invalid control was accepted.")
            controls[invalid_id] = False
        elif expected_error and expected_error not in "\n".join(invalid_errors):
            errors.append(f"{rel(path)}: did not produce expected error fragment {expected_error!r}.")
            controls[invalid_id] = False
        else:
            controls[invalid_id] = True
    return errors, controls


def expected_result(metrics: dict[str, Any], controls: dict[str, bool]) -> dict[str, Any]:
    return {
        "verification_result": "pass",
        "import_id": IMPORT_ID,
        "claim_id": CLAIM_ID,
        "source_commit": EXPECTED_SOURCE_COMMIT,
        "source_checkout_state": "dirty_at_import_review",
        "source_created_utc": EXPECTED_CREATED,
        "review_created_utc": EXPECTED_REVIEWED,
        "valid_fixture_sha256": metrics["fixture_hash"],
        "source_report_sha256": EXPECTED_REPORTS["assistant_runtime_report"]["sha256"],
        "source_trace_sha256": EXPECTED_REPORTS["assistant_viea_trace"]["sha256"],
        "trace_record_type_count": metrics["trace_record_type_count"],
        "gate_count": metrics["gate_count"],
        "passed_gate_count": metrics["passed_gate_count"],
        "hard_gate_count": metrics["hard_gate_count"],
        "warning_gate_count": metrics["warning_gate_count"],
        "route_validator_record_count": metrics["route_validator_record_count"],
        "route_validator_required_group_count": metrics["route_validator_required_group_count"],
        "vcm_selected_page_count": metrics["vcm_selected_page_count"],
        "latest_public_passed": metrics["latest_public_passed"],
        "latest_public_task_count": metrics["latest_public_task_count"],
        "expected_invalid_control_count": len(controls),
        "invalid_controls": dict(sorted(controls.items())),
        "support_state_effect": "bounded_non_core_transition_only",
        "new_support_state": "prototype-backed",
        "chapter_core_support_effect": "none",
        "verification_command": COMMAND,
        "non_claims": [
            "bounded sanitized assistant reference-trace import only",
            "no clean live Project Theseus replay, current runtime state, model quality, benchmark superiority, deployment readiness, safety, or ASI claim",
            "no chapter core claim promotion",
        ],
    }


def validate_result_file(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"{rel(RESULT)} missing; run {COMMAND} --write-result.")
        return
    if RESULT.read_text(encoding="utf-8") != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"{rel(TRANSITION)} missing.")
        return
    record = load_json(TRANSITION)
    expected = {
        "transition_id": "v1_x_measured.theseus_assistant_reference_trace_import.prototype_backed",
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for field, expected_value in expected.items():
        if record.get(field) != expected_value:
            errors.append(f"{rel(TRANSITION)}: {field} must be {expected_value!r}.")
    blob = text_blob(record)
    for required in (
        "does not prove clean live Project Theseus replay",
        "does not promote any chapter core claim",
        "raw assistant text",
        "benchmark superiority",
        "private verifier quality",
    ):
        if required not in blob:
            errors.append(f"{rel(TRANSITION)} missing boundary text {required!r}.")


def validate_surfaces(errors: list[str]) -> None:
    required_fragments: dict[Path, list[str]] = {
        DOC: [
            IMPORT_ID,
            CLAIM_ID,
            "19 required reference-trace record types",
            "27 / 27 gates",
            "2,203 VIEA view records",
            "11 expected-invalid controls",
            "does not prove clean live Project Theseus replay",
        ],
        ACTIVE_CYCLE: [
            "assistant reference-trace import",
            "lean:theseus.reference.assistant_reference_trace_import.fixture_bridge",
            "14 narrow non-core upward transitions",
        ],
        ROADMAP: [
            "assistant reference-trace import",
            "14 accepted narrow non-core upward transitions",
            "9 prototype-backed transitions",
        ],
        LEDGER: [
            CLAIM_ID,
            "14 narrow transitions",
            "docs/theseus_assistant_reference_trace_import.md",
            "prototype-backed",
        ],
        PROJECT_LEDGER: [
            "Assistant reference-trace imports | 1",
            "docs/theseus_assistant_reference_trace_import.md",
            "11 expected-invalid controls",
        ],
        OUTLINE: [
            "Theseus assistant reference-trace import validation",
            PROOF_TAG,
        ],
        APPENDIX_E: [
            "Theseus assistant reference-trace import validation",
            "python3 scripts/validate_theseus_assistant_reference_trace_import.py",
        ],
        CHANGELOG: [
            "Import Theseus assistant reference trace",
            CLAIM_ID,
        ],
        VALIDATE_BOOK: [
            "scripts/validate_theseus_assistant_reference_trace_import.py",
            'run_validator("validate_theseus_assistant_reference_trace_import.py")',
        ],
        LEAN_FILE: [*EXPECTED_THEOREMS],
    }
    for path, fragments in required_fragments.items():
        if not path.exists():
            errors.append(f"{rel(path)} missing.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{rel(path)} missing required fragment {fragment!r}.")

    manifest_text = MANIFEST.read_text(encoding="utf-8", errors="ignore") if MANIFEST.exists() else ""
    for fragment in (
        "Theseus assistant reference-trace import validation",
        PROOF_TAG,
        "A sanitized Project Theseus assistant reference-trace import fixture",
    ):
        if fragment not in manifest_text:
            errors.append(f"{rel(MANIFEST)} missing required fragment {fragment!r}.")

    proof_text = PROOF_MANIFEST.read_text(encoding="utf-8", errors="ignore") if PROOF_MANIFEST.exists() else ""
    if PROOF_TAG not in proof_text:
        errors.append(f"{rel(PROOF_MANIFEST)} missing {PROOF_TAG}.")
    triage_text = PROOF_TRIAGE.read_text(encoding="utf-8", errors="ignore") if PROOF_TRIAGE.exists() else ""
    if PROOF_TAG not in triage_text:
        errors.append(f"{rel(PROOF_TRIAGE)} missing {PROOF_TAG}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not VALID_FIXTURE.exists():
        fail([f"{rel(VALID_FIXTURE)} missing."])
    valid = load_json(VALID_FIXTURE)
    record_errors, metrics = validate_record(valid, rel(VALID_FIXTURE))
    errors.extend(record_errors)

    invalid_errors, controls = validate_invalid_controls(valid)
    errors.extend(invalid_errors)
    expected = expected_result(metrics, controls)
    validate_result_file(expected, args.write_result, errors)
    validate_transition(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print(
        "Theseus assistant reference-trace import validation passed: "
        f"{metrics['trace_record_type_count']} trace records, "
        f"{metrics['gate_count']} gates, {len(controls)} expected-invalid controls."
    )


if __name__ == "__main__":
    main()
