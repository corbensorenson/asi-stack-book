#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "failure_taxonomy_detector" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "failure_taxonomy_detector_probe.md"
CHAPTER = ROOT / "chapters" / "failure-modes-of-ungoverned-intelligence.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "failure-modes-of-ungoverned-intelligence.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "FailureModes.lean"

COMMAND = "python3 scripts/validate_failure_taxonomy_detector_probe.py"
PROOF_TAG = "lean:failure.taxonomy.detector_probe_bridge"
CODEX_TEST_NAME = "Failure taxonomy detector and mitigation-boundary probe"
REQUIRED_THEOREMS = ["failure_taxonomy_detector_probe_bridge"]
REQUIRED_NON_CLAIMS = [
    "does not prove failure detection",
    "does not prove prevention",
    "does not prove mitigation effectiveness",
    "does not run a deployed detector",
    "does not prove evaluator independence",
    "does not promote the chapter support state",
]


INCIDENTS: list[dict[str, Any]] = [
    {
        "incident_id": "failure://authority-creep-blocked",
        "expect_valid": True,
        "failure_classes": ["authority_creep", "power_seeking_boundary"],
        "affected_contract_refs": ["contract://effect-ceiling"],
        "boundary_owner": "governance",
        "detector_refs": ["detector://authority-ceiling"],
        "invariant_ref": "invariant://authority-within-ceiling",
        "evidence_receipts": ["receipt://denied-effect"],
        "containment_path": "escalate_authority_review",
        "mitigation_route": "escalate_review",
        "residuals": ["requested authority exceeded caller ceiling"],
        "normalization_guard": "blocked path remains a failure record",
        "learning_path": "tighten authority-request preflight",
        "recurrence_count": 1,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "failure://goodhart-evaluator-drift-residualized",
        "expect_valid": True,
        "failure_classes": ["goodhart_proxy_failure", "evaluator_drift"],
        "affected_contract_refs": ["contract://benchmark-ratchet"],
        "boundary_owner": "evidence-ledger",
        "detector_refs": ["detector://anti-goodhart-check", "detector://evaluator-integrity"],
        "invariant_ref": "invariant://metric-is-not-truth",
        "evidence_receipts": ["receipt://proxy-failure", "receipt://frozen-evaluator"],
        "containment_path": "freeze_evaluator",
        "mitigation_route": "escalate_review",
        "residuals": ["proxy improved while target adequacy failed"],
        "normalization_guard": "proxy success cannot erase target failure",
        "learning_path": "add target-adequacy residual to benchmark ratchet",
        "recurrence_count": 2,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://missing-failure-class",
        "expect_valid": False,
        "failure_classes": [],
        "affected_contract_refs": ["contract://unknown"],
        "boundary_owner": "governance",
        "detector_refs": ["detector://unknown"],
        "invariant_ref": "invariant://unknown",
        "evidence_receipts": ["receipt://unknown"],
        "containment_path": "escalate_review",
        "mitigation_route": "escalate_review",
        "residuals": ["class missing"],
        "normalization_guard": "do not normalize",
        "learning_path": "classify",
        "recurrence_count": 1,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://missing-boundary-owner",
        "expect_valid": False,
        "failure_classes": ["context_pollution"],
        "affected_contract_refs": ["contract://context"],
        "boundary_owner": "",
        "detector_refs": ["detector://taint"],
        "invariant_ref": "invariant://taint-needs-grant",
        "evidence_receipts": ["receipt://taint"],
        "containment_path": "quarantine_context",
        "mitigation_route": "quarantine",
        "residuals": ["owner missing"],
        "normalization_guard": "do not normalize",
        "learning_path": "assign owner",
        "recurrence_count": 1,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://mitigation-without-receipt",
        "expect_valid": False,
        "failure_classes": ["tool_overreach"],
        "affected_contract_refs": ["contract://tool"],
        "boundary_owner": "execution",
        "detector_refs": ["detector://tool-lease"],
        "invariant_ref": "invariant://tool-within-lease",
        "evidence_receipts": [],
        "containment_path": "deny_effect",
        "mitigation_route": "block",
        "residuals": ["receipt missing"],
        "normalization_guard": "do not normalize",
        "learning_path": "record receipt",
        "recurrence_count": 1,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://authority-creep-not-blocked",
        "expect_valid": False,
        "failure_classes": ["authority_creep"],
        "affected_contract_refs": ["contract://authority"],
        "boundary_owner": "governance",
        "detector_refs": ["detector://authority-ceiling"],
        "invariant_ref": "invariant://authority-within-ceiling",
        "evidence_receipts": ["receipt://authority"],
        "containment_path": "ordinary_operation",
        "mitigation_route": "none",
        "residuals": ["authority over ceiling"],
        "normalization_guard": "do not normalize",
        "learning_path": "escalate next time",
        "recurrence_count": 1,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://goodhart-no-residual",
        "expect_valid": False,
        "failure_classes": ["goodhart_proxy_failure"],
        "affected_contract_refs": ["contract://benchmark"],
        "boundary_owner": "evidence-ledger",
        "detector_refs": ["detector://anti-goodhart-check"],
        "invariant_ref": "invariant://metric-is-not-truth",
        "evidence_receipts": ["receipt://proxy-failure"],
        "containment_path": "block_claim_promotion",
        "mitigation_route": "block",
        "residuals": [],
        "normalization_guard": "do not normalize",
        "learning_path": "add residual",
        "recurrence_count": 1,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://recurrence-without-escalation",
        "expect_valid": False,
        "failure_classes": ["evaluator_drift"],
        "affected_contract_refs": ["contract://evaluator"],
        "boundary_owner": "evidence-ledger",
        "detector_refs": ["detector://evaluator-integrity"],
        "invariant_ref": "invariant://evaluator-independent",
        "evidence_receipts": ["receipt://drift"],
        "containment_path": "freeze_evaluator",
        "mitigation_route": "no_change",
        "residuals": ["repeated drift"],
        "normalization_guard": "do not normalize",
        "learning_path": "escalate repeated drift",
        "recurrence_count": 3,
        "support_state_effect": "none",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "incident_id": "invalid://support-state-promotion",
        "expect_valid": False,
        "failure_classes": ["context_pollution"],
        "affected_contract_refs": ["contract://context"],
        "boundary_owner": "vcm",
        "detector_refs": ["detector://taint"],
        "invariant_ref": "invariant://taint-needs-grant",
        "evidence_receipts": ["receipt://taint"],
        "containment_path": "quarantine_context",
        "mitigation_route": "quarantine",
        "residuals": ["tainted packet blocked"],
        "normalization_guard": "do not normalize",
        "learning_path": "tighten context admission",
        "recurrence_count": 1,
        "support_state_effect": "promote_chapter_core",
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Failure taxonomy detector probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def incident_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    incident_id = str(record.get("incident_id", "<missing>"))
    classes = set(record.get("failure_classes", []))
    containment = str(record.get("containment_path", ""))
    mitigation = str(record.get("mitigation_route", ""))
    recurrence = int(record.get("recurrence_count", 0))

    if not incident_id.startswith(("failure://", "invalid://")):
        errors.append(f"{incident_id}: incident_id must use failure:// or invalid://.")
    for key in ("failure_classes", "affected_contract_refs", "detector_refs", "evidence_receipts", "residuals"):
        if not nonempty_list(record, key):
            errors.append(f"{incident_id}: {key} is required.")
    for key in ("boundary_owner", "invariant_ref", "containment_path", "mitigation_route", "normalization_guard", "learning_path"):
        if not str(record.get(key, "")).strip():
            errors.append(f"{incident_id}: {key} is required.")
    if "authority_creep" in classes and containment != "escalate_authority_review":
        errors.append(f"{incident_id}: authority_creep must escalate authority review.")
    if "context_pollution" in classes and containment != "quarantine_context":
        errors.append(f"{incident_id}: context_pollution must quarantine context.")
    if "evaluator_drift" in classes and containment != "freeze_evaluator":
        errors.append(f"{incident_id}: evaluator_drift must freeze evaluator.")
    if "goodhart_proxy_failure" in classes and containment not in {"block_claim_promotion", "freeze_evaluator"}:
        errors.append(f"{incident_id}: goodhart_proxy_failure must block promotion or freeze evaluator.")
    if recurrence > 1 and mitigation != "escalate_review":
        errors.append(f"{incident_id}: recurring failures must escalate review.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{incident_id}: support_state_effect must remain none.")
    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{incident_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.failure_taxonomy_detector_probe.v0",
        "result_id": "2026-07-02-failure-taxonomy-detector-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_failure_taxonomy_detector_probe",
        "valid_incident_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "incident_count": len(INCIDENTS),
        "negative_controls": {
            "missing_failure_class_rejected": True,
            "missing_boundary_owner_rejected": True,
            "mitigation_without_receipt_rejected": True,
            "authority_creep_not_blocked_rejected": True,
            "goodhart_without_residual_rejected": True,
            "recurrence_without_escalation_rejected": True,
            "support_state_promotion_rejected": True,
        },
        "coverage": {
            "authority_creep_blocked": True,
            "goodhart_evaluator_drift_residualized": True,
            "affected_contract_refs_required": True,
            "detector_refs_required": True,
            "evidence_receipts_required": True,
            "residuals_required": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.FailureModes",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "authority_creep_incident_present": True,
                "goodhart_drift_incident_present": True,
                "negative_controls_rejected": True,
                "residual_boundary_present": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic failure-taxonomy detector fixture only; no deployed detector, runtime authority gate, evaluator-independence measurement, mitigation-effectiveness result, or prevention evidence was produced.",
            "The Failure Modes chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "failure-modes-of-ungoverned-intelligence":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Failure Modes chapter.")
        return
    if CODEX_TEST_NAME.lower() not in text_blob(chapter.get("codex_tests", [])):
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "authorityCreepIncidentPresent",
        "goodhartDriftIncidentPresent",
        "negativeControlsRejected",
        "residualBoundaryPresent",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Failure Taxonomy Detector Probe",
            rel(RESULT),
            "two valid synthetic failure incidents",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Failure taxonomy detector and mitigation-boundary probe",
            rel(RESULT),
            "two valid synthetic failure incidents",
            "seven expected-invalid controls",
            "Stack failure term",
            "Goal misbinding",
            "Goal misgeneralization",
            "Context pollution",
            "Distribution shift",
            "Authority creep",
            "Power-seeking",
            "Evaluator drift",
            "Goodhart/proxy failure",
            "Hidden optimization pressure",
            "Learned optimization",
            "Tool/action overreach",
            "Side effects",
            "Residual hiding",
            "comparator bridge, not a detector",
        ],
        READER: [
            "failure taxonomy detector and mitigation-boundary probe",
            "two synthetic failure incidents",
            "not a deployed failure detector",
            "Goal misbinding",
            "goal misgeneralization",
            "Authority creep",
            "power-seeking pressure",
            "Evaluator drift",
            "Goodhart",
            "Hidden optimization pressure",
            "learned-optimization risk",
            "Tool overreach",
            "side-effect",
            "Residual hiding",
            "metric laundering",
            "does not prove detection or prevention",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT), "External taxonomy bridge"],
        ROADMAP: [
            "Failure taxonomy detector and mitigation-boundary probe",
            "deterministic synthetic failure-taxonomy detector fixture",
            "validator-guarded live and curated reader taxonomy bridge",
            "no support-state promotion",
        ],
        CHANGELOG: ["Failure taxonomy detector and mitigation-boundary probe", rel(RESULT), "Tighten Failure Modes taxonomy bridge"],
        VALIDATION_REGISTRY: [
            "scripts/validate_failure_taxonomy_detector_probe.py",
            "docs/failure_taxonomy_detector_probe.md",
            "experiments/failure_taxonomy_detector/results/2026-07-02-local.json",
            '"script": "validate_failure_taxonomy_detector_probe.py"',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required failure taxonomy detector surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for incident in INCIDENTS:
        expect_valid = bool(incident.get("expect_valid"))
        current_errors = incident_errors(incident)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{incident.get('incident_id', '<missing>')}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic failure incidents.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Failure taxonomy detector probe validation passed.")


if __name__ == "__main__":
    main()
