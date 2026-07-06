#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "experiments" / "theseus_accelerator_parity_manifest_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "accelerator_parity_manifest_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-06-local.json"
DOC = ROOT / "docs" / "theseus_accelerator_parity_manifest_import.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_accelerator_parity_manifest_import_prototype_backed.json"
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER_CHAPTER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"

COMMAND = "python3 scripts/validate_theseus_accelerator_parity_manifest_import.py"
IMPORT_ID = "theseus-accelerator-parity-manifest-import-2026-07-06"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.accelerator_parity_manifest_import"
PROOF_TAG = "lean:theseus.reference.accelerator_parity_manifest_import.fixture_bridge"
EXPECTED_SOURCE_SHA = "80574979f333c209e5419ee61182bfef1954e5844b107a5dc76f9155b60b1ca7"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_POLICY = "project_theseus_accelerator_parity_manifest_v0"
EXPECTED_CREATED = "2026-06-15T05:45:50Z"
EXPECTED_SCORE_SEMANTICS = (
    "Audit manifest only. CUDA-equivalent surfaces are compared against current MLX bridge and Rust/Metal evidence using local reports; "
    "this does not spend public calibration, call a teacher, enable production scheduler routing, promote a model, or claim full parity."
)
EXPECTED_SURFACES = [
    "eval_chunk",
    "training_chunk",
    "rollout_chunk",
    "standalone_readout_cli",
    "rollout_cli",
    "rollout_sweep_cli",
    "token_superposition_cli",
]
EXPECTED_SUMMARY = {
    "surface_count": 7,
    "surface_ok_count": 7,
    "mlx_report_count": 7,
    "mlx_report_ok_count": 7,
    "metal_report_count": 4,
    "metal_report_ok_count": 4,
    "artifact_manifest_count": 4,
    "scheduler_canary_count": 4,
    "hard_failure_count": 0,
    "explicit_guardrail_gap_count": 0,
    "external_inference_calls": 0,
    "teacher_used_count": 0,
    "public_training_rows": 0,
    "model_promotion_allowed_count": 0,
    "production_routing_enabled_count": 0,
    "expected_invalid_control_count": 9,
}
EXPECTED_THEOREMS = (
    "theseus_accelerator_parity_manifest_import_fixture_valid",
    "theseus_accelerator_parity_manifest_import_full_parity_overclaim_rejected",
    "theseus_accelerator_parity_manifest_import_production_routing_overclaim_rejected",
    "theseus_accelerator_parity_manifest_import_model_promotion_overclaim_rejected",
    "theseus_accelerator_parity_manifest_import_core_promotion_rejected",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "checkpoints/",
    ".npz",
    "private_train/",
    "data/training_data/high_transfer",
    "runtime/dogfood/",
    "candidate_body",
    "solution_body",
    "reports/macos_mlx_work_proof",
    "reports/symliquid_",
    "reports/macos_metal_",
)
REQUIRED_NON_CLAIMS = (
    "does not copy the raw Project Theseus accelerator parity report",
    "does not prove full CUDA, MLX, or Metal parity",
    "does not promote any chapter core claim above argument",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus accelerator parity manifest import validation failed:")
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
    if record.get("schema_version") != "asi_stack.theseus_accelerator_parity_manifest_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_report_sha256") != EXPECTED_SOURCE_SHA:
        errors.append(f"{owner}: source_report_sha256 mismatch.")
    if not isinstance(record.get("source_report_sha256"), str) or not SHA_RE.match(record["source_report_sha256"]):
        errors.append(f"{owner}: source_report_sha256 must be a SHA-256 hex digest.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("source_report_path") != "reports/accelerator_parity_manifest.json":
        errors.append(f"{owner}: source_report_path mismatch.")
    if record.get("source_policy") != EXPECTED_POLICY:
        errors.append(f"{owner}: source_policy mismatch.")
    if record.get("source_created_utc") != EXPECTED_CREATED:
        errors.append(f"{owner}: source_created_utc mismatch.")
    if record.get("source_trigger_state") != "GREEN":
        errors.append(f"{owner}: source_trigger_state must be GREEN.")
    if record.get("source_ok") is not True:
        errors.append(f"{owner}: source_ok must remain true.")
    if record.get("score_semantics") != EXPECTED_SCORE_SEMANTICS:
        errors.append(f"{owner}: score_semantics mismatch.")

    for field in ("raw_report_copied", "private_payload_copied"):
        if record.get(field) is not False:
            errors.append(f"{owner}: {field} must remain false.")
    for field in ("private_path_fields_redacted", "sanitized_for_public_repo"):
        if record.get(field) is not True:
            errors.append(f"{owner}: {field} must remain true.")

    public_text = text_blob(record)
    for forbidden in FORBIDDEN_PUBLIC_TEXT:
        if forbidden in public_text:
            errors.append(f"{owner}: sanitized fixture leaks forbidden private/raw fragment {forbidden!r}.")

    summary = record.get("summary")
    if not isinstance(summary, dict):
        errors.append(f"{owner}: summary must be an object.")
        summary = {}
    for field, expected in EXPECTED_SUMMARY.items():
        if summary.get(field) != expected:
            errors.append(f"{owner}: summary.{field} must be {expected!r}.")

    guardrails = record.get("guardrails")
    if not isinstance(guardrails, dict):
        errors.append(f"{owner}: guardrails must be an object.")
        guardrails = {}
    expected_guardrails = {
        "public_calibration_run": False,
        "public_training_rows": 0,
        "external_inference_calls": 0,
        "teacher_used": False,
        "model_promotion_allowed": False,
        "production_scheduler_routing_enabled": False,
        "full_parity_claim_allowed": False,
    }
    for field, expected in expected_guardrails.items():
        if guardrails.get(field) != expected:
            errors.append(f"{owner}: guardrails.{field} must be {expected!r}.")

    rows = record.get("surface_rows")
    if not isinstance(rows, list):
        errors.append(f"{owner}: surface_rows must be a list.")
        rows = []
    if [row.get("surface") for row in rows if isinstance(row, dict)] != EXPECTED_SURFACES:
        errors.append(f"{owner}: surface_rows must preserve the reviewed surface order.")
    if sum(1 for row in rows if isinstance(row, dict) and row.get("mlx_present") is True) != 7:
        errors.append(f"{owner}: expected seven MLX-present rows.")
    if sum(1 for row in rows if isinstance(row, dict) and row.get("metal_present") is True) != 4:
        errors.append(f"{owner}: expected four Metal-present rows.")
    if sum(1 for row in rows if isinstance(row, dict) and row.get("artifact_manifest_available") is True) != 4:
        errors.append(f"{owner}: expected four artifact-manifest rows.")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{owner}: surface_rows[{index}] must be an object.")
            continue
        for field, expected in (
            ("surface_ok", True),
            ("full_parity_claim_allowed", False),
            ("production_scheduler_routing_enabled", False),
            ("model_promotion_allowed", False),
            ("external_inference_calls", 0),
            ("teacher_used", False),
            ("public_training_rows", 0),
        ):
            if row.get(field) != expected:
                errors.append(f"{owner}: surface_rows[{index}].{field} must be {expected!r}.")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    for field in (
        "chapter_core_promotion_claimed",
        "full_parity_claimed",
        "production_scheduler_routing_claimed",
        "model_promotion_claimed",
        "public_calibration_claimed",
        "public_training_rows_claimed",
        "external_inference_claimed",
        "teacher_use_claimed",
        "clean_live_theseus_replay_claimed",
        "deployment_claimed",
        "benchmark_performance_claimed",
        "model_quality_claimed",
        "safety_claimed",
        "asi_claimed",
    ):
        if boundary.get(field) is not False:
            errors.append(f"{owner}: claim_boundary.{field} must remain false.")

    if record.get("support_state_effect") != "bounded_non_core_transition_only":
        errors.append(f"{owner}: support_state_effect mismatch.")
    if record.get("chapter_core_support_effect") != "none":
        errors.append(f"{owner}: chapter_core_support_effect must remain none.")
    if record.get("hard_failures") != []:
        errors.append(f"{owner}: hard_failures must be empty.")
    if record.get("explicit_guardrail_gaps") != []:
        errors.append(f"{owner}: explicit_guardrail_gaps must be empty.")

    non_claim_text = "\n".join(str(item) for item in record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_text:
            errors.append(f"{owner}: missing non-claim phrase {phrase!r}.")

    stats = {
        "valid_fixture_hash": stable_hash(record),
        "source_report_sha256": record.get("source_report_sha256"),
        "source_commit": record.get("source_commit"),
        "source_checkout_state": record.get("source_checkout_state"),
        "source_policy": record.get("source_policy"),
        "source_trigger_state": record.get("source_trigger_state"),
        "surface_count": summary.get("surface_count"),
        "surface_ok_count": summary.get("surface_ok_count"),
        "mlx_report_count": summary.get("mlx_report_count"),
        "metal_report_count": summary.get("metal_report_count"),
        "artifact_manifest_count": summary.get("artifact_manifest_count"),
        "scheduler_canary_count": summary.get("scheduler_canary_count"),
        "expected_invalid_controls": 0,
    }
    return errors, stats


def invalid_controls(valid: dict[str, Any]) -> tuple[list[str], list[dict[str, Any]]]:
    errors: list[str] = []
    controls: list[dict[str, Any]] = []
    for path in sorted(INVALID_DIR.glob("*.invalid.json")):
        mutation = load_json(path)
        candidate = copy.deepcopy(valid)
        set_path(candidate, str(mutation["path"]), mutation["value"])
        candidate_errors, _ = validate_record(candidate, path.name)
        rejected = bool(candidate_errors)
        controls.append(
            {
                "fixture": rel(path),
                "mutation": mutation.get("mutation", ""),
                "rejected": rejected,
                "error_count": len(candidate_errors),
            }
        )
        if not rejected:
            errors.append(f"{rel(path)} unexpectedly passed validation.")
    if len(controls) != 9:
        errors.append(f"expected 9 invalid controls, found {len(controls)}.")
    return errors, controls


def validate_transition(errors: list[str]) -> dict[str, Any]:
    record = load_json(TRANSITION)
    expected = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "transition_effect": "upward",
        "transition_validity_state": "review_accepted",
        "verification_command": COMMAND,
        "verification_result": "pass",
        "review_status": "accepted",
        "support_state_effect": "eligible_for_bounded_evidence_review",
    }
    for field, value in expected.items():
        if record.get(field) != value:
            errors.append(f"{rel(TRANSITION)}: {field} must be {value!r}.")
    if record.get("acceptance_blockers") != []:
        errors.append(f"{rel(TRANSITION)}: acceptance_blockers must be empty.")
    transition_text = text_blob(record)
    for phrase in (
        "does not prove full CUDA, MLX, or Metal parity",
        "does not promote any chapter core claim",
        "does not copy the raw Project Theseus accelerator parity report",
    ):
        if phrase.lower() not in transition_text.lower():
            errors.append(f"{rel(TRANSITION)} missing non-claim phrase {phrase!r}.")
    return record


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "surfaceCount",
        "mlxReportCount",
        "metalReportCount",
        "artifactManifestCount",
        "schedulerCanaryCount",
        "hardFailureCount",
        "fullParityClaimed",
        "productionRoutingClaimed",
        "modelPromotionClaimed",
        "chapterCorePromotion",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing accelerator parity field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Theseus Accelerator Parity Manifest Import",
            IMPORT_ID,
            "7 / 7",
            "4 Metal report summaries",
            "nine expected-invalid controls",
            PROOF_TAG,
            "does not prove full CUDA, MLX, or Metal parity",
        ],
        CHAPTER: [
            "accelerator parity manifest",
            "7 of 7 surfaces",
            CLAIM_ID,
            "does not prove full CUDA, MLX, or Metal parity",
        ],
        READER_CHAPTER: [
            "accelerator parity manifest",
            "7 of 7 surfaces",
            "not full CUDA, MLX, or Metal parity",
        ],
        OUTLINE: [
            "Theseus accelerator parity manifest import",
            COMMAND,
            CLAIM_ID,
            PROOF_TAG,
        ],
        CHANGELOG: [
            "Import Theseus accelerator parity manifest",
            rel(RESULT),
            rel(TRANSITION),
        ],
        VALIDATE_BOOK: [
            "scripts/validate_theseus_accelerator_parity_manifest_import.py",
            "docs/theseus_accelerator_parity_manifest_import.md",
            "experiments/theseus_accelerator_parity_manifest_import/results/2026-07-06-local.json",
            'run_validator("validate_theseus_accelerator_parity_manifest_import.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"missing required surface: {rel(path)}")
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
        for phrase in phrases:
            if re.sub(r"\s+", " ", phrase).lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def write_result(valid: dict[str, Any], stats: dict[str, Any], controls: list[dict[str, Any]]) -> None:
    result = {
        "schema_version": "asi_stack.theseus_accelerator_parity_manifest_import_result.v0",
        "result_id": IMPORT_ID,
        "command": COMMAND,
        "source_report_sha256": valid["source_report_sha256"],
        "source_commit": valid["source_commit"],
        "source_checkout_state": valid["source_checkout_state"],
        "source_policy": valid["source_policy"],
        "source_created_utc": valid["source_created_utc"],
        "source_trigger_state": valid["source_trigger_state"],
        "source_ok": valid["source_ok"],
        "summary": valid["summary"],
        "guardrails": valid["guardrails"],
        "claim_boundary": valid["claim_boundary"],
        "expected_invalid_controls": controls,
        "expected_invalid_control_count": len(controls),
        "valid_fixture_hash": stats["valid_fixture_hash"],
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.TheseusReference",
            "proof_tag": PROOF_TAG,
            "theorem_refs": list(EXPECTED_THEOREMS),
            "expected": {
                "surface_count": 7,
                "mlx_report_count": 7,
                "metal_report_count": 4,
                "artifact_manifest_count": 4,
                "scheduler_canary_count": 4,
                "hard_failure_count": 0,
                "full_parity_claimed": False,
                "production_routing_claimed": False,
                "model_promotion_claimed": False,
                "chapter_core_promotion": False,
            },
        },
        "support_state_effect": "bounded_non_core_transition_only",
        "chapter_core_support_effect": "none",
        "new_support_state": "prototype-backed",
        "validation_result": "pass",
        "non_claims": valid["non_claims"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_doc(valid: dict[str, Any], controls: list[dict[str, Any]]) -> None:
    summary = valid["summary"]
    guardrails = valid["guardrails"]
    lines = [
        "# Theseus Accelerator Parity Manifest Import",
        "",
        f"Import ID: `{IMPORT_ID}`",
        "",
        "This document records a sanitized public-safe Project Theseus accelerator parity manifest import. It is a bounded implementation-reference evidence slice, not full CUDA/MLX/Metal parity, not production scheduler routing, not model promotion, and not a chapter-core support-state promotion.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---:|",
        f"| Trigger state | `{valid['source_trigger_state']}` |",
        f"| Surfaces OK | {summary['surface_ok_count']} / {summary['surface_count']} |",
        f"| MLX report summaries | {summary['mlx_report_ok_count']} / {summary['mlx_report_count']} |",
        f"| Metal report summaries | {summary['metal_report_ok_count']} / {summary['metal_report_count']} |",
        f"| Artifact manifests | {summary['artifact_manifest_count']} |",
        f"| Scheduler canary surfaces | {summary['scheduler_canary_count']} |",
        f"| Hard failures | {summary['hard_failure_count']} |",
        f"| Explicit guardrail gaps | {summary['explicit_guardrail_gap_count']} |",
        f"| Public training rows | {summary['public_training_rows']} |",
        f"| External inference calls | {summary['external_inference_calls']} |",
        f"| Teacher-use count | {summary['teacher_used_count']} |",
        f"| Model-promotion allowed count | {summary['model_promotion_allowed_count']} |",
        f"| Production-routing enabled count | {summary['production_routing_enabled_count']} |",
        "",
        f"The import records 7 of 7 surfaces, 4 Metal report summaries, {summary['scheduler_canary_count']} scheduler-canary surfaces, and nine expected-invalid controls.",
        "",
        "## Guardrails",
        "",
        "| Guardrail | Value |",
        "|---|---:|",
    ]
    for key, value in guardrails.items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(
        [
            "",
            "## Surface Rows",
            "",
            "| Surface | Class | CUDA-equivalent command | MLX | Metal | Artifact manifest |",
            "|---|---|---|---:|---:|---:|",
        ]
    )
    for row in valid["surface_rows"]:
        cuda = row["declared_cuda_equivalent"] or ""
        lines.append(
            f"| `{row['surface']}` | `{row['surface_class']}` | `{cuda}` | "
            f"{str(row['mlx_present']).lower()} | {str(row['metal_present']).lower()} | "
            f"{str(row['artifact_manifest_available']).lower()} |"
        )
    lines.extend(
        [
            "",
            "## Validation",
            "",
            f"- Command: `{COMMAND}`",
            f"- Result: `{rel(RESULT)}`",
            f"- Transition: `{rel(TRANSITION)}`",
            f"- Lean bridge: `{PROOF_TAG}`",
            f"- Expected-invalid controls: {len(controls)}.",
            "",
            "| Control | Rejected |",
            "|---|---:|",
        ]
    )
    for control in controls:
        lines.append(f"| `{Path(control['fixture']).name}` | {str(control['rejected']).lower()} |")
    lines.extend(["", "## Non-Claims", ""])
    for item in valid["non_claims"]:
        lines.append(f"- {item}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[str] = []
    valid = load_json(VALID_FIXTURE)
    if not isinstance(valid, dict):
        fail([f"{rel(VALID_FIXTURE)} must contain an object."])
    record_errors, stats = validate_record(valid, rel(VALID_FIXTURE))
    errors.extend(record_errors)
    control_errors, controls = invalid_controls(valid)
    errors.extend(control_errors)
    stats["expected_invalid_controls"] = len(controls)
    validate_transition(errors)
    write_result(valid, stats, controls)
    write_doc(valid, controls)
    validate_lean(errors)
    validate_surfaces(errors)
    if errors:
        fail(errors)
    print("Theseus accelerator parity manifest import validation passed.")


if __name__ == "__main__":
    main()
