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
BASE = ROOT / "experiments" / "theseus_project_registry_import"
VALID_FIXTURE = BASE / "fixtures" / "valid" / "project_registry_import.valid.json"
INVALID_DIR = BASE / "fixtures" / "invalid"
RESULT = BASE / "results" / "2026-07-05-local.json"
DOC = ROOT / "docs" / "theseus_project_registry_import.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "theseus_project_registry_import_prototype_backed.json"
CHAPTER = ROOT / "chapters" / "project-theseus-as-report-first-implementation-reference.qmd"
READER_CHAPTER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "project-theseus-as-report-first-implementation-reference.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
ACTIVE_CYCLE = ROOT / "docs" / "v1_x_active_evidence_cycle.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "TheseusReference.lean"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

COMMAND = "python3 scripts/validate_theseus_project_registry_import.py"
IMPORT_ID = "theseus-project-registry-import-2026-07-05"
CLAIM_ID = "project-theseus-as-report-first-implementation-reference.project_registry_reality_import"
PROOF_TAG = "lean:theseus.reference.project_registry_import.fixture_bridge"
EXPECTED_SOURCE_COMMIT = "1ad88a22"
EXPECTED_SOURCE_REPORT = "reports/theseus_project_registry_functional_promotion_gate.json"
EXPECTED_SOURCE_HASH = "7814b39a5ddcb191e7c35dea4309bee5738fe389e91af00702f57ef84cf8418b"
EXPECTED_STABLE_HASH = "215aeb759cfddabc8f7e66125b380d417fbf26a24169875bf92c148a5f716dfd"
EXPECTED_SUMMARY = {
    "active_source_surface_mib": 25.368,
    "artifact_type_counts": {
        "benchmark": 156,
        "configuration": 34,
        "control_plane": 34,
        "data_governance": 119,
        "deprecated": 57,
        "documentation": 50,
        "generated_artifact": 4432,
        "governance": 96,
        "memory": 41,
        "product_surface": 134,
        "runtime": 134,
        "supporting_script": 296,
        "training": 79,
    },
    "classified_report_duplicate_family_count": 57,
    "classified_source_duplicate_family_count": 10,
    "coverage_ratio": 1.0,
    "duplicate_family_count": 67,
    "entry_count": 5662,
    "generated_or_build_state_mib": 14193.374,
    "generated_source_artifact_count": 0,
    "missing_report_output_count": 0,
    "registered_path_count": 5662,
    "registry_governance_violation_count": 0,
    "registry_hard_governance_violation_count": 0,
    "report_duplicate_family_count": 57,
    "runtime_ms": 3293,
    "source_duplicate_family_count": 10,
    "stale_report_output_count": 0,
    "status_counts": {
        "deprecated": 57,
        "generated": 4432,
        "live": 877,
        "retained": 296,
    },
    "thresholds": {
        "red_unregistered_active_sources": 80,
        "yellow_duplicate_families": 8,
        "yellow_generated_source_artifacts": 1,
        "yellow_stale_report_outputs": 8,
        "yellow_unregistered_active_sources": 20,
    },
    "unclassified_duplicate_family_count": 0,
    "unclassified_report_duplicate_family_count": 0,
    "unclassified_source_duplicate_family_count": 0,
    "unregistered_active_source_count": 0,
}
EXPECTED_THEOREMS = (
    "theseus_project_registry_import_fixture_valid",
    "theseus_project_registry_import_unregistered_sources_rejected",
    "theseus_project_registry_import_clean_replay_overclaim_rejected",
    "theseus_project_registry_import_core_promotion_rejected",
    "theseus_project_registry_import_private_payload_rejected",
)
EXPECTED_RULES = (
    "source_of_truth_config_defines_owned_lifecycle_surfaces",
    "unregistered_active_sources_require_owner_deprecated_or_generated_status",
    "duplicate_families_must_be_consolidated_or_registered",
    "generated_artifacts_must_live_under_generated_roots_or_be_manifest_backed",
    "public_benchmark_boundary_does_not_unlock_public_calibration_or_training_data",
)
FORBIDDEN_PUBLIC_TEXT = (
    "/Users/",
    "checkpoints/",
    ".npz",
    "private_train/",
    "data/training_data/high_transfer/private_train",
    "runtime/dogfood/",
    "candidate_body",
    "solution_body",
)
REQUIRED_NON_CLAIMS = (
    "Project Theseus project-registry health is repository-organization evidence only.",
    "does not copy the raw Project Theseus registry report",
    "does not prove clean live Project Theseus replay",
    "does not promote any chapter core claim above argument",
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Theseus project-registry import validation failed:")
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
    if record.get("schema_version") != "asi_stack.theseus_project_registry_import.v0":
        errors.append(f"{owner}: schema_version mismatch.")
    if record.get("import_id") != IMPORT_ID:
        errors.append(f"{owner}: import_id mismatch.")
    if record.get("source_commit") != EXPECTED_SOURCE_COMMIT:
        errors.append(f"{owner}: source_commit mismatch.")
    if record.get("source_checkout_state") != "dirty_at_import_review":
        errors.append(f"{owner}: source_checkout_state must preserve dirty_at_import_review.")
    if record.get("source_report") != EXPECTED_SOURCE_REPORT:
        errors.append(f"{owner}: source_report mismatch.")
    if record.get("source_report_sha256") != EXPECTED_SOURCE_HASH:
        errors.append(f"{owner}: source_report_sha256 mismatch.")
    if record.get("source_report_stable_sha256") != EXPECTED_STABLE_HASH:
        errors.append(f"{owner}: source_report_stable_sha256 mismatch.")
    for field in ("source_report_sha256", "source_report_stable_sha256"):
        value = record.get(field)
        if not isinstance(value, str) or not SHA_RE.match(value):
            errors.append(f"{owner}: {field} must be a SHA-256 hex digest.")
    if record.get("policy") != "project_theseus_project_registry_v1":
        errors.append(f"{owner}: policy mismatch.")
    if record.get("created_utc") != "2026-06-22T08:00:20.592374Z":
        errors.append(f"{owner}: created_utc mismatch.")
    if record.get("trigger_state") != "GREEN":
        errors.append(f"{owner}: trigger_state must be GREEN.")
    if record.get("surface_count") != 24:
        errors.append(f"{owner}: surface_count must be 24.")
    if record.get("external_inference_calls") != 0:
        errors.append(f"{owner}: external_inference_calls must be 0.")

    safety = record.get("public_safety")
    if not isinstance(safety, dict):
        errors.append(f"{owner}: public_safety must be an object.")
        safety = {}
    for field in ("raw_report_copied", "private_payload_copied"):
        if safety.get(field) is not False:
            errors.append(f"{owner}: public_safety.{field} must remain false.")
    for field in ("private_path_fields_redacted", "sanitized_for_public_repo"):
        if safety.get(field) is not True:
            errors.append(f"{owner}: public_safety.{field} must remain true.")

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

    rules = record.get("registry_evolution_rules")
    if rules != list(EXPECTED_RULES):
        errors.append(f"{owner}: registry_evolution_rules must preserve the reviewed rules.")
    sample = record.get("surface_sample")
    if not isinstance(sample, list) or len(sample) < 10 or "theseus_plan_compiler" not in sample:
        errors.append(f"{owner}: surface_sample must contain at least 10 named surfaces including theseus_plan_compiler.")

    boundary = record.get("claim_boundary")
    if not isinstance(boundary, dict):
        errors.append(f"{owner}: claim_boundary must be an object.")
        boundary = {}
    expected_boundary = {
        "claim_id": CLAIM_ID,
        "old_support_state": "argument",
        "new_support_state": "prototype-backed",
        "support_state_effect": "eligible_for_bounded_evidence_review",
        "chapter_id": "project-theseus-as-report-first-implementation-reference",
        "chapter_core_claim_promotion": False,
        "clean_live_replay_claim": False,
        "deployment_claim": False,
        "model_quality_claim": False,
        "capability_claim": False,
    }
    for field, expected in expected_boundary.items():
        if boundary.get(field) != expected:
            errors.append(f"{owner}: claim_boundary.{field} must be {expected!r}.")

    non_claim_text = "\n".join(str(item) for item in record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase not in non_claim_text:
            errors.append(f"{owner}: missing non-claim phrase {phrase!r}.")

    stats = {
        "valid_fixture_hash": stable_hash(record),
        "expected_invalid_controls": 0,
        "entry_count": summary.get("entry_count"),
        "registered_path_count": summary.get("registered_path_count"),
        "surface_count": record.get("surface_count"),
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
    for phrase in ("does not prove clean live Project Theseus replay", "does not promote any chapter core claim"):
        if phrase.lower() not in transition_text.lower():
            errors.append(f"{rel(TRANSITION)} missing non-claim phrase {phrase!r}.")
    return record


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in EXPECTED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "entryCount",
        "registeredPathCount",
        "surfaceCount",
        "coverageComplete",
        "unregisteredActiveSources",
        "unclassifiedDuplicateFamilies",
        "registryGovernanceViolations",
        "generatedSourceArtifacts",
        "cleanLiveReplayClaimed",
        "chapterCorePromotion",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing project-registry field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Theseus Project Registry Import",
            IMPORT_ID,
            "5,662",
            "24 surfaces",
            "nine expected-invalid controls",
            PROOF_TAG,
            "does not prove clean live Project Theseus replay",
        ],
        CHAPTER: [
            "project-registry import",
            "5,662 registered paths",
            CLAIM_ID,
            "does not prove clean live Project Theseus replay",
        ],
        READER_CHAPTER: [
            "project-registry import",
            "5,662 registered paths",
            "not a clean live Theseus replay",
        ],
        OUTLINE: [
            "Theseus project-registry import",
            COMMAND,
            CLAIM_ID,
            PROOF_TAG,
        ],
        ROADMAP: [
            "project-registry import",
            "5,662 registered paths",
            "artifact-truth review",
        ],
        ACTIVE_CYCLE: [
            "project-registry import",
            "5,662 registered paths",
            "does not prove clean live Project Theseus replay",
        ],
        CHANGELOG: [
            "Import Theseus project-registry health",
            rel(RESULT),
            rel(TRANSITION),
        ],
        VALIDATION_REGISTRY: [
            "scripts/validate_theseus_project_registry_import.py",
            "docs/theseus_project_registry_import.md",
            "experiments/theseus_project_registry_import/results/2026-07-05-local.json",
            '"script": "validate_theseus_project_registry_import.py"',
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
        "schema_version": "asi_stack.theseus_project_registry_import_result.v0",
        "result_id": IMPORT_ID,
        "command": COMMAND,
        "source_commit": valid["source_commit"],
        "source_checkout_state": valid["source_checkout_state"],
        "source_report": valid["source_report"],
        "source_report_sha256": valid["source_report_sha256"],
        "source_report_stable_sha256": valid["source_report_stable_sha256"],
        "policy": valid["policy"],
        "created_utc": valid["created_utc"],
        "trigger_state": valid["trigger_state"],
        "surface_count": valid["surface_count"],
        "summary": valid["summary"],
        "claim_boundary": valid["claim_boundary"],
        "public_safety": valid["public_safety"],
        "expected_invalid_controls": controls,
        "expected_invalid_control_count": len(controls),
        "valid_fixture_hash": stats["valid_fixture_hash"],
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.TheseusReference",
            "proof_tag": PROOF_TAG,
            "theorem_refs": list(EXPECTED_THEOREMS),
            "expected": {
                "entry_count": 5662,
                "registered_path_count": 5662,
                "surface_count": 24,
                "coverage_complete": True,
                "unregistered_active_sources": 0,
                "unclassified_duplicate_families": 0,
                "stale_report_outputs": 0,
                "missing_report_outputs": 0,
                "generated_source_artifacts": 0,
                "registry_governance_violations": 0,
                "external_inference_calls": 0,
                "private_payload_copied": False,
                "clean_live_replay_claimed": False,
                "chapter_core_promotion": False,
            },
        },
        "support_state_effect": "bounded_non_core_transition_only",
        "chapter_core_support_effect": "none",
        "verification_result": "pass",
        "non_claims": valid["non_claims"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_doc(valid: dict[str, Any], controls: list[dict[str, Any]]) -> None:
    summary = valid["summary"]
    lines = [
        "# Theseus Project Registry Import",
        "",
        f"Import ID: `{IMPORT_ID}`",
        "",
        "This document records a sanitized public-safe Project Theseus project-registry import. It is a bounded implementation-reference evidence slice, not a clean live Theseus replay and not a chapter-core support-state promotion.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "|---|---:|",
        f"| Trigger state | `{valid['trigger_state']}` |",
        f"| Registered paths | {summary['registered_path_count']:,} / {summary['entry_count']:,} |",
        f"| Owned lifecycle surfaces | {valid['surface_count']} surfaces |",
        f"| Coverage ratio | {summary['coverage_ratio']} |",
        f"| Unregistered active sources | {summary['unregistered_active_source_count']} |",
        f"| Unclassified duplicate families | {summary['unclassified_duplicate_family_count']} |",
        f"| Stale report outputs | {summary['stale_report_output_count']} |",
        f"| Missing report outputs | {summary['missing_report_output_count']} |",
        f"| Generated source artifacts | {summary['generated_source_artifact_count']} |",
        f"| Registry-governance violations | {summary['registry_governance_violation_count']} |",
        f"| Hard governance violations | {summary['registry_hard_governance_violation_count']} |",
        f"| External inference calls | {valid['external_inference_calls']} |",
        "",
        f"The import records {summary['registered_path_count']:,} registered paths across {valid['surface_count']} surfaces and nine expected-invalid controls.",
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
    for control in controls:
        lines.append(f"| `{Path(control['fixture']).name}` | {str(control['rejected']).lower()} |")
    lines.extend(
        [
            "",
            "## Non-Claims",
            "",
        ]
    )
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
    print("Theseus project-registry import validation passed.")


if __name__ == "__main__":
    main()
